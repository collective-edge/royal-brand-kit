#!/usr/bin/env python3
"""Builds this kit's guidelines page.

    python3 guidelines/build.py          writes index.html at the repo root
    python3 guidelines/build.py --og     also renders guidelines/og.png, 1200 by 630 (needs Chrome or Chromium)
    python3 guidelines/build.py --check  builds, checks, writes nothing

This file and manual.css are identical in all three kits. Everything that
differs comes from the kit the script sits in:

    brands.json                 the registry: names, repos, CDN roots, the co-brand lockup
    tokens.json                 colors, tiers, alerts, chart colors, logo roles, the kit version
    snippets/type-tokens.json   the type scale, weights, spacing
    snippets/palette.css        token names, checked against everything the page prints
    snippets/data-color.css     chart token names
    documents.json              page sizes and margins, when the kit ships one
    for-humans/pack.json        which logo files have a PNG
    guidelines/page.json        the brand's own sentences and sample documents

The page links its own kit's files by relative path, so it works from a clone
and from GitHub Pages. Files that belong to another kit load from that kit's CDN.
The build fails when the page prints a hex, a token or a path the kit does not ship.
"""
import html, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
esc = html.escape


def load(rel, required=True):
    p = os.path.join(KIT, rel)
    if not os.path.exists(p):
        if required: sys.exit(f'missing {rel}')
        return None
    return json.load(open(p, encoding='utf-8'))


def read(rel):
    return open(os.path.join(KIT, rel), encoding='utf-8').read()


REG = load('brands.json')
T = load('tokens.json')
TT = load('snippets/type-tokens.json')
PG = load('guidelines/page.json')
PACK = load('for-humans/pack.json')
DOCS = load('documents.json', required=False)
KEY = T['brand']
ME = REG['brands'][KEY]
NAME = ME['name']
REPO = ME['repo']
CDNROOT = ME['cdnRoot']
ORDER = list(REG['brands'])
IS_PARENT = ME['role'] == 'parent'
PARENT = next(k for k in ORDER if REG['brands'][k]['role'] == 'parent')
PAGES = {k: 'https://{}.github.io/{}/'.format(*REG['brands'][k]['repo'].split('/')) for k in ORDER}
ZIP = f'https://github.com/{REPO}/archive/refs/heads/main.zip'

# ------------------------------------------------------------------ the kit's CSS, as data
CSS_FILES = ['snippets/palette.css', 'snippets/data-color.css', 'snippets/type-system.css', 'snippets/cobrand.css', 'snippets/ui.css']
CSS_TEXT = {f: read(f) for f in CSS_FILES}
CSSV = {}
for f in CSS_FILES:
    for m in re.finditer(r'(--[a-z][a-z0-9-]*)\s*:\s*([^;]+);', CSS_TEXT[f]):
        CSSV.setdefault(m.group(1), m.group(2).strip())
CSS_CLASSES = set(re.findall(r'\.([a-z][a-z0-9-]*)', ' '.join(CSS_TEXT.values())))


def resolve(var):
    """The value a custom property ends on, following var() references."""
    seen = set()
    val = CSSV[var]
    while True:
        m = re.fullmatch(r'var\((--[a-z0-9-]+)(?:\s*,\s*(.+))?\)', val)
        if not m: return val
        ref, fb = m.group(1), m.group(2)
        if ref in CSSV and ref not in seen:
            seen.add(ref); val = CSSV[ref]
        elif fb: val = fb.strip()
        else: sys.exit(f'{var} does not resolve')


def U(h): return h.upper() if h and h.startswith('#') else h
def rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
def lum(h):
    def f(c):
        c /= 255; return c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4
    r, g, b = rgb(h); return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def asset(brand, path):
    """A kit file. Relative for this kit, the CDN for another kit."""
    if brand == KEY:
        assert os.path.exists(os.path.join(KIT, path)), f'missing {path}'
        return path
    return REG['brands'][brand]['cdnRoot'] + path


def from_url(url):
    """A CDN URL as the page should load it: relative when it points into this kit."""
    for k in ORDER:
        root = REG['brands'][k]['cdnRoot']
        if url.startswith(root): return asset(k, url[len(root):])
    return url


def short(url):
    return url.split('@main/')[1] if '@main/' in url else url


# ------------------------------------------------------------------ theme, from tokens.json
BG, FG, BD, NEU, AL, TIERS = T['background'], T['foreground'], T['border'], T['neutral'], T['alert'], T['tiers']
TH = TIERS['tableHeader']
THEME = {
    'accent': FG['fg-accent']['value'], 'band': BG['bg-band']['value'], 'band-rule': BD['border-band-rule']['value'],
    'surface': BG['bg-surface']['value'], 'inverse': BG['bg-inverse']['value'],
    'th': TH['bg'], 'th-fg': TH['fg'], 'th-rule': TH['rule'] or TH['bg'],   # no rule: the header is solid to its edge
    'ink': FG['fg-1']['value'], 'sec': FG['fg-2']['value'], 'ter': FG['fg-3']['value'], 'dim': FG['fg-4']['value'],
    'hair': BD['border-1']['value'], 'border': BD['border-2']['value'],
    'od1': FG['fg-on-dark-1']['value'], 'od2': FG['fg-on-dark-2']['value'], 'od3': FG['fg-on-dark-3']['value'], 'odb': BD['border-on-dark']['value'],
    'go': AL['go']['text'], 'warn': AL['warn']['text'], 'stop': AL['stop']['text'], 'info': AL['info']['text'],
}

# ------------------------------------------------------------------ document facts
# documents.json holds the page sizes and margins. The fallback values are the owner rulings.
DOC_FACTS = {'memoMargin': 0.75, 'onePagerMargin': 0.6, 'deckMargins': {'topIn': 0.67, 'rightIn': 0.83, 'bottomIn': 0.42, 'leftIn': 0.83},
             'deckBody': 'body-lg', 'page': (8.5, 11), 'slide': (13.333, 7.5),
             'templates': {'memo': 'templates/memo.html', 'one-pager': 'templates/one-pager.html', 'deck': 'templates/deck.html'}}


def _margins(name):
    """types.<name>.margins in documents.json: topIn, rightIn, bottomIn, leftIn."""
    m = ((DOCS or {}).get('types', {}).get(name) or {}).get('margins')
    return m if isinstance(m, dict) and all(isinstance(m.get(k), (int, float)) for k in ('topIn', 'rightIn', 'bottomIn', 'leftIn')) else None


for _fact, _name in (('memoMargin', 'memo'), ('onePagerMargin', 'one-pager')):
    _m = _margins(_name)
    if _m:
        assert len(set(_m.values())) == 1, f'{_name} margins differ by side'
        DOC_FACTS[_fact] = _m['leftIn']
if _margins('deck'): DOC_FACTS['deckMargins'] = _margins('deck')
if DOCS and isinstance(DOCS.get('templates'), dict): DOC_FACTS['templates'].update({k: v for k, v in DOCS['templates'].items() if k in DOC_FACTS['templates']})


def inch(v): return f'{v:g}in'


# ------------------------------------------------------------------ helpers
def brk(text, fileish=False):
    """Escaped text with break opportunities after a slash, so a URL or a path never breaks inside a word."""
    t = esc(text).replace('://', '\x00')
    t = re.sub(r'([/_-])' if fileish else r'(/)', r'\1<wbr>', t)
    return t.replace('\x00', '://')
