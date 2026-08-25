#!/usr/bin/env python3
"""HOUSE UI STANDARD v1.0 · rendered-geometry audit.

Renders a page in headless Chrome over CDP and measures what a person actually
sees, then judges it against the house rules. Everything here is measured from
the rendered box tree, never inferred from the stylesheet, because the defects
the owner named are all defects of rendering: spacing that is not quite right,
lines crossing over, graphics crossing over.

    python3 ui-audit.py http://localhost:4321
    python3 ui-audit.py path/to/page.html
    python3 ui-audit.py page.html --width 1440 --only line-box-collision,ink-occlusion
    python3 ui-audit.py page.html --json > findings.json

Default pass widths are 375, 768 and 1440. Three widths, not one, because a
fluid clamp is on the grid at its endpoints and off it everywhere between, and
because a finger is the pointer only on the narrow pass.

Exit codes:
    0  no error-level finding
    1  at least one error-level finding
    2  the page could not be rendered or measured

Requires: Python 3, websocket-client, Google Chrome. Verified on 3.9.6.
"""

import argparse
import base64
import json
import os
import re
import socket
import struct
import subprocess
import sys
import time
import urllib.request
import zlib

try:
    import websocket
except ImportError:
    sys.stderr.write("error: websocket-client is not installed · pip3 install websocket-client\n")
    raise SystemExit(2)

