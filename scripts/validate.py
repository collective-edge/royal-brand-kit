#!/usr/bin/env python3
"""HOUSE TYPE SYSTEM v1.0 · mechanical validator.

Usage:
    python3 validate.py FILE.html [FILE2.html ...]
    python3 validate.py --json FILE.html
    python3 validate.py --quiet FILE.html

Checks generated HTML and its CSS against the mechanically checkable rules in
reference/type-system.md. Allowed values load from ../snippets/type-tokens.json.
Nothing about the type ladder is hardcoded here.

Rules checked:
    R1   no italic, at any weight, in any brand
    R2   weights 400 / 600 / 700 / 800 only
    R5   tracking in em, never px or pt
    R9   body measure, 54ch, never above 60ch, never unset
    R10  text-wrap balance on headings, pretty on paragraphs
    R13  codes, IDs and unit numbers in the mono face
    R14  micro-typography: no em dash, curly quotes, en dash ranges, real ellipsis
         (the curly-quote check skips mono context, where a straight quote is
          the character a reader has to be able to paste)

Exit codes:
    0  clean
    1  at least one violation
    2  usage error, unreadable input, or unreadable type-tokens.json
"""

import argparse
import bisect
import json
import os
import re
import sys

TOKENS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "snippets",
    "type-tokens.json",
)

RULE_TITLES = {
    "R1": "no italic",
    "R2": "weight not in the ladder",
    "R5": "tracking in em, never px or pt",
    "R9": "body measure",
    "R10": "text-wrap balance and pretty",
    "R13": "codes in the mono face",
    "R14": "micro-typography",
}
RULE_ORDER = ["R1", "R2", "R5", "R9", "R10", "R13", "R14"]

MAX_MEASURE_CH = 60

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
RAW_TAGS = {"script", "style", "textarea"}
MONO_TAGS = {"code", "kbd", "samp", "pre", "tt"}
PARA_ELEMENTS = {"p", "li", "dd", "blockquote", "figcaption"}
PARA_CLASSES = {"bk-body", "bk-body-lg", "bk-body-sm", "bk-caption", "bk-lead"}
HEADING_ELEMENTS = {"h1", "h2", "h3", "h4", "h5", "h6"}
HEADING_CLASSES = {
    "bk-h1", "bk-h2", "bk-h3", "bk-h4",
    "bk-display-xl", "bk-display-lg", "bk-display-md",
}
TEXTISH_PROPS = {
    "font", "font-size", "font-family", "font-weight", "line-height",
    "letter-spacing", "color", "text-align", "text-wrap", "text-transform",
}
NESTED_AT = {"media", "supports", "document", "layer", "scope", "container"}

TAG_RE = re.compile(r"<(/?)([A-Za-z][A-Za-z0-9:-]*)((?:\"[^\"]*\"|'[^']*'|[^>\"'])*)>", re.S)
ATTR_RE = re.compile(
    r"([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*(?:\"([^\"]*)\"|'([^']*)'|([^\s\"'=<>`]+))"
)
COMBINATOR_RE = re.compile(r"\s*[>+~]\s*|\s+")
ITALIC_VALUE_RE = re.compile(r"\b(italic|oblique)\b", re.I)
WEIGHT_INT_RE = re.compile(r"^[1-9]00$")
LS_ABSOLUTE_RE = re.compile(r"[-+]?\d*\.?\d+\s*(px|pt)\b", re.I)
MAXW_CH_RE = re.compile(r"([-+]?\d*\.?\d+)\s*ch\b", re.I)

CODE_MIXED_RE = re.compile(r"\b(?=[A-Za-z0-9._/-]*[A-Za-z])[A-Za-z0-9][A-Za-z0-9._/-]*\d{2,}[A-Za-z0-9._/-]*\b")
CODE_LABEL_RE = re.compile(
    r"\b(Auth|MRN|Unit|Rev\.)(?:&nbsp;|\s)*(?:No\.?|#|:)?(?:&nbsp;|\s)*([A-Za-z0-9][A-Za-z0-9._/-]*)"
)

EMDASH_RE = re.compile(r"—|&mdash;|&#8212;|&#x2014;", re.I)
STRAIGHT_QUOTE_RE = re.compile(r"[\"']|&quot;|&#34;|&apos;|&#39;", re.I)
YEAR_HYPHEN_RE = re.compile(r"\b(1[89]\d{2}|20\d{2})-(1[89]\d{2}|20\d{2})\b")
DOT_ELLIPSIS_RE = re.compile(r"\.{3,}")