def nb(t): return re.sub(r'(--[a-z][a-z0-9-]*|\.bk-code)', r'<span class="nb">\1</span>', t)
def v(text, copy=None, cls='v'):
    """A machine value: selectable text that copies on click."""
    c = f' data-c="{esc(copy)}"' if copy else ' data-c'
    return f'<span class="{cls}"{c}>{brk(text, fileish="/" in text and " " not in text and not text.startswith("http"))}</span>'
def mc(pairs):
    return '<div class="c3 mc">' + ''.join(f'<span class="k">{k}</span>{val}' for k, val in pairs) + '</div>'
def sentence(s): return s[0].upper() + s[1:]
def first(s): return s.split('. ')[0].rstrip('.')
def size_key(role):
    for k in ('horizontal', 'compact', 'stacked'):
        if role.startswith(k): return k
    return 'app' if role == 'app-icon' else 'mark'


ROLE_ORDER = ['horizontal-on-light', 'horizontal-on-dark', 'compact-on-light', 'compact-on-dark', 'mark-on-light', 'mark-on-dark',
              'app-icon', 'stacked-on-light', 'stacked-on-dark']
LOGOS = {r: T['logos'][r] for r in ROLE_ORDER if T['logos'].get(r)}          # role -> CDN URL, this kit
LOGO_SRC = {r: from_url(u) for r, u in LOGOS.items()}                          # role -> relative path
PACK_BY_SRC = {l['source']: l for l in PACK['logos']}
PACK_BY_BYTES = {open(os.path.join(KIT, l['source']), 'rb').read(): l for l in PACK['logos'] if os.path.exists(os.path.join(KIT, l['source']))}
PARENT_REG = REG['brands'][PARENT]
LOCKUP = REG['cobrand']['lockup']


def min_size(role):
    k = 'app-icon' if role == 'app-icon' else size_key(role)
    px = T['logos']['minWidth'].get(k); pr = T['logos']['minWidthPrint'].get(k)
    return ' · '.join(x for x in (px, pr) if x) or PG.get('minimumNote', {}).get(k) or 'none published'


def png_of(role):
    p = PACK_BY_SRC.get(LOGO_SRC[role]) or PACK_BY_BYTES.get(open(os.path.join(KIT, LOGO_SRC[role]), 'rb').read())
    if not p: return None
    rel = f'for-humans/logos/png/{PACK["filePrefix"]}-{p["name"]}-{p["png"][0]}w.png'
    return rel if os.path.exists(os.path.join(KIT, rel)) else None


def parent_lockup(ground):
    return from_url(LOCKUP['on-dark' if ground == 'dark' else 'on-light'])


def powered(ground='light'):
    return f'<div class="pw"><span>{esc(REG["cobrand"]["label"])}</span><img src="{parent_lockup(ground)}" alt="{esc(PARENT_REG["name"])}"></div>'


class Page:
    def __init__(s):
        s.fig = 0; s.sec = 0; s.sub = 0; s.r = 0
    def cap(s, text, right=''):
        s.fig += 1
        r = f'<span class="cap-r">{right}</span>' if right else ''
        return f'<figcaption><span><b>Fig. {s.fig:02d}</b>{text}</span>{r}</figcaption>'
    def rules(s, items, cls='lines'):
        out = ''
        for x in items:
            s.r += 1
            out += f'<li><span class="i">R{s.r:02d}</span><span>{esc(x)}</span></li>'
        return f'<ol class="{cls}">{out}</ol>'
    def section(s, title, lead, body, id_):
        s.sec += 1; s.sub = 0
        return f'''
<section class="sec" id="{id_}" aria-labelledby="{id_}-h">
  <div class="grid sec-head">
    <p class="rail num" aria-hidden="true">{s.sec:02d}</p>
    <div class="main">
      <h2 id="{id_}-h">{title}</h2>
      <p class="lead">{lead}</p>
    </div>
  </div>{body(s)}
</section>'''
    def subhead(s, title, note=''):
        s.sub += 1
        n = f'<p class="note">{note}</p>' if note else ''
        return f'<div class="rail"><p class="n">{s.sec}.{s.sub}</p><div><h3>{title}</h3>{n}</div></div>'
    def subsec(s, title, note, main, wide='', railnote=True):
        head = s.subhead(title, note if railnote else '')
        if not railnote: main = f'<p class="note">{note}</p>' + main
        w = f'\n    <div class="full">{wide}</div>' if wide else ''
        return f'''
  <div class="grid sub">
    {head}
    <div class="main">{main}</div>{w}
  </div>'''


# ------------------------------------------------------------------ 01 logo
def s_logo(P):
    out = ''
    g = PG['bigPlate']; bg = U(resolve(g['ground']))
    cls = 'bigplate plate' + (' ruled' if lum(bg) > .8 else '')
    out += f'''
  <div class="grid"><figure class="full">
    <div class="{cls}" style="background:{bg}"><img src="{LOGO_SRC[g['role']]}" alt="{esc(NAME)} logo, the primary lockup" style="width:{g['width']}px"></div>
    {P.cap(esc(g['caption']), v(g['role']) + ' on ' + v(bg))}
  </figure></div>'''
    rows = ''
    for role, url in LOGOS.items():
        app = role == 'app-icon'; dark = role.endswith('-on-dark')
        c = PG['logoCopy'][role]
        w = PG['logoRowWidth'][size_key(role)]
        ground = 'own square' if app else ('dark' if dark else 'light')
        links = f'<a href="{LOGO_SRC[role]}">SVG</a>'
        if png_of(role): links += f'<a href="{png_of(role)}">PNG</a>'
        rows += f'''
        <div class="g8 row">
          <div class="c3 plate{' dark' if dark else ''}"><img src="{LOGO_SRC[role]}" alt="{esc(NAME)} {esc(c['name'].lower())}, on {ground}" style="width:{w}px"></div>
          <div class="c2 tx"><b>{esc(c['name'])}</b>{esc(c['use'])}</div>
          {mc([('role', v(role)), ('file', v(short(url), url)), ('min', f'<span class="v">{min_size(role)}</span>'), ('get', f'<span class="v">{links}</span>')])}
        </div>'''
    tbl = f'''<div class="tbl logos">
        <div class="g8 hd"><span class="c3">Lockup, on its ground</span><span class="c2">Use</span><span class="c3">Role, file, minimum</span></div>{rows}
      </div>'''
    out += P.subsec('Lockups', 'One row per shipped file. Ask for the role. The file is what the role resolves to.' + (' The partner marks are in 6.2.' if IS_PARENT else '') + f' <a class="blk" href="{ZIP}">Download every logo, ZIP</a>', tbl)
    c = PG['clearSpace']; s = c['scale']
    x = c['x'] * s; aw = (c['art'][2] - c['art'][0]) * s; ah = (c['art'][3] - c['art'][1]) * s
    px = lambda n: f'calc(var(--u)*{n:.1f})'
    img = f'<img src="{LOGO_SRC[c["role"]]}" alt="" style="width:{px(c["viewBox"][0] * s)};left:{px(-c["art"][0] * s)};top:{px(-c["art"][1] * s)}">'
    cells = ''.join(f'<span>{"x" if k in (0, 2, 6, 8) else ""}</span>' if k != 4 else f'<span class="art">{img}</span>' for k in range(9))
    items = ''
    for m in PG['minimums']:
        role = m['role']; k = 'app-icon' if role == 'app-icon' else size_key(role)
        w = T['logos']['minWidth'][k]
        items += f'<li><span><img src="{LOGO_SRC[role]}" alt="" style="width:{w}"><b>{esc(m["label"])}</b></span><span class="d">{min_size(role)}</span></li>'
    fig = f'''<figure>
        <div class="cl">
          <div class="field"><div class="cs" role="img" aria-label="Clear space diagram: the logo with x of empty space on every side" style="--w:{aw + 2 * x + 4:.0f};grid-template-columns:{px(x)} {px(aw)} {px(x)};grid-template-rows:{px(x)} {px(ah)} {px(x)}">{cells}</div></div>
          <ul class="mins">{items}</ul>
        </div>
        {P.cap(f'Clear space, where x is {esc(c["unit"])}. Minimum sizes, drawn at actual size.')}
      </figure>
      {P.rules(PG['logoNotes'], 'lines cols2')}'''
    out += P.subsec('Space and size', 'Keep x clear on all four sides. Nothing enters it: no type, no rule, no edge. Minimums are screen width in pixels and print width in inches.', fig)
    return out