CHROME = os.environ.get(
    "UI_AUDIT_CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# Height is the second half of a pass. A 375 pass at 900px tall is a phone
# nobody owns, and under-fixed-chrome only means anything against a real
# viewport height, so each default width carries the height it ships with.
DEFAULT_WIDTHS = [(375, 812), (768, 1024), (1440, 900)]

# House rule 12. The ladder a reported value is snapped back to.
SPACE_LADDER = [4, 8, 12, 16, 24, 32, 48, 64, 96, 128]

# House rule 2.
WEIGHT_LADDER = {400, 600, 700, 800}

# The type ladder as it is authored in snippets/type-system.css. Five steps are
# clamp expressions, so these strings are resolved by the browser at the pass
# viewport rather than compared against hardcoded pixel numbers. A page that
# defines its own --fs-* tokens on :root overrides this, because the shared
# layer is a floor and not a ceiling.
HOUSE_FS = {
    "display-xl": "clamp(44px, 7.6vw, 96px)",
    "display-lg": "clamp(38px, 6.0vw, 72px)",
    "display-md": "clamp(32px, 4.6vw, 56px)",
    "h1": "clamp(28px, 3.2vw, 40px)",
    "h2": "clamp(24px, 2.4vw, 32px)",
    "h3": "24px",
    "h4": "20px",
    "body-lg": "20px",
    "body": "16px",
    "body-sm": "14px",
    "caption": "12px",
}

# id: (severity, default_on, one-line description)
CHECKS = {
    "line-box-collision":  ("error",   True,  "two rendered text lines sitting on each other"),
    "ink-occlusion":       ("error",   True,  "a graphic or filled panel painted over text"),
    "hairline-crosses-text": ("error", True,  "a rule or border running through type or a logo"),
    "flow-box-overlap":    ("warning", True,  "two in-flow siblings whose boxes intersect"),
    "text-clipped":        ("error",   True,  "text cut off by its own box"),
    "past-frame":          ("error",   True,  "content escaping the box meant to hold it"),
    "doc-overflow-x":      ("error",   True,  "the page scrolls sideways"),
    "under-fixed-chrome":  ("warning", True,  "content under a fixed bar at rest"),
    "spacing-off-4":       ("warning", True,  "space that is not a multiple of 4px · house rule 12"),
    "contrast-solid":      ("error",   True,  "text below WCAG 1.4.3 on a solid ground"),
    "contrast-over-image": ("warning", True,  "text over a photograph or gradient, sampled"),
    "contrast-nontext":    ("warning", True,  "a UI boundary below WCAG 1.4.11"),
    "touch-target":        ("warning", True,  "an interactive box under 44px"),
    "measure-over-75":     ("warning", True,  "a line of copy too long to track back to"),
    "type-scale":          ("warning", True,  "a font size off the house ladder"),
    "type-floor":          ("error",   True,  "type below the 12px screen floor · section 9"),
    "weight-ladder":       ("warning", True,  "a weight outside 400/600/700/800 · house rule 2"),
    "near-align":          ("note",    False, "edges that miss by one to three pixels"),
    "rhythm-gaps":         ("note",    False, "a sequence with one gap out of step"),
    "weight-size-count":   ("note",    False, "more than three weights or three sizes · house rule 3"),
}

SEVERITY_ORDER = ["blocker", "error", "warning", "note"]
ERROR_LEVEL = {"blocker", "error"}


# --------------------------------------------------------------------- chrome
def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


class Chrome(object):
    """A headless Chrome driven over the DevTools protocol.

    --remote-allow-origins=* is required or the websocket handshake is rejected
    by Chrome's origin check and every command times out with no error text.
    --hide-scrollbars keeps a reserved scrollbar gutter out of the measurement,
    which is what lets doc-overflow-x compare scrollWidth against innerWidth
    without a platform-dependent fudge factor.
    """

    def __init__(self, profile_dir, verbose=False):
        self.port = free_port()
        prof = os.path.join(profile_dir, "cdp%d" % self.port)
        os.makedirs(prof, exist_ok=True)
        self.proc = subprocess.Popen(
            [CHROME, "--headless=new", "--disable-gpu", "--no-sandbox",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             "--allow-file-access-from-files", "--remote-allow-origins=*",
             "--disable-features=CalculateNativeWinOcclusion",
             "--remote-debugging-port=%d" % self.port,
             "--user-data-dir=%s" % prof, "about:blank"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        ws = None
        for _ in range(120):
            try:
                tabs = json.loads(urllib.request.urlopen(
                    "http://127.0.0.1:%d/json" % self.port, timeout=2).read())
                page = [t for t in tabs if t.get("type") == "page"]
                if page:
                    ws = page[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                pass
            time.sleep(0.25)
        if not ws:
            raise RuntimeError("chrome did not expose a debugging target on port %d" % self.port)
        self.ws = websocket.create_connection(ws, timeout=120, max_size=512 * 1024 * 1024)
        self.i = 0
        self.verbose = verbose

    def cmd(self, method, **params):
        self.i += 1
        self.ws.send(json.dumps({"id": self.i, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.i:
                if "error" in m:
                    raise RuntimeError("%s: %s" % (method, m["error"]))
                return m.get("result", {})

    def viewport(self, width, height):
        # mobile=False on purpose. Mobile emulation gives a page with no
        # viewport meta the 980px legacy layout viewport, and every vw unit,
        # every clamp and every measured box would then be resolved against a
        # width nobody asked this tool for. A linter needs the width it was
        # given, exactly.
        self.cmd("Emulation.setDeviceMetricsOverride", width=width, height=height,
                 deviceScaleFactor=1, mobile=False,
                 screenWidth=width, screenHeight=height)

    def goto(self, url, settle=1.0):
        self.cmd("Page.enable")
        self.cmd("Page.navigate", url=url)
        for _ in range(160):
            try:
                r = self.cmd("Runtime.evaluate", expression="document.readyState",
                             returnByValue=True)
                if r["result"].get("value") == "complete":
                    break
            except Exception:
                pass
            time.sleep(0.25)
        # A metric measured before the webfont swaps is a metric of the fallback
        # face. Montserrat is 16.7% wider than Helvetica, so every measure,
        # every line count and every wrap in this report would be wrong.
        self.cmd("Runtime.evaluate",
                 expression="document.fonts ? document.fonts.ready.then(function(){return 1}) : 1",
                 awaitPromise=True, returnByValue=True)
        time.sleep(settle)

    def evaluate(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True,
                     awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError("page script failed: %s" %
                               json.dumps(r["exceptionDetails"])[:400])
        return r["result"].get("value")

    def shot(self, clip=None):
        p = {"format": "png", "captureBeyondViewport": True}
        if clip:
            p["clip"] = clip
        r = self.cmd("Page.captureScreenshot", **p)
        return base64.b64decode(r["data"])

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass
        try:
            self.proc.terminate()
            self.proc.wait(timeout=5)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


# ------------------------------------------------------------------ png + colour
def png_rgb(blob):
    """Decode an 8-bit non-interlaced PNG to (w, h, channels, bytes).

    Chrome hands back exactly that shape, and zlib is in the standard library,
    so contrast-over-image can sample real pixels without a third-party imaging
    dependency. Returns None for anything this decoder does not cover, and the
    caller then reports nothing rather than guessing a number.
    """
    if blob[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    pos, idat, w, h, depth, ct, interlace = 8, [], 0, 0, 0, 0, 0
    while pos + 8 <= len(blob):
        ln = struct.unpack(">I", blob[pos:pos + 4])[0]
        typ = blob[pos + 4:pos + 8]
        chunk = blob[pos + 8:pos + 8 + ln]
        pos += 12 + ln
        if typ == b"IHDR":
            w, h, depth, ct, _, _, interlace = struct.unpack(">IIBBBBB", chunk)
        elif typ == b"IDAT":
            idat.append(chunk)
        elif typ == b"IEND":
            break
    ch = {0: 1, 2: 3, 4: 2, 6: 4}.get(ct)
    if ch is None or depth != 8 or interlace != 0 or not w or not h:
        return None
    raw = zlib.decompress(b"".join(idat))
    stride = w * ch
    out = bytearray(h * stride)
    prev = bytearray(stride)
    i = 0
    for y in range(h):
        if i >= len(raw):
            break
        f = raw[i]
        i += 1
        line = bytearray(raw[i:i + stride])
        i += stride
        if len(line) < stride:
            break
        if f == 1:
            for x in range(ch, stride):
                line[x] = (line[x] + line[x - ch]) & 255
        elif f == 2:
            for x in range(stride):
                line[x] = (line[x] + prev[x]) & 255
        elif f == 3:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                line[x] = (line[x] + ((a + prev[x]) >> 1)) & 255
        elif f == 4:
            for x in range(stride):
                a = line[x - ch] if x >= ch else 0
                c = prev[x - ch] if x >= ch else 0
                b = prev[x]
                p = a + b - c
                pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                line[x] = (line[x] + pr) & 255
        out[y * stride:(y + 1) * stride] = line
        prev = line
    return w, h, ch, bytes(out)


def parse_color(s):
    if not s:
        return None
    m = re.findall(r"[-\d.]+", s)
    if len(m) < 3:
        return None
    try:
        r, g, b = float(m[0]), float(m[1]), float(m[2])
    except ValueError:
        return None
    a = float(m[3]) if len(m) > 3 else 1.0
    return (r, g, b, a)


def srgb_lum(r, g, b):
    def f(x):
        x = x / 255.0
        return x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def composite(fg, bg):
    """Paint fg over an opaque bg. WCAG ratios are only defined on what is seen."""
    r, g, b, a = fg
    br, bg_, bb = bg[0], bg[1], bg[2]
    return (r * a + br * (1 - a), g * a + bg_ * (1 - a), b * a + bb * (1 - a), 1.0)


def ratio(fg, bg):
    la, lb = srgb_lum(fg[0], fg[1], fg[2]), srgb_lum(bg[0], bg[1], bg[2])
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def text_threshold(fs, fw):
    """WCAG 2.1 1.4.3 · large is 24px, or 18.66px at weight 700 or heavier."""
    try:
        fw = int(fw)
    except (TypeError, ValueError):
        fw = 400
    return 3.0 if (fs >= 24 or (fs >= 18.66 and fw >= 700)) else 4.5


# --------------------------------------------------------------------- capture
COLLECT_JS = r"""
(function(){
  var SX=window.scrollX, SY=window.scrollY;
  var R2=function(n){return Math.round(n*100)/100;};
  var CHAR_BUDGET=60000;

  function pcol(s){var m=s&&s.match(/[-\d.]+/g);if(!m||m.length<3)return null;
    return {r:+m[0],g:+m[1],b:+m[2],a:m[3]===undefined?1:parseFloat(m[3])};}

  function sel(el){
    var parts=[],e=el,d=0;
    while(e&&e.nodeType===1&&d<3){
      var s=e.tagName.toLowerCase();
      if(e.id){parts.unshift(s+'#'+e.id);break;}
      var c=(typeof e.className==='string'?e.className:
             (e.className&&e.className.baseVal)||'').trim();
      if(c) s+='.'+c.split(/\s+/).slice(0,2).join('.');
      var p=e.parentElement;
      if(p){var sib=[].filter.call(p.children,function(k){return k.tagName===e.tagName;});
            if(sib.length>1) s+=':nth-of-type('+(sib.indexOf(e)+1)+')';}
      parts.unshift(s); e=p; d++;
    }
    return parts.join(' > ');}

  // Paint order, approximated by the stacking contexts an element sits inside.
  // Two elements are compared by this list first and by document order second,
  // which is what the painting algorithm reduces to once neither creates a
  // context of its own. That covers the case ink-occlusion cares about: a
  // decoration and a headline that are siblings.
  function zpath(el){
    var p=[],e=el;
    while(e&&e!==document.documentElement){
      var cs=getComputedStyle(e), z=cs.zIndex, pos=cs.position;
      if(pos!=='static'&&z!=='auto') p.unshift(parseInt(z,10)||0);
      else if(parseFloat(cs.opacity)<1||cs.transform!=='none'||cs.filter!=='none'||
              cs.mixBlendMode!=='normal'||cs.isolation==='isolate'||
              (cs.willChange&&cs.willChange.indexOf('transform')>=0)) p.unshift(0);
      e=e.parentElement;
    }
    return p;}

  // An ancestor transform changes the rendered size while leaving the computed
  // font-size untouched, so type-scale and type-floor judge fs times this.
  function accScale(el){
    var s=1,e=el;
    while(e&&e!==document.documentElement){
      var t=getComputedStyle(e).transform;
      if(t&&t!=='none'){
        var m=t.match(/^matrix\(([^)]+)\)$/);
        if(m){var v=m[1].split(',').map(parseFloat);
          s*=Math.sqrt(Math.abs(v[0]*v[3]-v[1]*v[2]))||1;}
        else{var m3=t.match(/^matrix3d\(([^)]+)\)$/);
          if(m3){var v3=m3[1].split(',').map(parseFloat);
            s*=Math.sqrt(Math.abs(v3[0]*v3[5]-v3[1]*v3[4]))||1;}}
      }
      e=e.parentElement;
    }
    return Math.round(s*1000)/1000;}

  function ownTextNodes(el){
    var out=[];
    for(var n=el.firstChild;n;n=n.nextSibling)
      if(n.nodeType===3&&n.textContent.trim()) out.push(n);
    return out;}

  // Per-LINE rects, taken from a Range over the text node. The element rect is
  // one box around every line, so it cannot tell a two-line heading whose
  // second line has dropped onto a caption from one that has not.
  function lineRects(nodes){
    var out=[];
    for(var i=0;i<nodes.length;i++){
      var rg=document.createRange(); rg.selectNodeContents(nodes[i]);
      var rs=rg.getClientRects();
      for(var k=0;k<rs.length;k++){
        var r=rs[k];
        if(r.width<0.5||r.height<0.5) continue;
        out.push([R2(r.left+SX),R2(r.top+SY),R2(r.width),R2(r.height)]);
      }
    }
    return out;}

  // Real characters per line, not width divided by an average advance.
  // Montserrat's caps and figures are far wider than its lowercase, so the
  // arithmetic shortcut fires on every all-caps eyebrow and misses long prose.
  function maxCharsPerLine(nodes){
    var best=0;
    for(var i=0;i<nodes.length;i++){
      var s=nodes[i].textContent, counts={}, rg=document.createRange();
      for(var k=0;k<s.length;k++){
        if(CHAR_BUDGET<=0) return best;
        if(s.charCodeAt(k)===10) continue;
        CHAR_BUDGET--;
        try{ rg.setStart(nodes[i],k); rg.setEnd(nodes[i],k+1); }catch(e){ continue; }
        var r=rg.getBoundingClientRect();
        if(r.width===0&&r.height===0) continue;
        var key=Math.round(r.top);
        counts[key]=(counts[key]||0)+1;
        if(counts[key]>best) best=counts[key];
      }
    }
    return best;}

  var els=[], idx=new Map(), all=document.querySelectorAll('*'), truncated=0;
  var LIMIT=8000;

  // An image or a scrim painted by an absolutely positioned SIBLING is
  // invisible to an ancestor walk, so a headline over a hero photograph would
  // otherwise resolve to the flat band colour underneath it and report a
  // contrast ratio against a ground nobody sees.
  var COVERS=[];
  for(var q=0;q<all.length&&q<LIMIT;q++){
    var o=all[q], ocs=getComputedStyle(o);
    var tag=o.tagName.toLowerCase();
    if((ocs.backgroundImage&&ocs.backgroundImage!=='none')||
       tag==='img'||tag==='svg'||tag==='canvas'||tag==='video'){
      var orr=o.getBoundingClientRect();
      if(orr.width>1&&orr.height>1) COVERS.push({el:o,r:orr});
    }
  }
  function overImage(el,r){
    for(var i=0;i<COVERS.length;i++){
      var o=COVERS[i];
      if(o.el===el||o.el.contains(el)||el.contains(o.el)) continue;
      var q=o.r;
      if(q.left<=r.left+1&&q.top<=r.top+1&&q.right>=r.right-1&&q.bottom>=r.bottom-1) return true;
    }
    return false;}

  // Composite every translucent layer down to an opaque ground, because a
  // ratio taken against rgba(0,0,0,0.4) is a ratio against a colour that is
  // never painted.
  function groundOf(el,r){
    var stack=[],e=el,img=false;
    while(e){
      var cs=getComputedStyle(e);
      if(cs.backgroundImage&&cs.backgroundImage!=='none'){img=true;break;}
      var c=pcol(cs.backgroundColor);
      if(c&&c.a>0){ stack.push(c); if(c.a>=0.999) break; }
      e=e.parentElement;
    }
    if(img) return {kind:'IMAGE'};
    if(!e && overImage(el,r)) return {kind:'IMAGE'};
    if(e===null||stack.length===0||stack[stack.length-1].a<0.999){
      if(overImage(el,r)) return {kind:'IMAGE'};
      stack.push({r:255,g:255,b:255,a:1});
    }
    var out=stack[stack.length-1];
    for(var i=stack.length-2;i>=0;i--){
      var f=stack[i];
      out={r:f.r*f.a+out.r*(1-f.a),g:f.g*f.a+out.g*(1-f.a),
           b:f.b*f.a+out.b*(1-f.a),a:1};
    }
    if(overImage(el,r)) return {kind:'IMAGE'};
    return {kind:'COLOR',c:[R2(out.r),R2(out.g),R2(out.b),1]};}

  var INTER_TAGS={a:1,button:1,input:1,select:1,textarea:1,summary:1,label:1};
  var INTER_ROLES={button:1,link:1,checkbox:1,radio:1,tab:1,'switch':1,menuitem:1,option:1};

  for(var n=0;n<all.length;n++){
    if(n>=LIMIT){ truncated=all.length-LIMIT; break; }
    var el=all[n], cs=getComputedStyle(el);
    if(cs.display==='none') continue;
    var r=el.getBoundingClientRect();
    if(r.width<0.5&&r.height<0.5) continue;
    var tg=el.tagName.toLowerCase();
    if(tg==='script'||tg==='style'||tg==='head'||tg==='meta'||tg==='link'||
       tg==='title'||tg==='noscript') continue;

    var i=els.length;
    idx.set(el,i);
    el.setAttribute('data-uiaudit',String(i));

    var f=function(v){return parseFloat(v)||0;};
    var mt=f(cs.marginTop),mr=f(cs.marginRight),mb=f(cs.marginBottom),ml=f(cs.marginLeft);
    var pt=f(cs.paddingTop),pr=f(cs.paddingRight),pb=f(cs.paddingBottom),pl=f(cs.paddingLeft);
    var bt=f(cs.borderTopWidth),br_=f(cs.borderRightWidth),
        bb=f(cs.borderBottomWidth),bl=f(cs.borderLeftWidth);

    var nodes=ownTextNodes(el);
    var L=nodes.length?lineRects(nodes):[];
    var sbg=pcol(cs.backgroundColor);
    var hasBgImg=!!(cs.backgroundImage&&cs.backgroundImage!=='none');
    var painted=(sbg&&sbg.a>=0.05)||hasBgImg||
                tg==='img'||tg==='svg'||tg==='canvas'||tg==='video';
    var vis=cs.visibility==='visible'&&parseFloat(cs.opacity)>0;

    var pseudo=[];
    ['::before','::after'].forEach(function(w){
      var ps=getComputedStyle(el,w);
      if(!ps||ps.content==='none'||ps.display==='none') return;
      var pw=f(ps.width)+f(ps.paddingLeft)+f(ps.paddingRight)+
             f(ps.borderLeftWidth)+f(ps.borderRightWidth);
      var ph=f(ps.height)+f(ps.paddingTop)+f(ps.paddingBottom)+
             f(ps.borderTopWidth)+f(ps.borderBottomWidth);
      if(pw>0&&ph>0) pseudo.push([R2(pw),R2(ph)]);
    });

    var role=el.getAttribute('role')||'';
    var interactive=(INTER_TAGS[tg]===1&&tg!=='label')||INTER_ROLES[role]===1||
                    (cs.cursor==='pointer'&&(el.onclick||el.hasAttribute('onclick')));
    var blockAnc=null,e2=el.parentElement;
    while(e2){var d2=getComputedStyle(e2).display;
      if(d2!=='inline'&&d2!=='contents'){blockAnc=e2;break;} e2=e2.parentElement;}

    var g=vis?groundOf(el,r):{kind:'HIDDEN'};

    var rec={
      i:i, p:idx.has(el.parentElement)?idx.get(el.parentElement):-1,
      sel:sel(el), tag:tg,
      b:[R2(r.left+SX),R2(r.top+SY),R2(r.width),R2(r.height)],
      m:[R2(r.left+SX-ml),R2(r.top+SY-mt),R2(r.width+ml+mr),R2(r.height+mt+mb)],
      pad:[R2(r.left+SX+bl),R2(r.top+SY+bt),
           R2(Math.max(0,r.width-bl-br_)),R2(Math.max(0,r.height-bt-bb))],
      disp:cs.display, pos:cs.position, z:zpath(el),
      tf:cs.transform!=='none', op:R2(parseFloat(cs.opacity)),
      pe:cs.pointerEvents, mbl:cs.mixBlendMode,
      vis:vis, ah:el.getAttribute('aria-hidden')==='true',
      dis:el.disabled===true||el.hasAttribute('disabled')||
          el.getAttribute('aria-disabled')==='true',
      sp:[mt,mr,mb,ml,pt,pr,pb,pl,f(cs.rowGap),f(cs.columnGap)],
      gapAuto:[cs.rowGap,cs.columnGap],
      bwd:[bt,br_,bb,bl],
      bcl:[cs.borderTopColor,cs.borderRightColor,cs.borderBottomColor,cs.borderLeftColor],
      bsty:[cs.borderTopStyle,cs.borderRightStyle,cs.borderBottomStyle,cs.borderLeftStyle],
      bsh:cs.boxShadow, sbg:cs.backgroundColor, bgi:hasBgImg, paint:painted,
      ovx:cs.overflowX, ovy:cs.overflowY,
      sw:el.scrollWidth, sh:el.scrollHeight, cw:el.clientWidth, ch:el.clientHeight,
      mh:cs.maxHeight, mw:cs.maxWidth, hgt:cs.height,
      teo:cs.textOverflow, ws:cs.whiteSpace, clamp:cs.webkitLineClamp||'none',
      inl:cs.display==='inline'||cs.display.indexOf('inline-')===0||cs.display==='contents',
      ifc:blockAnc&&idx.has(blockAnc)?idx.get(blockAnc):-1,
      ga:cs.gridArea, ps:pseudo, inter:!!interactive, role:role, cur:cs.cursor,
      sig:tg+'|'+((typeof el.className==='string'?el.className:'')||'').trim(),
      gk:g.kind, gc:g.kind==='COLOR'?g.c:null
    };
    if(nodes.length){
      rec.own=nodes.map(function(x){return x.textContent.trim();})
                   .join(' ').replace(/\s+/g,' ').slice(0,120);
      rec.L=L;
      rec.fs=R2(parseFloat(cs.fontSize));
      rec.fw=cs.fontWeight;
      rec.ls=R2(parseFloat(cs.letterSpacing)||0);
      rec.lh=cs.lineHeight==='normal'?R2(parseFloat(cs.fontSize)*1.219):R2(parseFloat(cs.lineHeight));
      rec.ff=cs.fontFamily.split(',')[0].replace(/["']/g,'');
      rec.tt=cs.textTransform;
      rec.col=cs.color;
      rec.tsh=cs.textShadow!=='none';
      rec.sro=(r.width<=1.5||r.height<=1.5)||
              cs.clipPath==='inset(50%)'||(cs.clip||'').replace(/\s/g,'')==='rect(0px,0px,0px,0px)';
      rec.mcl=(L.length>=2)?maxCharsPerLine(nodes):0;
      rec.scl=accScale(el);
      rec.fchk=(function(){try{return document.fonts.check(cs.fontWeight+' '+
        cs.fontSize+' '+cs.fontFamily);}catch(e){return null;}})();
    }
    els.push(rec);
  }

  var de=document.documentElement;
  return JSON.stringify({
    w:window.innerWidth, h:window.innerHeight,
    docW:de.scrollWidth, docH:de.scrollHeight,
    root:parseFloat(getComputedStyle(de).fontSize),
    url:location.href, truncated:truncated, els:els
  });
})()
"""

LADDER_JS = r"""
(function(){
  var src=__SRC__;
  var probe=document.createElement('div');
  probe.style.cssText='position:absolute;left:-99999px;top:0;visibility:hidden;margin:0;padding:0';
  document.body.appendChild(probe);
  var house={},page={},rs=getComputedStyle(document.documentElement);
  for(var k in src){
    probe.style.fontSize=src[k];
    house[k]=Math.round(parseFloat(getComputedStyle(probe).fontSize)*100)/100;
    var v=rs.getPropertyValue('--fs-'+k).trim();
    if(v){ probe.style.fontSize=v;
      page[k]=Math.round(parseFloat(getComputedStyle(probe).fontSize)*100)/100; }
  }
  probe.parentNode.removeChild(probe);
  return JSON.stringify({house:house,page:page,root:parseFloat(rs.fontSize)});
})()
"""

# At rest means two rests: the top of the document and the bottom of it. A
# sticky footer only covers the last row of a table once you are at the bottom.
BOTTOM_JS = r"""
(function(){
  window.scrollTo(0, document.documentElement.scrollHeight);
  var SX=window.scrollX, SY=window.scrollY, out={bars:[],boxes:[],sy:SY};
  var R2=function(n){return Math.round(n*100)/100;};
  function pcol(s){var m=s&&s.match(/[-\d.]+/g);if(!m||m.length<3)return null;
    return {a:m[3]===undefined?1:parseFloat(m[3])};}
  var all=document.querySelectorAll('*');
  for(var i=0;i<all.length&&i<8000;i++){
    var el=all[i],cs=getComputedStyle(el);
    if(cs.display==='none'||cs.visibility!=='visible') continue;
    var r=el.getBoundingClientRect();
    if(r.width<1||r.height<1) continue;
    var id=el.getAttribute('data-uiaudit');
    if(cs.position==='fixed'||cs.position==='sticky'){
      var c=pcol(cs.backgroundColor);
      var opaque=(c&&c.a>=0.5)||(cs.backgroundImage&&cs.backgroundImage!=='none');
      var off=(r.bottom<=0)||(r.top>=window.innerHeight)||(r.right<=0)||(r.left>=window.innerWidth);
      if(opaque&&!off) out.bars.push({id:id,sel:el.tagName.toLowerCase()+
        ((typeof el.className==='string'&&el.className)?'.'+el.className.trim().split(/\s+/)[0]:''),
        r:[R2(r.left),R2(r.top),R2(r.width),R2(r.height)],pos:cs.position});
      continue;
    }
    var own=false;
    for(var nn=el.firstChild;nn;nn=nn.nextSibling)
      if(nn.nodeType===3&&nn.textContent.trim()){own=true;break;}
    var tg=el.tagName.toLowerCase();
    var act=tg==='a'||tg==='button'||tg==='input'||tg==='select'||tg==='textarea';
    if(!own&&!act) continue;
    out.boxes.push({id:id,sel:el.tagName.toLowerCase(),
      r:[R2(r.left),R2(r.top),R2(r.width),R2(r.height)],act:act,
      t:(el.textContent||'').trim().slice(0,60)});
  }
  return JSON.stringify(out);
})()
"""


# ------------------------------------------------------------------- geometry
def isect(a, b):
    """Intersection of two [x, y, w, h] boxes, or None."""
    x = max(a[0], b[0])
    y = max(a[1], b[1])
    r = min(a[0] + a[2], b[0] + b[2])
    d = min(a[1] + a[3], b[1] + b[3])
    if r <= x or d <= y:
        return None
    return [x, y, r - x, d - y]


def area(r):
    return r[2] * r[3]


def union(boxes):
    x = min(b[0] for b in boxes)
    y = min(b[1] for b in boxes)
    r = max(b[0] + b[2] for b in boxes)
    d = max(b[1] + b[3] for b in boxes)
    return [x, y, r - x, d - y]


def is_anc(recs, a, b):
    """True when element index a is an ancestor of element index b.

    An ancestor containing a descendant is not an overlap. Every pairwise check
    in this file goes through here first, because that single confusion is what
    makes a geometry linter cry wolf until nobody runs it.
    """
    if a == b:
        return False
    p = recs[b]["p"]
    guard = 0
    while p >= 0 and guard < 512:
        if p == a:
            return True
        p = recs[p]["p"]
        guard += 1
    return False


def related(recs, a, b):
    return is_anc(recs, a, b) or is_anc(recs, b, a)


def paint_above(a, b):
    """True when element a paints on top of element b."""
    za, zb = a["z"], b["z"]
    for k in range(min(len(za), len(zb))):
        if za[k] != zb[k]:
            return za[k] > zb[k]
    if len(za) != len(zb):
        return len(za) > len(zb)
    return a["i"] > b["i"]


def same_ifc(a, b):
    """Two inline boxes in one inline formatting context share a row by design."""
    return (a["inl"] or b["inl"]) and a["ifc"] == b["ifc"] and a["ifc"] >= 0


def visible_text(r):
    return ("L" in r and r["L"] and r["vis"] and not r.get("sro")
            and r["op"] > 0.05)


def has_ink(r):
    if r.get("own"):
        return True
    c = parse_color(r["sbg"])
    if c and c[3] >= 0.05:
        return True
    if r["bgi"] or r["tag"] in ("img", "svg", "canvas", "video"):
        return True
    return any(w > 0 and s not in ("none", "hidden")
               for w, s in zip(r["bwd"], r["bsty"]))


def band_pairs(items, key_top, key_bot, band=64):
    """Yield candidate pairs without an n-squared sweep of the whole page."""
    buckets = {}
    for it in items:
        lo = int(key_top(it) // band)
        hi = int(key_bot(it) // band)
        for k in range(lo, hi + 1):
            buckets.setdefault(k, []).append(it)
    seen = set()
    for k in sorted(buckets):
        arr = buckets[k]
        for i in range(len(arr)):
            for j in range(i + 1, len(arr)):
                a, b = arr[i], arr[j]
                tag = (id(a), id(b))
                if tag in seen:
                    continue
                seen.add(tag)
                yield a, b


def fmt_box(b):
    return "%gx%g at %g,%g" % (round(b[2], 1), round(b[3], 1),
                               round(b[0], 1), round(b[1], 1))


def nearest_step(v, ladder):
    return min(ladder, key=lambda s: abs(s - v))


class Ctx(object):
    def __init__(self, page, width, height, ladder, opts, media="screen"):
        self.page = page
        self.recs = page["els"]
        self.width = width
        self.height = height
        self.ladder = ladder
        self.opts = opts
        self.media = media
        self.occluded = set()
        self.bottom = None


def find(ctx, check, sev, rec, detail, rule, **extra):
    f = {
        "check": check,
        "severity": sev,
        "width": ctx.width,
        "selector": rec["sel"] if rec else "-",
        "box": [round(v, 1) for v in rec["b"]] if rec else None,
        "detail": detail,
        "rule": rule,
    }
    if ctx.media != "screen":
        f["media"] = ctx.media
    if rec and rec.get("own"):
        f["text"] = rec["own"][:70]
    f.update(extra)
    return f


# --------------------------------------------------------------------- checks
def check_line_box_collision(ctx):
    """Two rendered text lines from different elements sitting on each other."""
    recs = ctx.recs
    lines = []
    for r in recs:
        if not visible_text(r):
            continue
        for ln in r["L"]:
            lines.append({"r": ln, "e": r})
    out, pairs = [], {}
    for a, b in band_pairs(lines, lambda x: x["r"][1], lambda x: x["r"][1] + x["r"][3]):
        ra, rb = a["e"], b["e"]
        if ra["i"] == rb["i"] or related(recs, ra["i"], rb["i"]) or same_ifc(ra, rb):
            continue
        it = isect(a["r"], b["r"])
        if not it:
            continue
        # A line rect is a line-height box, not a glyph box. Two columns set on
        # tight leading share a fifth of their boxes with clear air between the
        # glyphs, which is why the vertical floor is a quarter and not a sliver.
        if it[2] <= 2:
            continue
        floor = 0.25 * min(a["r"][3], b["r"][3])
        if it[3] <= floor:
            continue
        key = tuple(sorted((ra["i"], rb["i"])))
        if key not in pairs or it[3] > pairs[key][2][3]:
            pairs[key] = (ra, rb, it, a["r"], b["r"])
    for ra, rb, it, la, lb in pairs.values():
        out.append(find(
            ctx, "line-box-collision", "error", ra,
            "line %s overlaps %s line %s by %.1fpx horizontally and %.1fpx vertically"
            % (fmt_box(la), rb["sel"], fmt_box(lb), it[2], it[3]),
            "two text lines from different elements may not intersect by more than "
            "2px horizontally and 25% of the shorter line box vertically",
            other=rb["sel"], otherText=rb.get("own", "")[:70],
            overlapPx=[round(it[2], 1), round(it[3], 1)]))
    return out


def check_ink_occlusion(ctx):
    """A graphic or filled panel painted on top of text."""
    recs = ctx.recs
    texts = [r for r in recs if visible_text(r)]
    painted = []
    for r in recs:
        if not r["paint"] or not r["vis"] or r["op"] <= 0.05:
            continue
        # A fixed or sticky bar over content is the same picture but a
        # different defect, and under-fixed-chrome reports it with the right
        # rule and the right at-rest qualification.
        if r["pos"] in ("fixed", "sticky"):
            continue
        painted.append(r)
    out = []
    for t in texts:
        tbox = union(t["L"])
        for p in painted:
            if p["i"] == t["i"] or related(recs, p["i"], t["i"]):
                continue
            if p["pe"] == "none" and p["op"] < 0.35:
                continue
            if not paint_above(p, t):
                continue
            it = isect(p["b"], tbox)
            if not it:
                continue
            covered = sum(area(x) for x in
                          (isect(p["b"], ln) for ln in t["L"]) if x)
            ta = sum(area(ln) for ln in t["L"]) or 1.0
            frac = covered / ta
            deep = any(x and x[2] > 2 and x[3] > 2
                       for x in (isect(p["b"], ln) for ln in t["L"]))
            if frac <= 0.05 and not deep:
                continue
            c = parse_color(p["sbg"])
            opaque = (c is not None and c[3] >= 0.9) or p["bgi"] or \
                p["tag"] in ("img", "svg", "canvas", "video")
            sev = "blocker" if opaque else "error"
            if frac > 0.9:
                ctx.occluded.add(t["i"])
            out.append(find(
                ctx, "ink-occlusion", sev, t,
                "%s (%s, %s) is painted above this text and covers %.0f%% of it"
                % (p["sel"], p["tag"], p["sbg"] if not p["bgi"] else "background-image",
                   frac * 100),
                "no element painted above a text node may cover more than 5% of it, "
                "or reach more than 2px into a line box",
                cover=p["sel"], coverBox=[round(v, 1) for v in p["b"]],
                coveredPct=round(frac * 100, 1)))
            break
    return out


def hairline_strips(recs):
    """A rule, a divider, an underline bar, a single border edge."""
    strips = []
    for r in recs:
        if not r["vis"] or r["op"] <= 0.05:
            continue
        x, y, w, h = r["b"]
        if w < 0.5 or h < 0.5:
            continue
        if min(w, h) <= 4 and max(w, h) >= 24 and has_ink(r) and not r.get("own"):
            col = r["sbg"]
            cc = parse_color(col)
            if cc is None or cc[3] < 0.05:
                for bw, bc, bs in zip(r["bwd"], r["bcl"], r["bsty"]):
                    if bw > 0 and bs not in ("none", "hidden"):
                        col = bc
                        break
            strips.append((r, [x, y, w, h], col))
            continue
        if r.get("own"):
            continue
        sides = [k for k in range(4)
                 if r["bwd"][k] > 0 and r["bsty"][k] not in ("none", "hidden")]
        if len(sides) != 1:
            continue
        k = sides[0]
        t = max(r["bwd"][k], 1.0)
        # Only the drawn edge, never the whole box. A section with one
        # border-bottom would otherwise be reported as crossing every word
        # inside it.
        band = {0: [x, y, w, t], 1: [x + w - t, y, t, h],
                2: [x, y + h - t, w, t], 3: [x, y, t, h]}[k]
        strips.append((r, band, r["bcl"][k]))
    return strips


def check_hairline_crosses_text(ctx):
    """A rule or border running through a line of type or through a logo."""
    recs = ctx.recs
    strips = hairline_strips(recs)
    if not strips:
        return []
    targets = []
    for r in recs:
        if visible_text(r):
            for ln in r["L"]:
                targets.append((r, ln, "text", r["col"]))
        if r["tag"] in ("img", "svg") and r["vis"] and r["b"][2] > 4 and r["b"][3] > 4:
            targets.append((r, r["b"], "graphic", None))
    out, seen = [], set()
    for hr, band, col in strips:
        for tr, box, kind, tcol in targets:
            if hr["i"] == tr["i"] or related(recs, hr["i"], tr["i"]):
                continue
            # A strikethrough or an underline drawn as a bar is deliberate, and
            # its signature is that it is painted in the colour of the text.
            if tcol and col and parse_color(col) and parse_color(tcol) and \
                    [round(v) for v in parse_color(col)[:3]] == \
                    [round(v) for v in parse_color(tcol)[:3]]:
                continue
            it = isect(band, box)
            if not it or it[2] <= 0.1 or it[3] <= 0.1:
                continue
            key = (hr["i"], tr["i"])
            if key in seen:
                continue
            seen.add(key)
            out.append(find(
                ctx, "hairline-crosses-text", "error", tr,
                "%s (%s, %s) crosses this %s by %.1fpx"
                % (hr["sel"], fmt_box(band), col or "no colour", kind,
                   min(it[2], it[3])),
                "a rule, divider or single border edge may not intersect a text "
                "line box or an img or svg box at all",
                hairline=hr["sel"], hairlineBox=[round(v, 1) for v in band],
                depthPx=round(min(it[2], it[3]), 1)))
    return out


def check_flow_box_overlap(ctx):
    """Two in-flow siblings whose boxes intersect."""
    recs = ctx.recs
    cand = [r for r in recs
            if r["pos"] in ("static", "relative") and not r["tf"]
            and r["vis"] and not r.get("sro") and r["b"][2] > 0.5 and r["b"][3] > 0.5]
    out, seen = [], set()
    for a, b in band_pairs(cand, lambda x: x["b"][1], lambda x: x["b"][1] + x["b"][3]):
        if related(recs, a["i"], b["i"]) or same_ifc(a, b):
            continue
        if not (has_ink(a) or has_ink(b)):
            continue
        if a["p"] == b["p"] and a["p"] >= 0:
            par = recs[a["p"]]
            # Two grid items on the same named area are stacked on purpose.
            if par["disp"] in ("grid", "inline-grid") and a["ga"] == b["ga"] \
                    and a["ga"] not in ("auto / auto / auto / auto", "auto"):
                continue
            xo = isect([a["b"][0], 0, a["b"][2], 1], [b["b"][0], 0, b["b"][2], 1])
            column = not (xo and xo[2] > 0.5 * min(a["b"][2], b["b"][2]))
            # Adjacent vertical margins collapse, so a margin-box comparison of
            # two stacked blocks reports the shared margin as an overlap that
            # is both large and invisible.
            boxes = ("m", "m") if (column and not a["inl"] and not b["inl"]) else ("b", "b")
        else:
            boxes = ("b", "b")
        it = isect(a[boxes[0]], b[boxes[1]])
        if not it or area(it) <= 4:
            continue
        if area(it) < 0.05 * min(area(a[boxes[0]]), area(b[boxes[1]])):
            continue
        key = tuple(sorted((a["i"], b["i"])))
        if key in seen:
            continue
        seen.add(key)
        out.append(find(
            ctx, "flow-box-overlap", "warning", a,
            "%s box %s intersects %s box %s over %.0f square px"
            % ("margin" if boxes[0] == "m" else "border", fmt_box(a[boxes[0]]),
               b["sel"], fmt_box(b[boxes[1]]), area(it)),
            "two in-flow elements where neither contains the other may not "
            "intersect by more than 4 square px and 5% of the smaller box",
            other=b["sel"], overlapArea=round(area(it), 1)))
    return out


def check_text_clipped(ctx):
    """Text cut off by its own box."""
    out = []
    for r in ctx.recs:
        if not visible_text(r):
            continue
        ell = r["teo"] == "ellipsis" and r["ws"] in ("nowrap", "pre")
        clamped = r["clamp"] not in ("none", "", None)
        dx, dy = r["sw"] - r["cw"], r["sh"] - r["ch"]
        if dx > 1 and r["ovx"] in ("hidden", "clip") and not ell:
            out.append(find(
                ctx, "text-clipped", "error", r,
                "scrollWidth %d exceeds clientWidth %d by %dpx with overflow-x %s"
                % (r["sw"], r["cw"], dx, r["ovx"]),
                "text may not be cut off by overflow hidden or clip without "
                "text-overflow ellipsis or -webkit-line-clamp",
                overflowPx=dx, axis="x"))
            continue
        if dy > 1 and r["ovy"] in ("hidden", "clip") and not clamped:
            out.append(find(
                ctx, "text-clipped", "error", r,
                "scrollHeight %d exceeds clientHeight %d by %dpx with overflow-y %s"
                % (r["sh"], r["ch"], dy, r["ovy"]),
                "text may not be cut off by overflow hidden or clip without "
                "text-overflow ellipsis or -webkit-line-clamp",
                overflowPx=dy, axis="y"))
            continue
        # A fixed height can shave the descenders off the last line without
        # ever producing a scroll delta, so the line count is measured against
        # the box independently. Only boxes that are actually constrained are
        # judged, or an auto-height paragraph reports its own rounding.
        # A nowrap box has one line by definition, so a multi-rect Range result
        # there is an artefact of the clip and not a shaved last line.
        constrained = r["ovy"] in ("hidden", "clip") or r["mh"] != "none"
        if r["ws"] in ("nowrap", "pre") or ell:
            constrained = False
        if constrained and not clamped and r["L"] and r["lh"] > 0:
            need = len(r["L"]) * r["lh"]
            if need - r["ch"] > 1:
                out.append(find(
                    ctx, "text-clipped", "error", r,
                    "%d lines at %.2fpx line-height need %.1fpx, clientHeight is %d"
                    % (len(r["L"]), r["lh"], need, r["ch"]),
                    "a constrained box must be tall enough for the lines it renders",
                    overflowPx=round(need - r["ch"], 1), axis="y"))
    return out


def frame_of(recs, i):
    """Nearest ancestor that is supposed to hold this element in."""
    p = recs[i]["p"]
    guard = 0
    while p >= 0 and guard < 512:
        f = recs[p]
        if f["ovx"] in ("hidden", "clip", "auto", "scroll") or \
           f["ovy"] in ("hidden", "clip", "auto", "scroll") or f["mh"] != "none":
            return f
        p = f["p"]
        guard += 1
    return None


def check_past_frame(ctx):
    """Content escaping the box that is supposed to hold it."""
    recs = ctx.recs
    over = {}
    for r in recs:
        if not r["vis"] or r.get("sro") or r["pos"] == "fixed":
            continue
        f = frame_of(recs, r["i"])
        if f is None:
            continue
        if r["pos"] == "sticky" and (f["ovy"] in ("auto", "scroll")
                                     or f["ovx"] in ("auto", "scroll")):
            continue
        fx, fy, fw, fh = f["pad"]
        x, y, w, h = r["b"]
        sides = {}
        # A scroller is not a clipper. Report it only when the scroll it holds
        # is more than a viewport deep, which means nobody meant to scroll it.
        scroll_x = f["ovx"] in ("auto", "scroll") and (f["sw"] - f["cw"]) <= ctx.width
        scroll_y = f["ovy"] in ("auto", "scroll") and (f["sh"] - f["ch"]) <= ctx.height
        if not scroll_y and y < fy - 1:
            sides["top"] = round(fy - y, 1)
        if not scroll_y and y + h > fy + fh + 1:
            sides["bottom"] = round(y + h - fy - fh, 1)
        if not scroll_x and x < fx - 1:
            sides["left"] = round(fx - x, 1)
        if not scroll_x and x + w > fx + fw + 1:
            sides["right"] = round(x + w - fx - fw, 1)
        if sides:
            over[r["i"]] = (r, f, sides)
    out = []
    for i, (r, f, sides) in over.items():
        # Report the outermost escaping element only. When a container spills,
        # every word inside it spills too, and one finding is the fix.
        p = r["p"]
        if p in over and set(over[p][2]) & set(sides) and over[p][1]["i"] == f["i"]:
            continue
        out.append(find(
            ctx, "past-frame", "error", r,
            "escapes %s (frame %s) by %s"
            % (f["sel"], fmt_box(f["pad"]),
               ", ".join("%s %gpx" % (k, v) for k, v in sorted(sides.items()))),
            "a descendant border box may not exceed its frame content box by "
            "more than 1px on any side",
            frame=f["sel"], sides=sides,
            frameOverflow=[max(0, f["sw"] - f["cw"]), max(0, f["sh"] - f["ch"])]))
    return out


def check_doc_overflow_x(ctx):
    """The page scrolls sideways."""
    recs = ctx.recs
    delta = ctx.page["docW"] - ctx.page["w"]
    if delta <= 1:
        return []
    lim = ctx.page["w"] + 1
    offenders = []
    for r in recs:
        if not r["vis"] or r["b"][2] < 1:
            continue
        right = r["b"][0] + r["b"][2]
        if right <= lim:
            continue
        p = r["p"]
        if p >= 0 and recs[p]["b"][0] + recs[p]["b"][2] > lim:
            continue
        # A carousel or a marquee overflows on purpose, inside a scroller.
        anc, guard, inside = p, 0, False
        while anc >= 0 and guard < 512:
            if recs[anc]["ovx"] in ("auto", "scroll"):
                inside = True
                break
            anc = recs[anc]["p"]
            guard += 1
        if inside:
            continue
        offenders.append((r, right - ctx.page["w"]))
    out = [find(
        ctx, "doc-overflow-x", "error", None,
        "documentElement.scrollWidth %d exceeds innerWidth %d by %dpx"
        % (ctx.page["docW"], ctx.page["w"], delta),
        "the document may not scroll sideways at any pass width",
        overflowPx=delta,
        offenders=[o[0]["sel"] for o in offenders[:8]])]
    for r, px in sorted(offenders, key=lambda o: -o[1])[:8]:
        out.append(find(
            ctx, "doc-overflow-x", "error", r,
            "right edge %.1f is %.1fpx past innerWidth %d while its parent is not"
            % (r["b"][0] + r["b"][2], px, ctx.page["w"]),
            "the element that introduces the sideways scroll",
            overflowPx=round(px, 1)))
    return out


def check_under_fixed_chrome(ctx):
    """Content sitting under a fixed bar at rest."""
    recs = ctx.recs
    out = []
    bars = []
    for r in recs:
        if r["pos"] not in ("fixed", "sticky") or not r["vis"]:
            continue
        c = parse_color(r["sbg"])
        if not ((c and c[3] >= 0.5) or r["bgi"]):
            continue
        x, y, w, h = r["b"]
        # A hide-on-scroll header parks itself off screen with a transform.
        if y + h <= 0 or y >= ctx.height or x + w <= 0 or x >= ctx.width:
            continue
        bars.append(r)
    for bar in bars:
        # At scroll 0 a sticky element is still in flow and content has not
        # reached it yet, so only a fixed bar can be covering anything.
        if bar["pos"] != "fixed":
            continue
        for r in recs:
            if not r["vis"] or related(recs, bar["i"], r["i"]) or r["i"] == bar["i"]:
                continue
            if not (r.get("own") or r["inter"]):
                continue
            if r["pos"] in ("fixed", "sticky"):
                continue
            box = union(r["L"]) if r.get("L") else r["b"]
            it = isect(bar["b"], box)
            if not it or it[2] < 2 or it[3] < 2:
                continue
            out.append(find(
                ctx, "under-fixed-chrome", "warning", r,
                "sits under fixed bar %s (%s) at scroll 0, overlap %s"
                % (bar["sel"], fmt_box(bar["b"]), fmt_box(it)),
                "no text or interactive box may sit under an opaque fixed or "
                "sticky bar in a resting scroll position",
                bar=bar["sel"], state="top"))
            break
    b = ctx.bottom
    if b:
        for bar in b["bars"]:
            for box in b["boxes"]:
                if box["id"] is not None and bar["id"] is not None:
                    bi, xi = int(bar["id"]), int(box["id"])
                    if bi == xi or is_anc(recs, bi, xi):
                        continue
                it = isect(bar["r"], box["r"])
                if not it or it[2] < 2 or it[3] < 2:
                    continue
                rec = recs[int(box["id"])] if box["id"] is not None else None
                out.append(find(
                    ctx, "under-fixed-chrome", "warning", rec,
                    "sits under %s bar %s at the bottom of the document, overlap %s"
                    % (bar["pos"], bar["sel"], fmt_box(it)),
                    "no text or interactive box may sit under an opaque fixed or "
                    "sticky bar in a resting scroll position",
                    bar=bar["sel"], state="bottom", scrollY=b["sy"]))
                break
    return out


SPACE_PROPS = ["margin-top", "margin-right", "margin-bottom", "margin-left",
               "padding-top", "padding-right", "padding-bottom", "padding-left",
               "row-gap", "column-gap"]


def check_spacing_off_4(ctx, other):
    """Space that is not a multiple of 4px. House rule 12."""
    if other is None:
        return [{
            "check": "spacing-off-4", "severity": "note", "width": ctx.width,
            "selector": "-", "box": None,
            "detail": "skipped · isolating static space from fluid clamp space "
                      "needs two pass widths and only one was run",
            "rule": "run at 768 and 1440, or wider, to enable this check"}]
    a_by_i = {r["i"]: r for r in ctx.recs}
    b_by_i = {r["i"]: r for r in other.recs}
    root = ctx.page.get("root", 16)
    out = []
    for i, ra in a_by_i.items():
        rb = b_by_i.get(i)
        if rb is None or rb["sel"] != ra["sel"]:
            continue
        for k, prop in enumerate(SPACE_PROPS):
            va, vb = round(ra["sp"][k], 2), round(rb["sp"][k], 2)
            if va == 0:
                continue
            # Fluid space is off the grid at every width but its endpoints, and
            # is deliberate. A value identical at both passes is a static one.
            if abs(va - vb) > 0.01:
                continue
            if k >= 8 and ra["gapAuto"][k - 8] in ("normal", ""):
                continue
            m = va % 4
            if not (0.5 < m < 3.5):
                continue
            step = nearest_step(va, SPACE_LADDER)
            sev = "warning"
            detail = "%s is %gpx, off the 4px grid · nearest step %dpx" % (prop, va, step)
            if abs(root - 16) > 0.01:
                sev = "note"
                detail += " · root font-size is %gpx, so a rem source lands off " \
                          "grid legitimately" % root
            out.append(find(ctx, "spacing-off-4", sev, ra, detail,
                            "every margin, padding and gap is a multiple of 4px · "
                            "house rule 12",
                            property=prop, value=va, nearest=step))
    return out


def check_contrast_solid(ctx):
    """Text below WCAG 2.1 1.4.3 against a solid ground."""
    out = []
    for r in ctx.recs:
        if not visible_text(r) or r["gk"] != "COLOR" or r["ah"] or r["dis"]:
            continue
        if r["i"] in ctx.occluded:
            continue
        fg = parse_color(r["col"])
        if not fg or not r["gc"]:
            continue
        gnd = tuple(r["gc"])
        if fg[3] < 1.0:
            fg = composite(fg, gnd)
        v = ratio(fg, gnd)
        need = text_threshold(r["fs"], r["fw"])
        if v >= need:
            continue
        out.append(find(
            ctx, "contrast-solid", "error", r,
            "%s on rgb(%d, %d, %d) is %.2f:1, below %.1f:1 for %gpx weight %s"
            % (r["col"], round(gnd[0]), round(gnd[1]), round(gnd[2]), v, need,
               r["fs"], r["fw"]),
            "WCAG 2.1 1.4.3 · 3.0:1 at 24px or at 18.66px weight 700, "
            "4.5:1 everywhere else",
            contrast=v, required=need))
    return out


def check_contrast_over_image(ctx, chrome):
    """Text over a photograph or a gradient, sampled from real pixels."""
    if chrome is None:
        return []
    cands = [r for r in ctx.recs
             if visible_text(r) and r["gk"] == "IMAGE" and not r["ah"]
             and r["i"] not in ctx.occluded]
    cands.sort(key=lambda r: -(r["fs"] * len(r["L"])))
    cap = ctx.opts.image_samples
    out = []
    for r in cands[:cap]:
        fg = parse_color(r["col"])
        if not fg:
            continue
        box = union(r["L"])
        if box[2] < 2 or box[3] < 2:
            continue
        sel = '[data-uiaudit="%d"]' % r["i"]
        # Sampling the first render samples the glyphs, which reports the text
        # against its own colour: a ratio of 1.0 and a false blocker on every
        # node. The node is hidden before the ground is sampled.
        try:
            chrome.evaluate(
                "(function(){var e=document.querySelector('%s');"
                "e.setAttribute('data-uiaudit-vis', e.style.visibility||'');"
                "e.style.visibility='hidden';return 1})()" % sel)
            blob = chrome.shot({"x": box[0], "y": box[1], "width": box[2],
                                "height": box[3], "scale": 1})
        finally:
            chrome.evaluate(
                "(function(){var e=document.querySelector('%s');"
                "e.style.visibility=e.getAttribute('data-uiaudit-vis')||'';"
                "e.removeAttribute('data-uiaudit-vis');return 1})()" % sel)
        px = png_rgb(blob)
        if not px:
            continue
        w, h, ch, buf = px
        step = max(1, int(((w * h) / 2000.0) ** 0.5))
        ratios = []
        for y in range(0, h, step):
            for x in range(0, w, step):
                o = (y * w + x) * ch
                if ch >= 3:
                    pr, pg, pb = buf[o], buf[o + 1], buf[o + 2]
                else:
                    pr = pg = pb = buf[o]
                gnd = (pr, pg, pb, 1.0)
                f = composite(fg, gnd) if fg[3] < 1.0 else fg
                ratios.append(ratio(f, gnd))
        if not ratios:
            continue
        ratios.sort()
        v = ratios[int(0.05 * (len(ratios) - 1))]
        need = text_threshold(r["fs"], r["fw"])
        if v >= need:
            continue
        # A text-shadow or a paint-order stroke keeps type legible over a busy
        # image while the pixel maths says it fails.
        sev = "note" if r["tsh"] else "warning"
        out.append(find(
            ctx, "contrast-over-image", sev, r,
            "%s over an image ground is %.2f:1 at the 5th percentile of %d sampled "
            "pixels, below %.1f:1%s"
            % (r["col"], v, len(ratios), need,
               " · text-shadow is set, so this is a warning not a failure"
               if r["tsh"] else ""),
            "WCAG 2.1 1.4.3 applies over an image ground too, judged against the "
            "worst part of the image the text sits on",
            contrast=v, required=need, samples=len(ratios)))
    return out


CONTROL_TAGS = ("input", "select", "textarea", "button")
CONTROL_ROLES = ("button", "checkbox", "radio", "switch")


def check_contrast_nontext(ctx):
    """A UI boundary below WCAG 2.1 1.4.11."""
    recs = ctx.recs
    out = []
    for r in recs:
        if not r["vis"] or r["dis"] or r["ah"]:
            continue
        if r["tag"] not in CONTROL_TAGS and r["role"] not in CONTROL_ROLES:
            continue
        if r["p"] < 0 or not recs[r["p"]].get("gc"):
            continue
        outer = tuple(recs[r["p"]]["gc"])
        best, how = 0.0, "none"
        fill = parse_color(r["sbg"])
        if fill and fill[3] > 0:
            v = ratio(composite(fill, outer) if fill[3] < 1 else fill, outer)
            if v > best:
                best, how = v, "fill %s" % r["sbg"]
        for bw, bc, bs in zip(r["bwd"], r["bcl"], r["bsty"]):
            if bw <= 0 or bs in ("none", "hidden"):
                continue
            c = parse_color(bc)
            if not c:
                continue
            v = ratio(composite(c, outer) if c[3] < 1 else c, outer)
            if v > best:
                best, how = v, "border %s" % bc
        # A boundary drawn entirely by a box-shadow looks border-less to
        # computed style, so its colour is read too.
        if r["bsh"] and r["bsh"] != "none":
            c = parse_color(r["bsh"])
            if c:
                v = ratio(composite(c, outer) if c[3] < 1 else c, outer)
                if v > best:
                    best, how = v, "box-shadow"
        if best >= 3.0:
            continue
        out.append(find(
            ctx, "contrast-nontext", "warning", r,
            "control boundary is %.2f:1 against rgb(%d, %d, %d) · best edge is %s"
            % (best, round(outer[0]), round(outer[1]), round(outer[2]), how),
            "WCAG 2.1 1.4.11 · a control needs 3.0:1 from its border, its fill "
            "or its shadow against the ground around it",
            contrast=round(best, 2), required=3.0))
    return out


def check_touch_target(ctx):
    """An interactive box under 44px."""
    recs = ctx.recs
    out = []
    sev = "error" if ctx.width < 768 else "warning"
    for r in recs:
        if not r["inter"] or not r["vis"] or r.get("sro"):
            continue
        anc, guard, skip = r["p"], 0, False
        while anc >= 0 and guard < 512:
            a = recs[anc]
            if a["inter"] or a["tag"] == "label":
                skip = True
                break
            anc = a["p"]
            guard += 1
        if skip:
            continue
        # WCAG 2.5.5 exempts a link that is part of a sentence. The signature of
        # that is an inline box: an inline link takes its height from the line
        # it sits in and cannot be given a target size without breaking the
        # leading around it. A link set inline-block or block is a control and
        # is held to the target size like any other.
        if r["tag"] == "a" and r.get("disp") == "inline":
            continue
        if r["tag"] == "a" and r["p"] >= 0 and recs[r["p"]].get("own"):
            continue
        w, h = r["b"][2], r["b"][3]
        for pw, ph in r.get("ps", []):
            w, h = max(w, pw), max(h, ph)
        if w >= 44 and h >= 44:
            continue
        out.append(find(
            ctx, "touch-target", sev, r,
            "interactive box is %.0fx%.0fpx, under the 44x44px target%s"
            % (w, h, " (pseudo-element hit area included)" if r.get("ps") else ""),
            "every interactive element is at least 44px on both axes",
            size=[round(w, 1), round(h, 1)]))
    return out


MEASURE_LIMITS = {"heading": (36, 36), "body": (75, 70), "caption": (52, 52)}
NON_PROSE_TAGS = ("code", "pre", "th", "td", "kbd", "samp", "option", "textarea")


def check_measure_over_75(ctx):
    """A line of copy too long to track back to."""
    recs = ctx.recs
    out = []
    for r in recs:
        if not visible_text(r) or len(r["L"]) < 2 or not r.get("mcl"):
            continue
        if r["tag"] in NON_PROSE_TAGS:
            continue
        # An unbroken URL or identifier is a wrapping problem, not a measure one.
        if " " not in (r.get("own") or ""):
            continue
        anc, guard, skip = r["p"], 0, False
        while anc >= 0 and guard < 512:
            if recs[anc]["tag"] in ("nav", "table"):
                skip = True
                break
            anc = recs[anc]["p"]
            guard += 1
        if skip:
            continue
        role = "heading" if r["fs"] >= 24 else ("caption" if r["fs"] <= 13 else "body")
        hard, warn = MEASURE_LIMITS[role]
        n = r["mcl"]
        if n <= warn:
            continue
        sev = "warning" if n > hard else "note"
        out.append(find(
            ctx, "measure-over-75", sev, r,
            "longest line is %d characters at %gpx, over the %s limit of %d"
            % (n, r["fs"], role, hard if n > hard else warn),
            "house rule 9 · body copy holds 54ch, about 70 characters, and 75 is "
            "the line to draw · headings hold 36, captions hold 52",
            chars=n, role=role, limit=hard))
    return out


def check_type_scale(ctx):
    """A font size off the house ladder."""
    lad = ctx.ladder["values"]
    out = []
    for r in ctx.recs:
        if not r.get("own") or not r["vis"]:
            continue
        # An ancestor transform changes the rendered size while leaving the
        # computed font-size untouched.
        rendered = round(r["fs"] * r.get("scl", 1), 2)
        if min(abs(rendered - v) for v in lad) <= 0.5:
            continue
        out.append(find(
            ctx, "type-scale", "warning", r,
            "font-size renders at %gpx, off the ladder for %dpx · nearest step %gpx"
            % (rendered, ctx.width, nearest_step(rendered, lad)),
            "font sizes come from the ladder resolved at this width: %s"
            % ", ".join("%g" % v for v in lad),
            size=rendered, nearest=nearest_step(rendered, lad),
            ladderSource=ctx.ladder["source"]))
    return out


def check_type_floor(ctx):
    """Type below the readable floor. Section 9 of the standard."""
    out = []
    if ctx.media == "print":
        for r in ctx.recs:
            if not r.get("own") or not r["vis"]:
                continue
            pt = round(r["fs"] * r.get("scl", 1) * 0.75, 2)
            if pt >= 9.0:
                continue
            out.append(find(
                ctx, "type-floor", "error", r,
                "renders at %gpt in print media, below the 9pt floor" % pt,
                "section 9 · nothing prints below 9pt", sizePt=pt))
        return out
    for r in ctx.recs:
        if not r.get("own") or not r["vis"] or r.get("sro"):
            continue
        rendered = round(r["fs"] * r.get("scl", 1), 2)
        if rendered >= 12:
            continue
        out.append(find(
            ctx, "type-floor", "error", r,
            "renders at %gpx, below the 12px screen floor" % rendered,
            "section 9 · nothing on screen falls under 12px", size=rendered))
    return out


def check_weight_ladder(ctx):
    """A weight outside 400, 600, 700, 800. House rule 2."""
    recs = ctx.recs
    out = []
    # House rule 4 wants more tracking on a dark ground than the same step
    # carries on a light one. The light-ground value for each step is read off
    # this page rather than assumed, so the comparison is to something measured.
    light = {}
    for r in recs:
        if not r.get("own") or not r["vis"] or r["gk"] != "COLOR" or not r["gc"]:
            continue
        if srgb_lum(*r["gc"][:3]) >= 0.18:
            light.setdefault((r["fs"], r["fw"]), []).append(r["ls"])
    for r in recs:
        if not r.get("own") or not r["vis"] or r.get("sro"):
            continue
        try:
            fw = int(r["fw"])
        except (TypeError, ValueError):
            continue
        parent_fw = None
        if r["p"] >= 0 and recs[r["p"]].get("fw"):
            try:
                parent_fw = int(recs[r["p"]]["fw"])
            except (TypeError, ValueError):
                parent_fw = None
        if fw not in WEIGHT_LADDER:
            # Inherited weight is not an authored weight, so only the element
            # that introduced it is reported.
            if parent_fw != fw:
                out.append(find(
                    ctx, "weight-ladder", "warning", r,
                    "font-weight %d is outside 400, 600, 700, 800%s" % (
                        fw, "" if r.get("fchk") is not False else
                        " · the loaded family cannot produce it, so it renders synthesised"),
                    "house rule 2 · four weights, no others", weight=fw))
            continue
        dark = r["gk"] == "COLOR" and r["gc"] and srgb_lum(*r["gc"][:3]) < 0.18
        if not dark:
            continue
        if fw == 800 and parent_fw != 800:
            out.append(find(
                ctx, "weight-ladder", "warning", r,
                "weight 800 on a ground of luminance %.3f" % srgb_lum(*r["gc"][:3]),
                "house rule 4 · display weight drops one step on a dark ground",
                weight=fw))
            continue
        peers = light.get((r["fs"], r["fw"]))
        if peers:
            want = max(peers) + 0.005 * r["fs"]
            if r["ls"] < want - 0.01:
                out.append(find(
                    ctx, "weight-ladder", "warning", r,
                    "letter-spacing is %.3fpx on a dark ground, and the same step "
                    "on a light ground on this page is %.3fpx, so it needs at "
                    "least %.3fpx" % (r["ls"], max(peers), want),
                    "house rule 4 · tracking gains 0.005em on a dark ground",
                    letterSpacing=r["ls"], required=round(want, 3)))
    return out


def check_near_align(ctx):
    """Edges that miss by one to three pixels. Off by default."""
    recs = [r for r in ctx.recs if r["vis"] and r["b"][2] >= 8 and r["b"][3] >= 8]
    groups = {}
    for r in recs:
        f = frame_of(ctx.recs, r["i"])
        groups.setdefault(f["i"] if f else -1, []).append(r)
    out = []
    for _, arr in groups.items():
        for kind, get in (("left", lambda r: r["b"][0]),
                          ("right", lambda r: r["b"][0] + r["b"][2]),
                          ("top", lambda r: r["b"][1])):
            vals = sorted(((round(get(r), 1), r) for r in arr), key=lambda t: t[0])
            i = 0
            while i < len(vals):
                j = i
                while j + 1 < len(vals) and vals[j + 1][0] - vals[i][0] <= 4:
                    j += 1
                cluster = vals[i:j + 1]
                i = j + 1
                if len(cluster) < 3:
                    continue
                spread = cluster[-1][0] - cluster[0][0]
                if spread <= 0 or spread > 4:
                    continue
                counts = {}
                for v, _r in cluster:
                    counts[round(v)] = counts.get(round(v), 0) + 1
                mode = max(counts, key=lambda k: (counts[k], -abs(k)))
                for v, r in cluster:
                    if abs(v - mode) < 0.5:
                        continue
                    out.append(find(
                        ctx, "near-align", "note", r,
                        "%s edge at %gpx misses the cluster of %d edges at %gpx "
                        "by %.1fpx" % (kind, v, len(cluster), mode, abs(v - mode)),
                        "edges that nearly line up either line up or clearly do not",
                        edge=kind, offsetPx=round(abs(v - mode), 1)))
    return out


def check_rhythm_gaps(ctx):
    """A sequence with one gap out of step. Off by default."""
    recs = ctx.recs
    kids = {}
    for r in recs:
        if r["p"] >= 0 and r["vis"]:
            kids.setdefault(r["p"], []).append(r)
    out = []
    for pi, arr in kids.items():
        par = recs[pi]
        if par["disp"] not in ("flex", "grid", "block", "inline-flex", "inline-grid"):
            continue
        by_sig = {}
        for r in arr:
            by_sig.setdefault(r["sig"], []).append(r)
        for sig, group in by_sig.items():
            if len(group) < 4:
                continue
            vert = sorted(group, key=lambda r: r["b"][1])
            horiz = sorted(group, key=lambda r: r["b"][0])
            for axis, seq, lo, hi in (("vertical", vert, 1, 3), ("horizontal", horiz, 0, 2)):
                gaps = []
                ok = True
                for a, b in zip(seq, seq[1:]):
                    g = round(b["b"][lo] - (a["b"][lo] + a["b"][hi]), 1)
                    if g < -0.5:
                        ok = False
                        break
                    gaps.append(g)
                if not ok or len(gaps) < 3:
                    continue
                if max(gaps) - min(gaps) < 2 or max(gaps) - min(gaps) > 24:
                    continue
                out.append(find(
                    ctx, "rhythm-gaps", "note", seq[0],
                    "%d siblings matching %s have %s gaps of %s"
                    % (len(seq), sig, axis, ", ".join("%g" % g for g in gaps)),
                    "a sequence laid out on one axis has one gap, not several",
                    gaps=gaps, axis=axis))
                break
    return out


def check_weight_size_count(ctx):
    """More than three weights or three sizes above body. House rule 3. Off by default."""
    recs = ctx.recs
    out = []
    sections = {}
    for r in recs:
        if not r.get("own") or not r["vis"]:
            continue
        anc, guard, sec = r["p"], 0, -1
        while anc >= 0 and guard < 512:
            if recs[anc]["tag"] in ("section", "article", "main", "aside", "footer", "header"):
                sec = anc
                break
            anc = recs[anc]["p"]
            guard += 1
        sections.setdefault(sec, []).append(r)
    for si, arr in sections.items():
        weights = sorted({r["fw"] for r in arr})
        sizes = sorted({r["fs"] for r in arr if r["fs"] > 16})
        if len(weights) <= 3 and len(sizes) <= 3:
            continue
        rec = recs[si] if si >= 0 else arr[0]
        out.append(find(
            ctx, "weight-size-count", "note", rec,
            "%d weights (%s) and %d sizes above 16px (%s)"
            % (len(weights), ", ".join(weights), len(sizes),
               ", ".join("%g" % s for s in sizes)),
            "house rule 3 · three weights maximum, three sizes above body maximum",
            weights=list(weights), sizes=sizes))
    return out


# ---------------------------------------------------------------------- driver
def resolve_ladder(chrome, opts):
    raw = chrome.evaluate(LADDER_JS.replace("__SRC__", json.dumps(HOUSE_FS)))
    d = json.loads(raw)
    if opts.ladder:
        return {"values": sorted(set(opts.ladder), reverse=True), "source": "config"}
    if len(d["page"]) >= 8:
        return {"values": sorted(set(d["page"].values()), reverse=True),
                "source": "page :root --fs-* tokens"}
    return {"values": sorted(set(d["house"].values()), reverse=True),
            "source": "house type-system.css, resolved at this width"}


def capture(chrome, url, width, height, opts, media="screen"):
    chrome.viewport(width, height)
    # Always set it, never only on the print pass. An emulated media type
    # outlives the pass that asked for it, and a later screen pass would then
    # be measuring the print stylesheet without saying so.
    chrome.cmd("Emulation.setEmulatedMedia", media="" if media == "screen" else media)
    chrome.goto(url, settle=opts.settle)
    raw = chrome.evaluate(COLLECT_JS)
    if not raw:
        raise RuntimeError("the page returned no measurement payload")
    return json.loads(raw)


def run_width(chrome, url, width, height, opts, enabled, media="screen"):
    page = capture(chrome, url, width, height, opts, media)
    ctx = Ctx(page, width, height, resolve_ladder(chrome, opts), opts, media)
    if "under-fixed-chrome" in enabled and media == "screen":
        try:
            ctx.bottom = json.loads(chrome.evaluate(BOTTOM_JS))
            chrome.evaluate("window.scrollTo(0,0)")
        except Exception:
            ctx.bottom = None
    findings = []
    order = [
        ("ink-occlusion", lambda: check_ink_occlusion(ctx)),
        ("line-box-collision", lambda: check_line_box_collision(ctx)),
        ("hairline-crosses-text", lambda: check_hairline_crosses_text(ctx)),
        ("flow-box-overlap", lambda: check_flow_box_overlap(ctx)),
        ("text-clipped", lambda: check_text_clipped(ctx)),
        ("past-frame", lambda: check_past_frame(ctx)),
        ("doc-overflow-x", lambda: check_doc_overflow_x(ctx)),
        ("under-fixed-chrome", lambda: check_under_fixed_chrome(ctx)),
        ("contrast-solid", lambda: check_contrast_solid(ctx)),
        ("contrast-over-image", lambda: check_contrast_over_image(ctx, chrome)),
        ("contrast-nontext", lambda: check_contrast_nontext(ctx)),
        ("touch-target", lambda: check_touch_target(ctx)),
        ("measure-over-75", lambda: check_measure_over_75(ctx)),
        ("type-scale", lambda: check_type_scale(ctx)),
        ("type-floor", lambda: check_type_floor(ctx)),
        ("weight-ladder", lambda: check_weight_ladder(ctx)),
        ("near-align", lambda: check_near_align(ctx)),
        ("rhythm-gaps", lambda: check_rhythm_gaps(ctx)),
        ("weight-size-count", lambda: check_weight_size_count(ctx)),
    ]
    for name, fn in order:
        if name not in enabled:
            continue
        findings.extend(fn())
    return ctx, findings


# ---------------------------------------------------------------------- report
def group_key(f):
    return (f["severity"], f["check"], f["selector"], f["detail"])


def report(findings, meta, opts):
    lines = []
    W = lines.append
    W("")
    W("UI AUDIT · %s" % meta["target"])
    W("%s · %s · %d checks run, %d off"
      % (", ".join("%dx%d" % (w, h) for w, h in meta["widths"]),
         " · ".join("%d elements at %d" % (n, w) for w, n in meta["counts"]),
         len(meta["enabled"]), len(CHECKS) - len(meta["enabled"])))
    if meta.get("truncated"):
        W("element cap reached · %d elements were not measured" % meta["truncated"])
    W("")
    grouped = {}
    for f in findings:
        k = group_key(f)
        g = grouped.setdefault(k, {"f": f, "widths": []})
        if f["width"] not in g["widths"]:
            g["widths"].append(f["width"])
    by_sev = {}
    for g in grouped.values():
        by_sev.setdefault(g["f"]["severity"], []).append(g)
    total = 0
    for sev in SEVERITY_ORDER:
        arr = by_sev.get(sev)
        if not arr:
            continue
        by_check = {}
        for g in arr:
            by_check.setdefault(g["f"]["check"], []).append(g)
        W("%s · %d" % (sev.upper(), len(arr)))
        W("")
        for check in sorted(by_check, key=lambda c: -len(by_check[c])):
            group = by_check[check]
            W("  %s · %d · %s" % (check, len(group), CHECKS[check][2]))
            shown = group if opts.max_per_check <= 0 else group[:opts.max_per_check]
            for g in shown:
                f = g["f"]
                w = ", ".join(str(x) for x in sorted(g["widths"]))
                W("    %s" % f["selector"])
                if f.get("box"):
                    W("      %s · at %s" % (fmt_box(f["box"]), w))
                else:
                    W("      at %s" % w)
                if f.get("text") and not opts.quiet:
                    W('      "%s"' % f["text"])
                W("      %s" % f["detail"])
                if not opts.quiet:
                    W("      rule · %s" % f["rule"])
                W("")
            if len(group) > len(shown):
                W("    + %d more, use --json for the rest" % (len(group) - len(shown)))
                W("")
            total += len(group)
        W("")
    if not grouped:
        n = len(meta["widths"])
        W("clean · no findings from %d checks at %d width%s"
          % (len(meta["enabled"]), n, "" if n == 1 else "s"))
        W("")
    else:
        counts = " · ".join("%d %s" % (len(by_sev[s]), s)
                            for s in SEVERITY_ORDER if by_sev.get(s))
        W("%d finding%s · %s" % (total, "" if total == 1 else "s", counts))
        W("")
    return "\n".join(lines)


def parse_widths(values):
    if not values:
        return list(DEFAULT_WIDTHS)
    out = []
    for chunk in values:
        for part in str(chunk).split(","):
            part = part.strip()
            if not part:
                continue
            if "x" in part:
                w, h = part.split("x", 1)
                out.append((int(w), int(h)))
            else:
                w = int(part)
                h = dict(DEFAULT_WIDTHS).get(w, 900)
                out.append((w, h))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="ui-audit.py",
        description="HOUSE UI STANDARD v1.0 · audit a rendered page for the "
                    "defects a person sees: spacing off the grid, lines crossing "
                    "over, graphics crossing over.")
    ap.add_argument("target", nargs="?", help="a URL or a path to a local html file")
    ap.add_argument("--width", action="append", default=[],
                    help="pass width, or WIDTHxHEIGHT · repeatable · comma separated "
                         "· default 375, 768, 1440")
    ap.add_argument("--only", default="", help="run only these check ids, comma separated")
    ap.add_argument("--skip", default="", help="skip these check ids, comma separated")
    ap.add_argument("--json", action="store_true", help="emit findings as json")
    ap.add_argument("--quiet", action="store_true", help="one finding, no rule text")
    ap.add_argument("--strict", action="store_true", help="promote every warning to an error")
    ap.add_argument("--print-media", action="store_true",
                    help="add a print-media pass and check the 9pt floor")
    ap.add_argument("--image-samples", type=int, default=16,
                    help="how many text nodes over an image to sample per width · default 16")
    ap.add_argument("--max-per-check", type=int, default=8,
                    help="findings printed per check · 0 for all · default 8")
    ap.add_argument("--ladder", default="",
                    help="declare this project's own font-size ladder in px, comma "
                         "separated · the shared layer is a floor, not a ceiling")
    ap.add_argument("--settle", type=float, default=1.0,
                    help="seconds to wait after fonts are ready · default 1.0")
    ap.add_argument("--list-checks", action="store_true", help="list every check and exit")
    opts = ap.parse_args(argv)

    if opts.list_checks:
        for cid in CHECKS:
            sev, on, desc = CHECKS[cid]
            print("%-22s %-8s %-4s %s" % (cid, sev, "on" if on else "off", desc))
        return 0
    if not opts.target:
        ap.error("a target url or file path is required")

    opts.ladder = [float(x) for x in opts.ladder.split(",") if x.strip()] \
        if opts.ladder else None

    enabled = {c for c in CHECKS if CHECKS[c][1]}
    if opts.only:
        want = {c.strip() for c in opts.only.split(",") if c.strip()}
        bad = want - set(CHECKS)
        if bad:
            sys.stderr.write("error: unknown check id · %s\n" % ", ".join(sorted(bad)))
            return 2
        enabled = want
    if opts.skip:
        drop = {c.strip() for c in opts.skip.split(",") if c.strip()}
        bad = drop - set(CHECKS)
        if bad:
            sys.stderr.write("error: unknown check id · %s\n" % ", ".join(sorted(bad)))
            return 2
        enabled -= drop
    if not enabled:
        sys.stderr.write("error: every check was skipped\n")
        return 2

    target = opts.target
    if not re.match(r"^[a-z]+://", target):
        p = os.path.abspath(os.path.expanduser(target))
        if not os.path.exists(p):
            sys.stderr.write("error: no such file · %s\n" % p)
            return 2
        target = "file://" + p
    if not os.path.exists(CHROME):
        sys.stderr.write("error: chrome not found at %s · set UI_AUDIT_CHROME\n" % CHROME)
        return 2

    widths = parse_widths(opts.width)
    tmp = os.path.join(os.path.expanduser("~"), ".cache", "ui-audit")
    findings, counts, contexts, truncated = [], [], {}, 0
    chrome = None
    try:
        chrome = Chrome(tmp)
        for w, h in widths:
            ctx, fs = run_width(chrome, target, w, h, opts, enabled)
            contexts[w] = ctx
            counts.append((w, len(ctx.recs)))
            truncated = max(truncated, ctx.page.get("truncated", 0))
            findings.extend(fs)
        if "spacing-off-4" in enabled:
            wide = sorted(contexts, reverse=True)
            a = contexts[1440] if 1440 in contexts else contexts[wide[0]]
            b = contexts[768] if 768 in contexts else (
                contexts[wide[1]] if len(wide) > 1 else None)
            findings.extend(check_spacing_off_4(a, b))
        if opts.print_media and "type-floor" in enabled:
            w, h = widths[-1]
            _, pf = run_width(chrome, target, w, h, opts, {"type-floor"}, media="print")
            findings.extend(pf)
    except Exception as exc:
        sys.stderr.write("error: %s\n" % exc)
        return 2
    finally:
        if chrome:
            chrome.close()

    if opts.strict:
        for f in findings:
            if f["severity"] == "warning":
                f["severity"] = "error"

    meta = {"target": target, "widths": widths, "counts": counts,
            "enabled": sorted(enabled), "truncated": truncated}
    if opts.json:
        sev_counts = {}
        for f in findings:
            sev_counts[f["severity"]] = sev_counts.get(f["severity"], 0) + 1
        print(json.dumps({"meta": meta, "counts": sev_counts,
                          "findings": findings}, indent=1))
    else:
        sys.stdout.write(report(findings, meta, opts))
    return 1 if any(f["severity"] in ERROR_LEVEL for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