# ---------- tokens -------------------------------------------------------


def load_tokens(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except OSError as exc:
        sys.stderr.write("error: cannot read %s · %s\n" % (path, exc))
        raise SystemExit(2)
    except ValueError as exc:
        sys.stderr.write("error: %s is not valid JSON · %s\n" % (path, exc))
        raise SystemExit(2)


def allowed_weights(tokens):
    out = set()
    for value in tokens.get("weight", {}).values():
        if isinstance(value, dict) and isinstance(value.get("value"), int):
            out.add(value["value"])
    if not out:
        sys.stderr.write("error: type-tokens.json defines no weights\n")
        raise SystemExit(2)
    return out


def reserved_weights(tokens):
    return {w for w in tokens.get("weight", {}).get("reserved", []) or [] if isinstance(w, int)}


def mono_pattern(tokens):
    stack = tokens.get("family", {}).get("mono", {}).get("stack", []) or []
    names = {str(n).strip().lower() for n in stack if str(n).strip()}
    names |= {"monospace", "mono", "courier", "courier new", tokens.get("family", {}).get("mono", {}).get("office", "consolas").lower()}
    return re.compile("|".join(re.escape(n) for n in sorted(names, key=len, reverse=True)), re.I)


def sans_italic_names(tokens):
    name = tokens.get("family", {}).get("sans", {}).get("name", "Montserrat")
    return re.compile(r"\bitalic\b|%s\s*italic" % re.escape(name), re.I)


# ---------- source scanning ----------------------------------------------


def line_starts(src):
    return [m.start() for m in re.finditer("\n", src)]


def line_of(starts, pos):
    return bisect.bisect_right(starts, pos) + 1


def snippet(text, limit=88):
    flat = " ".join(text.split())
    if len(flat) > limit:
        flat = flat[: limit - 1] + "…"
    return flat


def scan(src):
    """Split HTML into CSS chunks, visible text chunks, italic tags and links."""
    css = []           # (text, absolute_offset, inline_selector_or_None)
    texts = []         # (text, absolute_offset, ancestor_tuple)
    italic_tags = []   # (tag, absolute_offset)
    links = []         # href strings
    stack = []
    n = len(src)
    i = 0
    while i < n:
        lt = src.find("<", i)
        if lt < 0:
            texts.append((src[i:], i, tuple(stack)))
            break
        if lt > i:
            texts.append((src[i:lt], i, tuple(stack)))
        if src.startswith("<!--", lt):
            end = src.find("-->", lt + 4)
            i = n if end < 0 else end + 3
            continue
        m = TAG_RE.match(src, lt)
        if not m:
            i = lt + 1
            continue
        closing = m.group(1) == "/"
        tag = m.group(2).lower()
        raw_attrs = m.group(3)
        self_closing = raw_attrs.rstrip().endswith("/")
        i = m.end()
        if closing:
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == tag:
                    del stack[k:]
                    break
            continue
        attrs = {}
        for a in ATTR_RE.finditer(raw_attrs):
            for g in (2, 3, 4):
                if a.group(g) is not None:
                    attrs[a.group(1).lower()] = (a.group(g), m.start(3) + a.start(g))
                    break
        classes = frozenset(attrs.get("class", ("", 0))[0].split())
        style_val, style_off = attrs.get("style", ("", 0))
        if style_val.strip():
            subject = tag + "".join("." + c for c in sorted(classes))
            css.append((style_val, style_off, subject))
        if tag == "link":
            links.append(attrs.get("href", ("", 0))[0])
        if tag in ("i", "em"):
            italic_tags.append((tag, lt))
        node = (tag, classes, style_val)
        if tag in RAW_TAGS and not self_closing:
            close = re.compile(r"</\s*%s\s*>" % tag, re.I).search(src, i)
            end = close.start() if close else n
            if tag == "style":
                css.append((src[i:end], i, None))
            i = close.end() if close else n
            continue
        if tag not in VOID_TAGS and not self_closing:
            stack.append(node)
    return css, texts, italic_tags, links


# ---------- CSS parsing ---------------------------------------------------


def blank_comments(css):
    out = list(css)
    for m in re.finditer(r"/\*.*?\*/", css, re.S):
        for k in range(m.start(), m.end()):
            if out[k] != "\n":
                out[k] = " "
    return "".join(out)


def parse_decls(body, base):
    decls = []
    depth = 0
    quote = None
    start = 0

    def emit(chunk, offset):
        lead = len(chunk) - len(chunk.lstrip())
        chunk = chunk.strip()
        if not chunk or ":" not in chunk:
            return
        prop, _, value = chunk.partition(":")
        prop = prop.strip().lower()
        if not prop or prop.startswith("@"):
            return
        decls.append((prop, value.strip(), offset + lead))

    for idx, ch in enumerate(body):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == ";" and depth == 0:
            emit(body[start:idx], base + start)
            start = idx + 1
    emit(body[start:], base + start)
    return decls


def parse_rules(css, base, out):
    n = len(css)
    i = 0
    start = 0
    while i < n:
        ch = css[i]
        if ch == "{":
            prelude = css[start:i]
            j = i + 1
            depth = 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            body = css[i + 1: j - 1] if depth == 0 else css[i + 1:]
            sel = prelude.strip()
            at = re.match(r"@([A-Za-z-]+)", sel)
            if at and at.group(1).lower() in NESTED_AT:
                parse_rules(body, base + i + 1, out)
            elif sel:
                lead = len(prelude) - len(prelude.lstrip())
                out.append({
                    "selector": sel,
                    "offset": base + start + lead,
                    "decls": parse_decls(body, base + i + 1),
                    "inline": False,
                })
            i = j
            start = j
        elif ch == "}":
            i += 1
            start = i
        else:
            i += 1
    return out


def collect_rules(css_chunks):
    rules = []
    for text, base, inline_selector in css_chunks:
        clean = blank_comments(text)
        if inline_selector is None:
            parse_rules(clean, base, rules)
        else:
            rules.append({
                "selector": inline_selector,
                "offset": base,
                "decls": parse_decls(clean, base),
                "inline": True,
            })
    return rules


def subject(sel):
    sel = sel.strip()
    if not sel or sel.startswith("@"):
        return "", frozenset()
    parts = [p for p in COMBINATOR_RE.split(sel) if p]
    if not parts:
        return "", frozenset()
    last = parts[-1]
    last = re.sub(r"::?[A-Za-z-]+(\([^)]*\))?", "", last)
    last = re.sub(r"\[[^\]]*\]", "", last)
    el = re.match(r"([A-Za-z][A-Za-z0-9-]*)", last)
    classes = frozenset(c.lower() for c in re.findall(r"\.([A-Za-z_][-A-Za-z0-9_]*)", last))
    return (el.group(1).lower() if el else ""), classes


def para_key(el, classes):
    for c in sorted(classes):
        if c in PARA_CLASSES:
            return "." + c
    if el in PARA_ELEMENTS:
        return el
    return None


def heading_key(el, classes):
    for c in sorted(classes):
        if c in HEADING_CLASSES:
            return "." + c
    if el in HEADING_ELEMENTS:
        return el
    return None


# ---------- checks --------------------------------------------------------


class Report(object):
    def __init__(self, path):
        self.path = path
        self.items = []

    def add(self, rule, line, text, message):
        self.items.append({
            "rule": rule,
            "file": self.path,
            "line": line,
            "text": snippet(text),
            "message": message,
        })


def weight_tokens(value):
    return re.findall(r"[A-Za-z0-9.%-]+", value)


def check_file(path, tokens, weights, reserved, mono_re, italic_family_re):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            src = fh.read()
    except IsADirectoryError:
        sys.stderr.write("error: %s is a directory\n" % path)
        return None
    except FileNotFoundError:
        sys.stderr.write("error: %s does not exist\n" % path)
        return None
    except OSError as exc:
        sys.stderr.write("error: cannot read %s · %s\n" % (path, exc))
        return None

    rep = Report(path)
    starts = line_starts(src)
    css_chunks, texts, italic_tags, links = scan(src)
    rules = collect_rules(css_chunks)
    kit_loaded = any("type-system.css" in (h or "") for h in links)

    wrap_heading = tokens.get("composition", {}).get("textWrapHeading", "balance")
    wrap_para = tokens.get("composition", {}).get("textWrapParagraph", "pretty")
    measure_ch = tokens.get("measure", {}).get("body", {}).get("ch", 54)

    mono_classes = set()
    mono_elements = set(MONO_TAGS)
    for rule in rules:
        for prop, value, _ in rule["decls"]:
            if prop in ("font-family", "font") and mono_re.search(value):
                for part in rule["selector"].split(","):
                    el, classes = subject(part)
                    mono_classes |= classes
                    if el:
                        mono_elements.add(el)

    para_index = {}
    head_index = {}

    for rule in rules:
        decls = rule["decls"]
        props = {p for p, _, _ in decls}

        for prop, value, off in decls:
            line = line_of(starts, off)
            decl_text = "%s: %s" % (prop, value)

            # R1
            if prop == "font-style" and ITALIC_VALUE_RE.search(value):
                rep.add("R1", line, decl_text, "italic is not in this system at any weight")
            if prop in ("font-family", "font") and italic_family_re.search(value):
                rep.add("R1", line, decl_text, "italic named in a font stack")

            # R2
            if prop == "font-weight":
                if "var(" not in value:
                    for tok in weight_tokens(value):
                        low = tok.lower()
                        if low in ("lighter", "bolder"):
                            rep.add("R2", line, decl_text, "%s is relative, call a real weight" % low)
                        elif tok.isdigit():
                            num = int(tok)
                            if num not in weights:
                                note = "reserved" if num in reserved else "not in the ladder"
                                rep.add("R2", line, decl_text, "%d is %s · use %s" % (
                                    num, note, "/".join(str(w) for w in sorted(weights))))
            if prop == "font" and "var(" not in value:
                for tok in weight_tokens(value):
                    low = tok.lower()
                    if low in ("lighter", "bolder"):
                        rep.add("R2", line, decl_text, "%s is relative, call a real weight" % low)
                    elif WEIGHT_INT_RE.match(tok) and int(tok) not in weights:
                        num = int(tok)
                        note = "reserved" if num in reserved else "not in the ladder"
                        rep.add("R2", line, decl_text, "%d in the font shorthand is %s · use %s" % (
                            num, note, "/".join(str(w) for w in sorted(weights))))

            # R5
            if prop == "letter-spacing":
                m = LS_ABSOLUTE_RE.search(value)
                if m:
                    rep.add("R5", line, decl_text,
                            "tracking in %s · an absolute unit is a different optical amount at every size, use em"
                            % m.group(1).lower())

        # R9 and R10 aggregation
        for part in rule["selector"].split(","):
            el, classes = subject(part)
            pkey = para_key(el, classes)
            hkey = heading_key(el, classes)
            textish = bool(props & TEXTISH_PROPS) or el in PARA_ELEMENTS or el in HEADING_ELEMENTS
            for key, index in ((pkey, para_index), (hkey, head_index)):
                if key is None:
                    continue
                entry = index.setdefault(key, {
                    "line": line_of(starts, rule["offset"]),
                    "selector": part.strip(),
                    "textish": False,
                    "max_width": False,
                    "wrap": set(),
                })
                entry["textish"] = entry["textish"] or textish
                for prop, value, off in decls:
                    if prop == "max-width":
                        entry["max_width"] = True
                        if pkey is not None and index is para_index:
                            line = line_of(starts, off)
                            if "none" in value.lower():
                                rep.add("R9", line, "%s { max-width: %s }" % (part.strip(), value),
                                        "body text must not run the full container width")
                            m = MAXW_CH_RE.search(value)
                            if m and float(m.group(1)) > MAX_MEASURE_CH:
                                rep.add("R9", line, "%s { max-width: %s }" % (part.strip(), value),
                                        "measure runs past %dch · body measure is %sch" % (
                                            MAX_MEASURE_CH, measure_ch))
                    if prop == "text-wrap":
                        entry["wrap"].add(value.strip().lower())

    def exempt(key):
        if not kit_loaded:
            return False
        return key.startswith(".bk-") or key in PARA_ELEMENTS or key in HEADING_ELEMENTS

    for key, entry in sorted(para_index.items()):
        if entry["textish"] and not entry["max_width"] and not exempt(key):
            rep.add("R9", entry["line"], "%s { }" % entry["selector"],
                    "body text with no max-width · set max-width: %sch" % measure_ch)
        if entry["textish"] and wrap_para not in entry["wrap"] and not exempt(key):
            rep.add("R10", entry["line"], "%s { }" % entry["selector"],
                    "paragraph rule without text-wrap: %s" % wrap_para)

    for key, entry in sorted(head_index.items()):
        if entry["textish"] and wrap_heading not in entry["wrap"] and not exempt(key):
            rep.add("R10", entry["line"], "%s { }" % entry["selector"],
                    "heading rule without text-wrap: %s" % wrap_heading)

    # R1, markup
    for tag, off in italic_tags:
        rep.add("R1", line_of(starts, off), "<%s>" % tag,
                "<%s> carries italic semantics · use .bk-emphasis at 700" % tag)

    # R13 and R14, visible text
    for text, base, ancestors in texts:
        if not text.strip():
            continue
        mono = any(
            node[0] in mono_elements
            or node[1] & mono_classes
            or "bk-code" in node[1]
            or mono_re.search(node[2] or "")
            for node in ancestors
        )
        if not mono:
            for m in CODE_MIXED_RE.finditer(text):
                rep.add("R13", line_of(starts, base + m.start()), m.group(0),
                        "code or ID in Montserrat · wrap it in .bk-code")
            for m in CODE_LABEL_RE.finditer(text):
                rep.add("R13", line_of(starts, base + m.start()), m.group(0),
                        "%s code in Montserrat · wrap the value in .bk-code" % m.group(1))
        for m in EMDASH_RE.finditer(text):
            rep.add("R14", line_of(starts, base + m.start()), context(text, m),
                    "em dash · use a period, a comma or ·")
        # Curly quotes are a prose rule. Inside a code specimen the straight
        # quote is the correct character: a snippet a reader retypes has to be
        # the string that works when they paste it. Mono context is the only
        # place in the system where that is true.
        if not mono:
            for m in STRAIGHT_QUOTE_RE.finditer(text):
                rep.add("R14", line_of(starts, base + m.start()), context(text, m),
                        "straight quote · use “ ” ’")
        for m in YEAR_HYPHEN_RE.finditer(text):
            rep.add("R14", line_of(starts, base + m.start()), m.group(0),
                    "year range on a hyphen · use an en dash –")
        for m in DOT_ELLIPSIS_RE.finditer(text):
            rep.add("R14", line_of(starts, base + m.start()), context(text, m),
                    "dots for truncation · use …")

    rep.items.sort(key=lambda d: (RULE_ORDER.index(d["rule"]), d["line"]))
    return rep


def context(text, match, span=28):
    lo = max(0, match.start() - span)
    hi = min(len(text), match.end() + span)
    return snippet(text[lo:hi])


# ---------- output --------------------------------------------------------


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate.py",
        description="House type system v1.0 · check HTML and CSS against the fifteen rules.",
    )
    parser.add_argument("files", nargs="+", metavar="FILE.html")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--quiet", action="store_true", help="no output, exit code only")
    parser.add_argument("--tokens", default=TOKENS_PATH, help="path to type-tokens.json")
    args = parser.parse_args(argv)

    tokens = load_tokens(args.tokens)
    weights = allowed_weights(tokens)
    reserved = reserved_weights(tokens)
    mono_re = mono_pattern(tokens)
    italic_family_re = sans_italic_names(tokens)

    findings = []
    read = []
    missing = []
    for path in args.files:
        rep = check_file(path, tokens, weights, reserved, mono_re, italic_family_re)
        if rep is None:
            missing.append(path)
            continue
        read.append(path)
        findings.extend(rep.items)

    grouped = {}
    for item in findings:
        grouped.setdefault(item["rule"], []).append(item)

    if args.json:
        payload = {
            "typeSystemVersion": tokens.get("version"),
            "filesChecked": read,
            "filesUnreadable": missing,
            "total": len(findings),
            "counts": {r: len(grouped.get(r, [])) for r in RULE_ORDER},
            "violations": findings,
            "ok": not findings and not missing,
        }
        sys.stdout.write(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    elif not args.quiet:
        print("type system v%s · validate · %d file%s checked"
              % (tokens.get("version", "?"), len(read), "" if len(read) == 1 else "s"))
        for rule in RULE_ORDER:
            items = grouped.get(rule)
            if not items:
                continue
            print("")
            print("%-4s %-42s %4d" % (rule, RULE_TITLES[rule], len(items)))
            for item in items:
                print("     %s:%d  %s" % (item["file"], item["line"], item["text"]))
                print("       └ %s" % item["message"])
        print("")
        if findings:
            print("%d violation%s across %d rule%s"
                  % (len(findings), "" if len(findings) == 1 else "s",
                     len(grouped), "" if len(grouped) == 1 else "s"))
        elif read:
            print("clean · 7 rules, 0 violations")
        for path in missing:
            print("unreadable: %s" % path)

    if missing:
        return 2
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