# ------------------------------------------------------------------ 02 color
TIER_LABEL = {'surface2': 'Surface 2'}
NEUTRALS = [('ink', 'Ink', '--fg-1'), ('secondary', 'Secondary', '--fg-2'), ('tertiary', 'Tertiary', '--fg-3'), ('dimmed', 'Dimmed', '--fg-4'),
            ('border', 'Border', '--border-2'), ('hairline', 'Hairline', '--border-1'), ('onDarkBody', 'On-dark body', '--fg-on-dark-2'), ('onDarkCaption', 'On-dark caption', '--fg-on-dark-3')]
ALERT_WORD = {'go': 'Cleared', 'warn': 'At risk', 'stop': 'Blocked', 'info': 'Notice'}


def palette_rows():
    raw = {r['key']: r for r in T['raw']}
    n = 0; rows = []
    for p in PG['palette']:
        if 'tier' in p:
            n += 1; t = TIERS[p['tier']]; r = raw[p['raw']]
            assert U(t['hex']) == U(r['hex']), f'tier {p["tier"]} and raw {p["raw"]} disagree'
            name = TIER_LABEL.get(p['tier'], p['tier'].capitalize()); role = f'Tier {n} · {p["raw"].capitalize()}'; var = t['var']
        else:
            name, role, var = p['name'], p['role'], p['token']
            m = re.match(r'Tier (\d+) ', role)
            if m:
                n += 1; assert int(m.group(1)) == n, f'{role} is out of order'
        rows.append(dict(name=name, role=role, var=var, hex=U(resolve(var)), use=p['use'], never=p.get('never')))
    return rows


def s_color(P):
    out = ''
    rows = ''
    for p in palette_rows():
        r, g, bb = rgb(p['hex'])
        edge = ' edge' if lum(p['hex']) > .8 else ''
        nv = f' <span class="nv">{esc(p["never"])}</span>' if p['never'] else ''
        rows += f'''
        <div class="row">
          <div class="sw{edge}" style="background:{p['hex']}"></div>
          <div class="info">
            <div class="tx"><b>{esc(p['name'])}<span class="rl">{esc(p['role'])}</span></b>{nb(esc(p['use']))}{nv}</div>
            <div class="mc">{''.join(f'<span class="k">{k}</span>{val}' for k, val in [('hex', v(p['hex'])), ('rgb', v(f'{r} {g} {bb}')), ('token', v(p['var']))])}</div>
          </div>
        </div>'''
    main = f'''<div class="tbl pal">
        <div class="g8 hd"><span class="c2">{esc(PG['paletteHead'])}</span><span class="c3">Name and use</span><span class="c3">Hex, RGB, token</span></div>{rows}
      </div>'''
    out += P.subsec('Palette', esc(PG['colorNote']), main)
    rows = ''
    for k, nm, tk in NEUTRALS:
        h = U(NEU[k]['hex'])
        assert U(resolve(tk)) == h, f'{tk} is not the neutral {k}'
        rows += f'''
        <div class="g8 row">
          <div class="c2 nm"><span class="chip{' edge' if lum(h) > .7 else ''}" style="background:{h}"></span>{nm}</div>
          <div class="c3 u">{esc(NEU[k]['use'].rstrip('.'))}.</div>
          <div class="c3 mci">{v(h)}{v(tk)}</div>
        </div>'''
    main = f'''<div class="tbl neu">
        <div class="g8 hd"><span class="c2">Neutral</span><span class="c3">Use. Ratios are on white</span><span class="c3 mci"><span>Hex</span><span>Token</span></span></div>{rows}
      </div>'''
    out += P.subsec('Neutrals', 'One neutral family for all three brands. It leans neither blue nor purple, so it sits beside every brand color.', main)
    names = {s: AL['css'][s].replace('<name>', '{}') for s in ('base', 'text', 'tint', 'onTint', 'onDark')}
    rows = ''
    for k in ('go', 'warn', 'stop', 'info'):
        a = {s: U(AL[k][s]) for s in ('base', 'text', 'tint', 'onTint', 'onDark')}
        w = ALERT_WORD[k]
        rows += f'''<tr>
            <th scope="row"><b>{k.capitalize()}</b><span class="s">{esc(first(AL[k]['use']))}</span>{v(T['status'][k]['var'], cls='s')}</th>
            <td data-l="Base"><span class="sw" style="background:{a['base']}"></span>{v(a['base'], cls='s')}{v(names['base'].format(k), cls='s tk')}</td>
            <td data-l="Text on white"><span class="sw txt bare" style="color:{a['text']}"><span class="dot" style="background:{a['text']}"></span>{w}</span>{v(a['text'], cls='s')}{v(names['text'].format(k), cls='s tk')}</td>
            <td data-l="Tint"><span class="sw txt" style="background:{a['tint']};color:{a['onTint']}"><span class="dot" style="background:{a['onTint']}"></span>{w}</span>{v(a['tint'], cls='s')}{v(names['tint'].format(k), cls='s tk')}</td>
            <td data-l="On the band"><span class="sw txt dk" style="color:{a['onDark']}"><span class="dot" style="background:{a['onDark']}"></span>{w}</span>{v(a['onDark'], cls='s')}{v(names['onDark'].format(k), cls='s tk')}</td>
          </tr>'''
    main = f'''<figure>
        <table class="alert"><thead><tr><th scope="col">Meaning and alias</th><th scope="col">Base</th><th scope="col">Text on white</th><th scope="col">Tint</th><th scope="col">On the band</th></tr></thead><tbody>{rows}</tbody></table>
        {P.cap('The alert family. Shared by all three brands. Each step carries its token. The status alias resolves to the base.')}
      </figure>'''
    out += P.subsec('Alerts', 'Four meanings, one family. Green means good and nothing else. A brand color is never a status. The word always travels with the color.', main)
    D = T['data']; cap = D['series']['allPairsCap']
    nums = {3: 'three', 4: 'four'}
    count = {6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten'}
    cols = ''
    for i, (h, hd) in enumerate(zip(D['series']['light'], D['series']['dark'])):
        h, hd = U(h), U(hd)
        cols += f'<li><span class="c" style="background:{h}"></span><span class="c dk" style="background:{hd}"></span><span class="nn">{i + 1}</span>{v(h)}{v(hd)}{v(f"--series-{i + 1}", cls="tk")}</li>'
    sq = ''.join(f'<li><span class="c" style="background:{U(h)}"></span>{v(U(h))}{v(f"--seq-{st}", cls="tk")}</li>' for st, h in zip(D['sequential']['steps'], D['sequential']['light']))
    main = f'''<figure>
        <p class="series-h">Series. Top chip on light, lower chip on the band. Hex in the same order.</p>
        <ol class="series two">{cols}</ol>
        <p class="series-h">Sequential ramp, {esc(NAME)}</p>
        <ol class="series seq">{sq}</ol>
        {P.cap(f'Chart series in fixed order, one to {count[len(D["series"]["light"])]}, and the sequential ramp. The ramp ends on {"the ink" if not T["hasColor"] else "the brand"}.')}
      </figure>'''
    out += P.subsec('Charts', f'Chart color is a separate house set of {count[len(D["series"]["light"])]}. A brand color is never a series color. Assign in order. Never cycle. In a scatter, {nums[cap["light"]]} series at most on light and {nums[cap["dark"]]} on dark. Darker means more, so the ramp can carry the brand.', main)
    return out


# ------------------------------------------------------------------ 03 type
SCALE = {t['token']: t for t in TT['scale']}
SAMPLES = {'display-xl': 'Unit 12', 'display-lg': 'On scene', 'display-md': 'Shift report', 'h1': 'Night coverage', 'h2': 'Fleet readiness',
           'h3': 'Crew handoff at 06:00', 'h4': 'Station 4, north county', 'body-lg': 'Every crew hands off on one page.', 'body': 'Unit 12 cleared the scene at 06:42.',
           'body-sm': 'Mileage 48,210. Next service at 50,000.', 'caption': 'Handoff form, page one.', 'eyebrow': 'Shift summary'}
TYPE_USE = {'display-xl': 'Hero and title bands only', 'display-lg': 'Hero and title bands only', 'display-md': 'Slide headlines', 'h1': 'Page title', 'h2': 'Section heading',
            'h3': 'Subhead', 'h4': 'Subhead', 'body-lg': 'Lead paragraph, deck body', 'body': 'Body', 'body-sm': f'Table cells, secondary body. {TT["office"]["minBodyPt"]:g}pt is the print body floor',
            'caption': f'Captions, footers. {TT["office"]["minAnyPt"]:g}pt is the print floor', 'eyebrow': 'Uppercase labels, always tracked'}


def weight_use(w): return sentence(re.sub(r'\bh(\d)', r'bk-h\1', w['use']))


def pt(tok): return f'{SCALE[tok]["pt"]:g}pt'


def s_type(P):
    out = ''
    weights = [TT['weight'][k] for k in ('regular', 'semibold', 'bold', 'extrabold')]
    ws = ''.join(f'<li class="c2"><span class="s" style="font-weight:{w["value"]}">Unit 12</span><b>{w["value"]} {w["name"]}</b><span class="u">{esc(weight_use(w))}</span></li>' for w in weights)
    stack = ', '.join(TT['family']['sans']['stack'])
    woff = T['type']['variableWoff2']
    spec = f'''<figure>
        <div class="g8 fam">
          <div class="c5"><p class="w">{esc(TT['family']['sans']['name'])}</p><p class="a">ABCDEFGHIJKLMNOPQRSTUVWXYZ<br>abcdefghijklmnopqrstuvwxyz<br>0123456789 &nbsp;.,:;·?&amp;%#()</p></div>
          {mc([('family', v(TT['family']['sans']['name'])), ('weights', v(' '.join(str(w['value']) for w in weights))), ('italic', '<span class="v">none, at any weight</span>'), ('stack', v(stack)), ('file', v(short(woff), woff))])}
        </div>
        <ul class="g8 wts">{ws}</ul>
        {P.cap('Montserrat. One family, three brands, four weights.')}
      </figure>'''
    out += P.subsec('Family', nb(f'One typeface for every word in the house. Four weights and nothing else. {sentence({3: "three"}[TT["weight"]["maxPerPiece"]])} at most in one piece. 800 is for hero and title bands only. The kit also defines a mono face, .bk-code, for hex values, paths and code. This page marks those strings with the class and sets them in Montserrat.'), spec)
    rows = ''
    for t in TT['scale']:
        caps = t['tracking'] is None
        trv = t['capsTracking'] if caps else t['tracking']
        tr = '0' if not trv else f'{trv:+.3f}'.replace('-', '−')
        st = f"--fs:{t['px']}px;line-height:{t['leading']};font-weight:{t['weight']};letter-spacing:{trv}em" + (';text-transform:uppercase' if caps else '')
        if t['cssClamp']: st += f";--fl:{t['cssClamp']}"
        rows += f'''<tr>
            <th scope="row">{v('bk-' + t['token'], cls='tok')}<span class="u">{esc(TYPE_USE[t['token']])}</span></th>
            <td class="s"><span style="{st}">{SAMPLES[t['token']]}</span></td>
            <td data-l="px">{t['px']}</td><td data-l="pt">{t['pt']:g}</td><td data-l="Weight">{t['weight']}</td><td data-l="Leading">{t['leading']:.2f}</td><td data-l="Tracking">{tr}</td>
          </tr>'''
    count = {12: 'Twelve'}[len(TT['scale'])]
    wide = f'''<figure>
        <table class="scale"><thead><tr><th scope="col">Token, the class name</th><td class="s">Specimen, at real size</td><td>px</td><td>pt</td><td>Weight</td><td>Leading</td><td>Tracking, em</td></tr></thead><tbody>{rows}</tbody></table>
        <div class="grid"><div class="main">{P.cap(f'The type scale. {count} steps, identical in all three kits.')}</div></div>
      </figure>'''
    out += P.subsec('Scale', f'{count} steps. Three sizes above body at most in one piece. This page sets its text at 12, 14, 16, 20 and 40.', '', wide, railnote=False)
    sp = TT['space']
    sq = ''.join(f'<li><span class="q" style="width:{val}px;height:{val}px"></span><b>{val}</b>{v(f"--space-{i + 1}", cls="tk")}</li>' for i, val in enumerate(sp['steps']))
    m = TT['measure']; od = TT['weight']['onDark']
    setting = [f'Uppercase is always tracked and never longer than {({4: "four"})[TT["composition"]["capsMaxWords"]]} words.', 'Flush left, ragged right. Never justify. Never center past three lines.',
               f'On a dark ground, add {od["trackingBonusEm"]}em tracking and drop one weight at 700 or heavier. {od["weightFloor"]} is the floor.',
               f'Space above a heading is three times the space below it. {sp["aboveHeading"]} above, {sp["belowHeading"]} below.',
               f'A body line stops at {m["body"]["realChars"]} characters, {m["body"]["ch"]}ch. Captions {m["caption"]["ch"]}ch. Headings {m["heading"]["ch"]}ch.',
               f'Corners are square. Diagram nodes take {T["radius"]["md"]}. Shadow signals elevation only.']
    fig = f'''<figure>
        <div class="field space"><ol>{sq}</ol></div>
        {P.cap(f'The spacing scale in pixels, drawn at actual size. Every vertical value is a multiple of {sp["base"]}.')}
      </figure>
      {P.rules(setting, 'lines cols2')}'''
    out += P.subsec('Setting and space', f'Ten spacing steps on a base of {sp["base"]}, and the six rules that decide most pages.', fig)
    return out


# ------------------------------------------------------------------ 04 in use
def status(k, w): return f'<span class="st {k}"><span class="dot"></span>{w}</span>'
def used(pairs, cls='used'):
    return f'<span class="{cls}">' + ''.join(f'<span><b>{a}</b>{v(c)}</span>' for a, c in pairs) + '</span>'


def s_use(P):
    d = PG['onePager']; m = PG['memo']; s = PG['deck']; out = ''
    date = PG['sampleDate']
    hl = LOGO_SRC['horizontal-on-dark']
    lw = 204 if IS_PARENT else 154
    band_logo = f'<img src="{hl}" alt="{esc(NAME)}" style="width:calc(var(--e)*{lw / 16})">'
    mm = DOC_FACTS['memoMargin']; om = DOC_FACTS['onePagerMargin']; dk = DOC_FACTS['deckMargins']; dm = dk['leftIn']
    tpl = DOC_FACTS['templates']
    def foot(text):
        if IS_PARENT: return f'<div class="x-foot"><span>{text}</span><span>Page 1 of 1</span></div>'
        return f'<div class="x-foot">{powered()}<span>{text} · Page 1 of 1</span></div>'
    acts = ''.join(f'<li><span>{i + 1}</span>{esc(a)}</li>' for i, a in enumerate(m['acts']))
    once = '' if IS_PARENT else ' The Powered by lockup sits once, in the footer.'
    memo = f'''<figure>
        <div class="frame"><article class="x-doc" style="--mx:{mm * 6:g}">
          <header class="x-band"><p class="x-bt">Memo</p>{band_logo}</header>
          <div class="x-body">
            <div class="x-to"><span>To</span><b>{m['to']}</b><span>From</span><b>{m['frm']}</b><span>Date</span><b>{date}</b><span>Re</span><b class="re">{m['re']}</b></div>
            {''.join(f'<p class="x-p">{p}</p>' for p in m['ps'])}
            <h4 class="x-h3">Actions.</h4>
            <ol class="x-ol">{acts}</ol>
            <p class="x-sign"><b>{m['sign'][0]}</b><span>{m['sign'][1]}</span></p>
          </div>
          {foot(m['foot'])}
        </article></div>
        {P.cap(f'Memo, US Letter, {inch(mm)} margins. Drawn at 816 by 1056, scaled to fit. Sample content.' + once)}
      </figure>'''
    meta = ''.join(f'<div><span>{k}</span><b>{val}</b></div>' for k, val in d['meta'])
    th = ''.join(f'<th scope="col">{t}</th>' for t in d['th'])
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r[:-1]) + f'<td>{status(*r[-1])}</td></tr>' for r in d['rows'])
    onep = f'''<figure>
        <div class="frame"><article class="x-doc" style="--mx:{om * 6:g}">
          <header class="x-band"><p class="x-bt">{d['band']}</p>{band_logo}</header>
          <div class="x-body">
            <h4 class="x-h1">{d['h1']}</h4>
            <p class="x-lead">{d['lead']}</p>
            <div class="x-meta">{meta}</div>
            <h5 class="x-h3">{d['h2a']}</h5>
            <p class="x-p">{d['pa']}</p>
            <h5 class="x-h3">{d['h2b']}</h5>
            <table class="x-table"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>
            <p class="x-call">{d['close']}</p>
          </div>
          {foot(d['foot'])}
        </article></div>
        {P.cap(f'One-pager, US Letter, {inch(om)} margins. Drawn at 816 by 1056, scaled to fit. Sample content.' + once)}
      </figure>'''
    note = f'Both open on the band. The logo sits once, in the band. Body runs on white at a {TT["measure"]["body"]["realChars"]} character measure. The memo carries no headline. The one-pager states its finding in one.'
    for t in tpl.values(): assert os.path.exists(os.path.join(KIT, t)), t
    u = used([('Band title', 'bk-h2'), ('Headline', 'bk-h1'), ('Lead', 'bk-body-lg'), ('Subhead', 'bk-h3'), ('Body', 'bk-body'), ('Table', 'bk-body-sm'), ('Footer', 'bk-caption'),
              ('Memo margin', inch(mm)), ('One-pager margin', inch(om)), ('Memo template', tpl['memo']), ('One-pager template', tpl['one-pager'])], 'used wide')
    out += P.subsec('Memo and one-pager', note, u, f'<div class="pair">{memo}{onep}</div>', railnote=False)
    t1 = f'''<figure>
        <div class="frame"><article class="x-slide title" style="--mx:{dm * 6:g};--mt:{dk['topIn'] * 6:g};--mb:{dk['bottomIn'] * 6:g}">
          <img class="lg" src="{hl}" alt="{esc(NAME)}" style="width:calc(var(--e)*{(260 if IS_PARENT else 200) / 16})">
          <div class="mid"><p class="x-dt">{s['title']}</p><p class="x-ds">{s['sub']}</p></div>
          <div class="ft"><span>{esc(NAME)}</span><span>{s['date']}</span></div>
        </article></div>
        {P.cap('Title slide, 16:9. Drawn at 1280 by 720, scaled to fit.' + (' The one other place true black appears.' if resolve('--bg-inverse').upper() == '#000000' else '') + ' Sample content.')}
      </figure>'''
    pts = ''.join(f'<li>{p}</li>' for p in s['pts'])
    th = ''.join(f'<th scope="col">{t}</th>' for t in s['th'])
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in s['rows'])
    mark = LOGO_SRC.get('compact-on-light') or LOGO_SRC['horizontal-on-light']
    t2 = f'''<figure>
        <div class="frame"><article class="x-slide body" style="--mx:{dm * 6:g};--mt:{dk['topIn'] * 6:g};--mb:{dk['bottomIn'] * 6:g}">
          <h4 class="x-st">{s['h']}</h4>
          <div class="cols">
            <ul class="x-pts">{pts}</ul>
            <div><p class="x-tc">{s['cap']}</p><table class="x-table big"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>
          </div>
          <div class="ft"><img src="{mark}" alt="{esc(NAME)}" style="width:calc(var(--e)*{PG['deckMarkWidth'] / 16})"><span>2</span></div>
        </article></div>
        {P.cap(f'Content slide, 16:9, on white. Body at {pt(DOC_FACTS["deckBody"])}. Sample content.')}
      </figure>'''
    body = 'bk-' + DOC_FACTS['deckBody']
    assert dk['leftIn'] == dk['rightIn']
    margin = f"{inch(dk['topIn'])} top, {inch(dk['leftIn'])} left and right, {inch(dk['bottomIn'])} bottom"
    u = used([('Title', 'bk-display-lg'), ('Subtitle', 'bk-h3'), ('Finding', 'bk-display-md'), ('Key point', 'bk-h3'), ('Body', body), ('Table', body), ('Footer', 'bk-body'), ('Slide', '13.333in by 7.5in'),
              ('Margin', margin), ('Template', tpl['deck'])], 'used wide')
    note = (f'Content slides are white. The dark ground is for the title, divider and closing slides. Body is {pt(DOC_FACTS["deckBody"])} in every brand. Uppercase is for the title slide only, four words at most, always tracked. '
            'A content slide states its finding in sentence case, with one table and no decoration.' + ('' if IS_PARENT else ' The Powered by lockup sits once, on the closing slide.'))
    out += P.subsec('Deck', note, u, f'<div class="stack">{t1}{t2}</div>', railnote=False)
    return out


# ------------------------------------------------------------------ 05 rules
def two_lists(P, a_title, a, b_title, b):
    return f'<div class="pair rules"><div><h4>{a_title}</h4>{P.rules(a)}</div><div><h4>{b_title}</h4>{P.rules(b)}</div></div>'


def s_rules(P):
    out = P.subsec('Use and avoid', 'Every rule on this page carries one number, R01 onward. Cite the number.', two_lists(P, 'Use', PG['rules']['use'], 'Avoid', PG['rules']['avoid']))
    out += P.subsec('Voice', esc('. '.join(PG['character']) + '.'), P.rules(PG['voice'], 'lines cols2'))
    return out


# ------------------------------------------------------------------ 06 co-brand
def s_cobrand(P):
    cb = REG['cobrand']; pt_ = PG['partner']; out = ''
    lt = cb['labelType']
    label = f'{lt["fontWeight"]}, caps, {lt["fontSize"].split(", ")[1].split(" ")[0]}, {float(lt["tracking"].split(", ")[1].replace("em", "")):g}em'
    floor = re.search(r'(\d+px) minimum', LOCKUP['widthNote']).group(1)
    rows = ''
    for pl in pt_['plates']:
        ground = pl['ground']; bd = REG['brands'][pl['brand']]
        src = asset(pl['brand'], bd['logos'][pl['role']])
        cel = LOCKUP['on-dark' if ground == 'dark' else 'on-light']
        pc = 'c3 plate dark' if ground == 'dark' else 'c3 plate'
        st = f' style="background:{U(bd["color"]["bandBackground"])}"' if ground == 'dark' else ''
        rows += f'''
        <div class="g8 row">
          <div class="{pc}"{st}>
            <div class="lk"><img src="{src}" alt="{esc(bd['name'])}" style="width:{pl['width']}px">
            {powered(ground)}</div>
          </div>
          <div class="c2 tx"><b>{esc(pl['label'])}</b>{esc(pl['text'])}</div>
          {mc([('class', v(cb['classes'][ground])), ('file', v(short(cel), cel)), ('width', v(LOCKUP['width'])), ('floor', f'<span class="v">{floor}, not a target</span>'), ('label', f'<span class="v">{label}</span>')])}
        </div>'''
    tbl = f'''<div class="tbl lockrow">
        <div class="g8 hd"><span class="c3">The lockup, beside the {'partner' if IS_PARENT else 'brand'} mark</span><span class="c2">Ground</span><span class="c3">Class, file, size</span></div>{rows}
      </div>'''
    out += P.subsec('The lockup', esc(pt_['note']), tbl + two_lists(P, 'Where it goes', cb['placement'], 'Do not', cb['doNot']))
    rows = ''
    marks = PARENT_REG['cobrandMarks']
    for w in pt_['wedge']:
        p = w['partner']
        if p:
            fl, fd = marks[p]['on-light'], marks[p]['on-dark']
            rl, rd = f'cobrandMarks.{p}.on-light', f'cobrandMarks.{p}.on-dark'
            hx = U(REG['brands'][p]['wedgeHue']); st = f' style="background:{U(REG["brands"][p]["color"]["bandBackground"])}"'
        else:
            fl, fd = PARENT_REG['logos']['mark-on-light'], PARENT_REG['logos']['mark-on-dark']
            rl, rd = 'mark-on-light', 'mark-on-dark'
            hx = U(resolve('--wedge-standalone')); st = ''
        ul, ud = PARENT_REG['cdnRoot'] + fl, PARENT_REG['cdnRoot'] + fd
        rows += f'''
        <div class="g8 row">
          <div class="c3 duo"><div class="plate"><img src="{asset(PARENT, fl)}" alt="{esc(PARENT_REG['name'])} block mark, on light"></div><div class="plate dark"{st}><img src="{asset(PARENT, fd)}" alt="{esc(PARENT_REG['name'])} block mark, on dark"></div></div>
          <div class="c2 tx"><b>{esc(w['label'])}</b>The wedge is {v(hx)}.</div>
          {mc([('light', v(rl)), ('file', v(short(ul), ul)), ('dark', v(rd)), ('file', v(short(ud), ud))])}
        </div>'''
    tbl = f'''<div class="tbl wedge">
        <div class="g8 hd"><span class="c3">Block mark, on light and on dark</span><span class="c2">Wedge</span><span class="c3">Role and file</span></div>{rows}
      </div>'''
    out += P.subsec('The wedge', esc(pt_['wedgeNote']), tbl)
    return out


# ------------------------------------------------------------------ 07 agents
def s_agents(P):
    out = ''
    def rows(items, numbered=True, copyname=False):
        o = ''
        for i, (n, t, u) in enumerate(items):
            nm = v(n, cls='nm') if copyname else esc(n)
            dd = ('<span class="d">' + t + '</span>') if t else ''
            o += f'<li class="grid"><div class="rail"><span class="i">{i + 1 if numbered else ""}</span><div><b>{nm}</b>{dd}</div></div><div class="main">{v(u)}</div></li>'
        return f'<ol class="full urls">{o}</ol>'
    ent = [('Registry', 'All three brands in one file.', CDNROOT + 'brands.json'), ('Agent page', 'The shortest correct path. With Layout, it wins on documents.', CDNROOT + 'for-agents/README.md'),
           ('Skill', 'The full standard. It wins on logo, color and voice.', CDNROOT + 'SKILL.md'), ('Layout', 'Page sizes, margins and what goes where.', CDNROOT + 'reference/layout.md'),
           ('Data color', 'Chart and status color, with the reasoning.', CDNROOT + 'reference/data-color.md'), ('Tokens', 'Palette, semantic colors and radius, as data.', CDNROOT + ME['tokensJson']),
           ('Type tokens', 'The type scale as data.', REG['shared']['typeTokensJson'])]
    if DOCS is not None: ent.insert(3, ('Documents', 'Every document type, as data.', CDNROOT + 'documents.json'))
    for _, _, u in ent:
        if u.startswith(CDNROOT): assert os.path.exists(os.path.join(KIT, u[len(CDNROOT):])), u
    out += f'''
  <div class="grid sub">
    {P.subhead('What an agent reads')}
    <div class="main"><p class="note">{esc(PG['agentLine'])} An agent reads these live, in this order, on every request. Public on jsDelivr. No auth, no install.</p></div>
    {rows(ent)}
  </div>'''
    css = [('type-system.css', 'House type system. Identical for all three brands.', REG['shared']['typeSystemCss']), ('palette.css', 'The only stylesheet that differs by brand.', CDNROOT + ME['paletteCss']),
           ('cobrand.css', 'The Powered by lockup.', REG['cobrand']['css']), ('data-color.css', 'Only when the page has a chart or a reported number.', T['dataColorCss'])]
    out += f'''
  <div class="grid sub">
    {P.subhead('Load order')}
    <div class="main"><p class="note">Four stylesheets, in this order, for anything built as HTML. Style through the bk classes and the fg, bg and border variables. The names are identical in all three brands.</p></div>
    {rows(css)}
  </div>'''
    lg = [(role, '', url) for role, url in LOGOS.items()]
    out += f'''
  <div class="grid sub">
    {P.subhead('Logos by role')}
    <div class="main"><p class="note">Ask for a role, never a filename. Filenames differ between brands. The role names its ground: on-light goes on a light background, on-dark on a dark one. Place the file as it ships. Never recolor it.</p></div>
    {rows(lg, numbered=False, copyname=True)}
  </div>'''
    return out


# ------------------------------------------------------------------ page
SECTIONS = [('01', 'Logo', 'Lockups, grounds, clear space', 'brands.json'),
            ('02', 'Color', 'Palette, neutrals, alerts, charts', 'tokens.json'),
            ('03', 'Type', 'Montserrat, the scale, spacing', 'snippets/type-tokens.json'),
            ('04', 'In use', 'A memo, a one-pager, a deck', 'documents.json' if DOCS is not None else 'reference/layout.md'),
            ('05', 'Rules', 'Use, avoid, voice', 'SKILL.md'),
            ('06', PG['partner']['title'], 'The Powered by lockup, the wedge', 'snippets/cobrand.css'),
            ('07', 'For agents', 'Every file an agent reads, as a URL', 'for-agents/README.md')]
HOUSE_FILES = {'snippets/type-tokens.json': REG['shared']['typeTokensJson'], 'snippets/cobrand.css': REG['cobrand']['css']}
JS = '''document.addEventListener('click',function(e){var t=e.target.closest('[data-c]');if(!t)return;
var s=t.getAttribute('data-c')||t.textContent.trim(),done=function(){t.classList.add('ok');setTimeout(function(){t.classList.remove('ok')},900)};
if(navigator.clipboard&&window.isSecureContext){navigator.clipboard.writeText(s).then(done)}
else{var a=document.createElement('textarea');a.value=s;a.style.position='fixed';a.style.opacity='0';document.body.appendChild(a);a.select();try{document.execCommand('copy');done()}catch(x){}a.remove()}});'''
FONT_FILES = {f['weight']: f['file'] for f in TT['office']['requiredStaticFonts']}
KIND = 'Parent company' if IS_PARENT else sentence(ME['role'])
DESC = f'{PG["say"]} Logo, color, type, document examples and rules, with every value an agent reads.'


def stylesheet():
    css = open(os.path.join(HERE, 'manual.css'), encoding='utf-8').read()
    faces = ''
    for w, f in FONT_FILES.items():
        rel = asset(KEY, 'for-humans/fonts/static/' + f)
        faces += f'@font-face {{ font-family: "Montserrat"; src: url("{rel}") format("truetype"), url("{CDNROOT}{rel}") format("truetype"); font-weight: {w}; font-style: normal; font-display: swap; }}\n'
    css = css.replace('/*FONTS*/', faces.rstrip())
    css = css.replace('/*THEME*/', '\n'.join(f'  --{k}: {val};' for k, val in THEME.items()))
    def typ(m):
        t = SCALE[m.group(1)]
        return f'font-size: E({t["px"]}); line-height: {t["leading"]}; font-weight: {t["weight"]}; letter-spacing: {t["tracking"] or 0}em;'
    css = re.sub(r'TYPE\(([a-z0-9-]+)\);', typ, css)
    css = re.sub(r'E\(([\d.]+)\)', lambda m: f'calc(var(--e)*{float(m.group(1)) / 16:g})', css)
    return css


def head_meta():
    og = PAGES[KEY] + 'guidelines/og.png'
    title = f'{NAME} · Brand standards'
    return f'''<title>{esc(title)}</title>
<meta name="description" content="{esc(DESC)}">
<link rel="canonical" href="{PAGES[KEY]}">
<link rel="icon" href="{LOGO_SRC['mark-on-light']}" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(NAME)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(DESC)}">
<meta property="og:url" content="{PAGES[KEY]}">
<meta property="og:image" content="{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(NAME)} logo on the brand band">
<meta name="twitter:card" content="summary_large_image">'''


def build():
    P = Page(); c = PG['cover']
    nav = ''.join(f'<a href="{PAGES[k]}"{" aria-current=page" if k == KEY else ""}>{esc(REG["brands"][k]["name"])}</a>' for k in ORDER)
    toc = '<li class="g8 hd"><span class="c2">Section</span><span class="c3">What is there</span><span class="c3">What an agent reads</span></li>'
    for n, t, desc, f in SECTIONS:
        url = HOUSE_FILES.get(f) or CDNROOT + f
        if f not in HOUSE_FILES: assert os.path.exists(os.path.join(KIT, f)), f
        toc += f'<li class="g8"><a class="c2 t" href="#s{n}"><span>{n}</span>{esc(t)}</a><span class="c3 d">{desc}</span><a class="c3 f" href="{url}">{f}</a></li>'
    body = ''
    body += P.section('Logo', esc(PG['logoLead']), s_logo, 's01')
    body += P.section('Color', esc(PG['colorLead']), s_color, 's02')
    body += P.section('Type', 'Montserrat for every word. Weights 400, 600, 700 and 800. No italic, ever.', s_type, 's03')
    body += P.section('In use', 'What on brand looks like. A memo, a one-pager and a deck, built from the scale in section 03 and the colors in section 02.', s_use, 's04')
    body += P.section('Rules', 'The short list. Use, avoid, and how the brand writes.', s_rules, 's05')
    body += P.section(esc(PG['partner']['title']), esc(PG['partner']['lead']), s_cobrand, 's06')
    body += P.section('For agents', 'An agent that makes documents for the company reads the kit, not this page. These are the files it reads, as full URLs.', s_agents, 's07')
    right = f'<div class="pw"><span>The kit</span><a href="{ZIP}">Download the kit, ZIP</a></div>' if IS_PARENT else powered()
    ver = f'Version {T["version"]}'
    page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{head_meta()}
<style>
{stylesheet()}
</style>
</head>
<body class="b-{KEY}">
<a class="skip" href="#content">Skip to the standards</a>

<header class="band">
  <div class="wrap">
    <div class="grid top">
      <p class="rail">Brand standards</p>
      <nav class="main g8" aria-label="Brands"><span class="c5">{nav}</span><a class="c3 dl" href="{ZIP}">Download the kit, ZIP</a></nav>
    </div>
    <div class="grid id">
      <div class="rail meta">
        <p><b>{KIND}</b>{ver}</p>
        <p>Every value in the right-hand column is text. Click one to copy it.</p>
      </div>
      <div class="main">
        <img src="{LOGO_SRC['horizontal-on-dark']}" alt="{esc(NAME)}" style="width:{c['width']}px;margin-left:{c['nudge']}px">
        <h1 class="say">{esc(PG['say'])}</h1>
      </div>
    </div>
    <nav class="grid toc" aria-label="Contents">
      <p class="rail">Contents</p>
      <ol class="main">{toc}</ol>
    </nav>
  </div>
</header>

<main class="wrap" id="content">{body}
</main>

<footer class="wrap">
  <div class="grid colophon">
    <div class="rail"><img src="{LOGO_SRC['horizontal-on-light']}" alt="{esc(NAME)}" style="width:{c['footWidth']}px;margin-left:{c['nudge'] * c['footWidth'] / c['width']:.1f}px"></div>
    <div class="main">
      <p>{ver}. Built from tokens.json, brands.json and the snippets by guidelines/build.py.<br>Set in Montserrat 400, 600 and 700. 800 appears in specimens only.<br>Twelve columns, 24px gutters, 96px margins.</p>
      {right}
    </div>
  </div>
</footer>

<script>
{JS}
</script>
</body>
</html>
'''
    page = re.sub(r'#[0-9a-fA-F]{6}\b', lambda m: m.group(0).upper(), page)
    return mark_codes(page.replace('&#x27;', '’')), P


# The two patterns scripts/validate.py reads as a code or an identifier, rule 13: a hex, a size with its unit, a rule number, a unit number.
CODE_RE = re.compile(r'\b(?:Auth|MRN|Unit|Rev\.)(?:&nbsp;|\s)*(?:No\.?|#|:)?(?:&nbsp;|\s)*[A-Za-z0-9][A-Za-z0-9._/-]*'
                     r'|\b(?=[A-Za-z0-9._/-]*[A-Za-z])[A-Za-z0-9][A-Za-z0-9._/-]*\d{2,}[A-Za-z0-9._/-]*\b')


def mark_codes(page):
    """Wraps every code in the visible text in .bk-code, once. Tags, styles and scripts pass through untouched."""
    out = []; skip = None; depth = []          # depth: one flag per open span, True when it is a .bk-code span
    for part in re.split(r'(<[^>]+>)', page):
        if part.startswith('<'):
            m = re.match(r'<(/?)([a-zA-Z0-9]+)', part)
            if m:
                close, tag = m.group(1), m.group(2).lower()
                if tag in ('style', 'script', 'title'): skip = None if close else tag
                elif tag == 'span':
                    if close: depth and depth.pop()
                    else: depth.append('bk-code' in part)
            out.append(part)
        elif skip or any(depth) or not part.strip():
            out.append(part)
        else:
            out.append(CODE_RE.sub(lambda m: f'<span class="bk-code">{m.group(0)}</span>', part))
    return ''.join(out)


# ------------------------------------------------------------------ checks
def check(page, P):
    bad = []
    if '—' in page: bad.append('em dash')
    if re.search(r'<(em|i)[ >]', page): bad.append('em or i element')
    if re.search(r'font-style:\s*(italic|oblique)', page): bad.append('italic')
    if re.search(r'teal', page, re.I): bad.append('the word teal')
    if page.count('<h1') != 1: bad.append('h1 count')
    if set(re.findall(r'font-weight:\s*(\d+)', page)) - {'400', '600', '700', '800'}: bad.append('a weight outside 400 600 700 800')
    if re.search(r'filter:', page): bad.append('a CSS filter')
    # every hex is one the kit ships: tokens, registry, stylesheets, drawn logo fills
    known = set()
    for txt in [json.dumps(T), json.dumps(REG)] + list(CSS_TEXT.values()) + [read(p) for p in set(LOGO_SRC.values())]:
        known |= {h.upper() for h in re.findall(r'#[0-9a-fA-F]{6}\b', txt)}
    known |= {'#' + ''.join(c * 2 for c in h).upper() for h in re.findall(r'#([0-9a-fA-F]{3})\b', ' '.join(read(p) for p in set(LOGO_SRC.values())))}
    for h in sorted(set(re.findall(r'#[0-9A-F]{6}\b', page)) - known): bad.append(f'hex {h} is not in the kit')
    # every printed token and class exists in the kit's CSS
    text = re.sub(r'<style>.*?</style>|<script>.*?</script>', '', page, flags=re.S)
    text = re.sub(r'style="[^"]*"', '', text)
    for tk in sorted(set(re.findall(r'--[a-z][a-z0-9-]*', text))):
        if tk not in CSSV: bad.append(f'token {tk} is not in the kit CSS')
    for cl in sorted(set(re.findall(r'\bbk-[a-z0-9-]+', text)) | set(re.findall(r'\bce-powered[a-z-]*', text))):
        if cl not in CSS_CLASSES: bad.append(f'class {cl} is not in the kit CSS')
    # every relative path exists; every absolute URL into this kit exists
    for u in sorted(set(re.findall(r'(?:src|href)="([^"#][^"]*)"', page)) | set(re.findall(r'url\("([^"]+)"\)', page)) | set(re.findall(r'data-c="(https[^"]+)"', page)) | set(re.findall(r'>(https://cdn[^<]+)<', re.sub(r'<wbr>', '', page)))):
        rel = u[len(CDNROOT):] if u.startswith(CDNROOT) else (None if re.match(r'https?:', u) else u)
        if rel is not None and not os.path.exists(os.path.join(KIT, rel)): bad.append(f'path {rel} does not exist')
    # alt text on every image; empty alt only inside a labelled diagram or beside its own label
    for im in re.findall(r'<img [^>]*>', page):
        if 'alt="' not in im: bad.append('img without alt: ' + im[:80])
    # headings in order
    last = 0
    for h in re.findall(r'<h([1-6])', page):
        if int(h) > last + 1: bad.append(f'heading jumps from h{last} to h{h}')
        last = int(h)
    return bad


def render_og():
    chrome = next((c for c in ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
                               shutil.which('google-chrome') or '', shutil.which('chromium') or '', shutil.which('chromium-browser') or ''] if c and os.path.exists(c)), None)
    if not chrome: sys.exit('og.png needs Chrome or Chromium')
    c = PG['cover']; w = round(c['width'] * 1.15)
    faces = ''.join(f'@font-face{{font-family:"Montserrat";src:url("../for-humans/fonts/static/{f}");font-weight:{wt}}}' for wt, f in FONT_FILES.items())
    doc = f'''<!doctype html><html lang="en"><meta charset="utf-8"><style>{faces}
*{{margin:0;box-sizing:border-box}}html,body{{width:1200px;height:630px;overflow:hidden}}
body{{background:{U(THEME['band'])};border-bottom:6px solid {U(THEME['band-rule'])};color:#FFFFFF;font-family:"Montserrat";padding:72px 96px 66px;display:flex;flex-direction:column;-webkit-font-smoothing:antialiased}}
img{{display:block;width:{w}px;margin-left:{c['nudge'] * 1.15:.0f}px}}
p{{margin-top:auto;display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid {THEME['odb']};padding-top:24px;font-size:32px;line-height:1.25;font-weight:600;letter-spacing:-0.003em}}
span{{font-weight:400;color:{U(THEME['od2'])}}}
</style><body><img src="../{LOGO_SRC['horizontal-on-dark']}" alt=""><p>{esc(NAME)}<span>Brand standards</span></p></body></html>'''
    tmp = os.path.join(HERE, '.og.html'); out = os.path.join(HERE, 'og.png')
    open(tmp, 'w', encoding='utf-8').write(doc)
    try:
        subprocess.run([chrome, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1', '--allow-file-access-from-files',
                        '--window-size=1200,630', f'--screenshot={out}', 'file://' + tmp], capture_output=True, timeout=120)
    finally:
        os.remove(tmp)
    print('guidelines/og.png')


if __name__ == '__main__':
    page, P = build()
    bad = check(page, P)
    if bad:
        print('\n'.join('FAIL  ' + b for b in bad)); sys.exit(1)
    if '--check' not in sys.argv:
        open(os.path.join(KIT, 'index.html'), 'w', encoding='utf-8').write(page)
    print(f'{KEY}  index.html  {len(page)} bytes  {P.sec} sections  {P.fig} figures  {P.r} rules  version {T["version"]}')
    if '--og' in sys.argv: render_og()
