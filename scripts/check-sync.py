#!/usr/bin/env python3
"""HOUSE TYPE SYSTEM v1.0 · drift check.

Usage:
    python3 check-sync.py
    python3 check-sync.py --json
    python3 check-sync.py --reference /path/to/collective-edge-brand-kit

Asserts four things about the kit this script sits in:

  1. The seventeen shared files are byte-identical to the copies in the
     collective-edge-brand-kit sibling directory. The type layer is never forked.
  2. snippets/palette.css defines every variable in the semantic contract, so a
     component written for one brand renders in another with only that file swapped.
  3. Every scale row in snippets/type-tokens.json resolves to a matching
     --fs- / --lh- / --tr- token in snippets/type-system.css, at the same value,
     so the JSON and the CSS cannot drift.
  4. tokens.json has the same key structure as the tokens.json in the other
     kits it can find beside it. Same keys, values may differ. A list may be
     any length, including empty; every object inside one list has the keys
     its counterparts have.

Exit codes:
    0  pass
    1  at least one mismatch
    2  a file needed for the check is missing or unparseable
"""

import argparse
import hashlib
import json
import os
import re
import sys

SHARED_FILES = [
    "reference/type-system.md",
    "reference/ui.md",
    "reference/data-color.md",
    "NEW-BRAND.md",
    "brands.json",
    "documents.json",
    "snippets/type-system.css",
    "snippets/type-tokens.json",
    "snippets/cobrand.css",
    "snippets/ui.css",
    "snippets/data-color.css",
    "Examples/ui-controls.html",
    "Examples/data-color.html",
    "scripts/validate.py",
    "scripts/validate-palette.py",
    "scripts/check-sync.py",
    "scripts/ui-audit.py",
]

SEMANTIC_CONTRACT = [
    "--fg-1", "--fg-2", "--fg-3", "--fg-4", "--fg-accent",
    "--fg-on-dark-1", "--fg-on-dark-2", "--fg-on-dark-3",
    "--bg-canvas", "--bg-surface", "--bg-elevated", "--bg-inverse", "--bg-band",
    "--border-1", "--border-2", "--border-on-dark", "--border-band-rule",
    "--bg-surface-2", "--bg-mid",
]

# The functional families every palette.css carries under identical names:
# the shared neutrals, the alert family with its five steps, the aliases
# that older pages read, and the brand's sequential ramp for data-color.css.
SEMANTIC_CONTRACT += ["--neutral-%s" % n for n in (
    "ink", "secondary", "tertiary", "dimmed", "border", "hairline",
    "tint", "tint-2", "mid", "on-dark-body", "on-dark-caption")]
SEMANTIC_CONTRACT += ["--alert-%s%s" % (n, step)
                      for n in ("go", "warn", "stop", "info")
                      for step in ("", "-text", "-tint", "-on-tint", "-on-dark")]
SEMANTIC_CONTRACT += ["--status-%s" % n for n in ("go", "warn", "stop", "info")]
SEMANTIC_CONTRACT += ["--diagram-%s" % n for n in (
    "decision", "decision-text", "decision-border",
    "warning", "warning-text", "warning-border",
    "process", "process-text", "process-border", "connector")]
SEMANTIC_CONTRACT += ["--brand-seq-%s%d" % (g, n)
                      for g in ("", "dark-") for n in range(100, 800, 100)]

REFERENCE_KIT = "collective-edge-brand-kit"
SISTER_KITS = ["collective-edge-brand-kit", "apex-brand-kit", "royal-brand-kit"]
COLOR_TOKENS = "tokens.json"
PALETTE = "snippets/palette.css"
TOKENS = "snippets/type-tokens.json"
TYPE_CSS = "snippets/type-system.css"

NESTED_AT = {"media", "supports", "document", "layer", "scope", "container"}
VAR_DEF_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:", re.M)
VAR_REF_RE = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")


def fail(msg):
    sys.stderr.write("error: %s\n" % msg)
    raise SystemExit(2)


def read(path):
    try:
        with open(path, "rb") as fh:
            return fh.read()
    except OSError as exc:
        fail("cannot read %s · %s" % (path, exc))


def digest(blob):
    return hashlib.md5(blob).hexdigest()


def blank_comments(css):
    out = list(css)
    for m in re.finditer(r"/\*.*?\*/", css, re.S):
        for k in range(m.start(), m.end()):
            if out[k] != "\n":
                out[k] = " "
    return "".join(out)


def parse_blocks(css, out):
    """Flatten a stylesheet to (selector, body) pairs, descending into @media."""
    n = len(css)
    i = 0
    start = 0
    while i < n:
        ch = css[i]
        if ch == "{":
            prelude = css[start:i].strip()
            j = i + 1
            depth = 1
            while j < n and depth:
                if css[j] == "{":
                    depth += 1
                elif css[j] == "}":
                    depth -= 1
                j += 1
            body = css[i + 1: j - 1] if depth == 0 else css[i + 1:]
            at = re.match(r"@([A-Za-z-]+)", prelude)
            if at and at.group(1).lower() in NESTED_AT:
                parse_blocks(body, out)
            elif prelude:
                out.append((prelude, body))
            i = j
            start = j
        elif ch == "}":
            i += 1
            start = i
        else:
            i += 1
    return out


def declared_vars(css):
    """Map every custom property to its last declared value."""
    values = {}
    for _, body in parse_blocks(css, []):
        for decl in body.split(";"):
            m = VAR_DEF_RE.match(decl.strip())
            if m:
                values[m.group(1)] = decl.strip()[len(m.group(0)):].strip()
    return values


def class_rules(css):
    """Map .bk-<token> to its own declarations, for tokens with no 1:1 variable."""
    rules = {}
    for selector, body in parse_blocks(css, []):
        for part in selector.split(","):
            part = part.strip()
            if re.match(r"^\.bk-[A-Za-z0-9-]+$", part):
                rules.setdefault(part, []).append(body)
    return rules


def norm(value):
    return re.sub(r"\s+", "", value or "")


def as_number(value):
    m = re.match(r"^\s*([-+]?\d*\.?\d+)\s*(em)?\s*$", value or "")
    return float(m.group(1)) if m else None


def resolve(token, prefix, prop, css_vars, rules):
    """Return (variable_name, value) for a scale row, direct or via its .bk- class."""
    name = "%s-%s" % (prefix, token)
    if name in css_vars:
        return name, css_vars[name]
    # The class may set the property directly, or declare the value on a custom
    # property that a later shared rule applies. Tracking uses the second form so
    # that --tr-dark can be inherited from .bk-on-dark, see type-system.css §10.
    indirect = {"letter-spacing": "--tr"}.get(prop)
    for body in rules.get(".bk-%s" % token, []):
        for target in (prop, indirect):
            if not target:
                continue
            m = re.search(r"(?<![-\w])%s\s*:\s*var\(\s*(--[A-Za-z0-9_-]+)"
                          % re.escape(target), body)
            if m and m.group(1) in css_vars:
                return m.group(1), css_vars[m.group(1)]
    return None, None


def key_shape(node, path="", out=None):
    """Flatten a JSON value to the set of its key paths.

    An object contributes one path per key. A list contributes "[]" and the
    keys of the objects inside it, merged, so two lists of different lengths
    compare equal when their items are built alike. An empty list contributes
    nothing below itself and is skipped by the comparison.
    """
    if out is None:
        out = set()
    if isinstance(node, dict):
        for key, value in node.items():
            child = "%s.%s" % (path, key) if path else key
            out.add(child)
            key_shape(value, child, out)
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, (dict, list)):
                key_shape(item, path + "[]", out)
    return out


def empty_lists(node, path="", out=None):
    """Paths of the lists that hold no object, so their items cannot be compared."""
    if out is None:
        out = set()
    if isinstance(node, dict):
        for key, value in node.items():
            empty_lists(value, "%s.%s" % (path, key) if path else key, out)
    elif isinstance(node, list):
        if not any(isinstance(item, (dict, list)) for item in node):
            out.add(path + "[]")
        for item in node:
            empty_lists(item, path + "[]", out)
    return out


def ragged_lists(node, path="", out=None):
    """Lists whose own objects do not share one set of keys."""
    if out is None:
        out = []
    if isinstance(node, dict):
        for key, value in node.items():
            ragged_lists(value, "%s.%s" % (path, key) if path else key, out)
    elif isinstance(node, list):
        dicts = [item for item in node if isinstance(item, dict)]
        if dicts and any(set(d) != set(dicts[0]) for d in dicts[1:]):
            out.append(path + "[]")
        for item in node:
            ragged_lists(item, path + "[]", out)
    return out


def shape_diff(mine, theirs):
    """Key paths present on one side only, ignoring the items of an empty list."""
    skip = tuple(p + "." for p in empty_lists(mine) | empty_lists(theirs))
    a = set(p for p in key_shape(mine) if not p.startswith(skip))
    b = set(p for p in key_shape(theirs) if not p.startswith(skip))
    return sorted(a - b), sorted(b - a)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check-sync.py",
        description="House type system v1.0 · assert the shared layer has not drifted.",
    )
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--reference", default=None, help="path to the collective-edge-brand-kit")
    args = parser.parse_args(argv)

    kit = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    kit_name = os.path.basename(kit)
    ref = os.path.abspath(args.reference) if args.reference else os.path.join(
        os.path.dirname(kit), REFERENCE_KIT)
    if not os.path.isdir(ref):
        fail("reference kit not found at %s" % ref)
    is_reference = os.path.realpath(ref) == os.path.realpath(kit)

    checks = []
    failures = []

    def record(group, name, ok, detail):
        checks.append({"group": group, "name": name, "ok": ok, "detail": detail})
        if not ok:
            failures.append("%s · %s · %s" % (group, name, detail))

    # 1. shared files, byte for byte
    for rel in SHARED_FILES:
        mine_path = os.path.join(kit, rel)
        theirs_path = os.path.join(ref, rel)
        if not os.path.isfile(mine_path):
            record("shared", rel, False, "missing from %s" % kit_name)
            continue
        if not os.path.isfile(theirs_path):
            record("shared", rel, False, "missing from %s" % REFERENCE_KIT)
            continue
        mine = read(mine_path)
        theirs = read(theirs_path)
        if is_reference:
            record("shared", rel, True, "%s · reference kit" % digest(mine)[:8])
        elif mine == theirs:
            record("shared", rel, True, digest(mine)[:8])
        else:
            record("shared", rel, False,
                   "%s differs from %s · %s vs %s · never fork the shared layer"
                   % (rel, REFERENCE_KIT, digest(mine)[:8], digest(theirs)[:8]))

    # 2. semantic contract
    palette_path = os.path.join(kit, PALETTE)
    if not os.path.isfile(palette_path):
        record("palette", PALETTE, False, "missing from %s" % kit_name)
    else:
        palette = blank_comments(read(palette_path).decode("utf-8"))
        defined = set(VAR_DEF_RE.findall(palette))
        missing = [v for v in SEMANTIC_CONTRACT if v not in defined]
        if missing:
            record("palette", PALETTE, False,
                   "%s does not define %s" % (PALETTE, " ".join(missing)))
        else:
            record("palette", PALETTE, True,
                   "%d of %d contract variables defined" % (len(SEMANTIC_CONTRACT), len(SEMANTIC_CONTRACT)))

    # 3. tokens against the CSS
    tokens_path = os.path.join(kit, TOKENS)
    css_path = os.path.join(kit, TYPE_CSS)
    if not os.path.isfile(tokens_path) or not os.path.isfile(css_path):
        record("scale", TOKENS, False, "%s or %s missing from %s" % (TOKENS, TYPE_CSS, kit_name))
    else:
        try:
            spec = json.loads(read(tokens_path).decode("utf-8"))
        except ValueError as exc:
            fail("%s is not valid JSON · %s" % (TOKENS, exc))
        css = blank_comments(read(css_path).decode("utf-8"))
        css_vars = declared_vars(css)
        rules = class_rules(css)
        resolved = 0
        for row in spec.get("scale", []):
            token = row.get("token")
            wanted = {
                "--fs": ("font-size", row.get("cssClamp") or "%gpx" % row.get("px"), norm),
                "--lh": ("line-height", row.get("leading"), as_number),
                "--tr": ("letter-spacing", row.get("tracking"), as_number),
            }
            for prefix, (prop, expected, cast) in wanted.items():
                name, value = resolve(token, prefix, prop, css_vars, rules)
                if name is None:
                    record("scale", "%s-%s" % (prefix, token), False,
                           "%s declares scale row %s but %s defines no %s-%s and .bk-%s resolves none"
                           % (TOKENS, token, TYPE_CSS, prefix, token, token))
                    continue
                resolved += 1
                if expected is None:
                    continue
                got = cast(value)
                want = cast(expected if isinstance(expected, str) else "%g" % expected)
                if got is None or want is None or got != want:
                    record("scale", "%s-%s" % (prefix, token), False,
                           "%s says %s = %s, %s says %s = %s"
                           % (TOKENS, token, expected, TYPE_CSS, name, value.strip()))
        if not any(c["group"] == "scale" and not c["ok"] for c in checks):
            record("scale", "scale rows", True,
                   "%d rows · %d tokens resolved" % (len(spec.get("scale", [])), resolved))

    # 4. tokens.json, one key structure across the kits
    mine_tokens_path = os.path.join(kit, COLOR_TOKENS)
    if not os.path.isfile(mine_tokens_path):
        record("tokens", COLOR_TOKENS, False, "missing from %s" % kit_name)
    else:
        try:
            mine_tokens = json.loads(read(mine_tokens_path).decode("utf-8"))
        except ValueError as exc:
            fail("%s is not valid JSON · %s" % (COLOR_TOKENS, exc))
        ragged = ragged_lists(mine_tokens)
        if ragged:
            record("tokens", COLOR_TOKENS, False,
                   "objects inside %s do not share one set of keys" % " ".join(ragged))
        siblings = [ref] if not is_reference else []
        for name in SISTER_KITS:
            other = os.path.join(os.path.dirname(kit), name)
            if (os.path.realpath(other) != os.path.realpath(kit)
                    and os.path.realpath(other) not in [os.path.realpath(x) for x in siblings]
                    and os.path.isfile(os.path.join(other, COLOR_TOKENS))):
                siblings.append(other)
        if not siblings:
            record("tokens", COLOR_TOKENS, True, "no sister kit beside this one · nothing to compare")
        for other in siblings:
            other_name = os.path.basename(other)
            other_path = os.path.join(other, COLOR_TOKENS)
            if not os.path.isfile(other_path):
                record("tokens", "vs %s" % other_name, False, "%s missing from %s" % (COLOR_TOKENS, other_name))
                continue
            try:
                theirs_tokens = json.loads(read(other_path).decode("utf-8"))
            except ValueError as exc:
                fail("%s in %s is not valid JSON · %s" % (COLOR_TOKENS, other_name, exc))
            only_mine, only_theirs = shape_diff(mine_tokens, theirs_tokens)
            if only_mine or only_theirs:
                parts = []
                if only_mine:
                    parts.append("only in %s: %s" % (kit_name, " ".join(only_mine[:8])
                                 + (" and %d more" % (len(only_mine) - 8) if len(only_mine) > 8 else "")))
                if only_theirs:
                    parts.append("only in %s: %s" % (other_name, " ".join(only_theirs[:8])
                                 + (" and %d more" % (len(only_theirs) - 8) if len(only_theirs) > 8 else "")))
                record("tokens", "vs %s" % other_name, False,
                       "key structure differs · %s" % " · ".join(parts))
            else:
                record("tokens", "vs %s" % other_name, True,
                       "%d key paths, same structure" % len(key_shape(mine_tokens)))

    if args.json:
        sys.stdout.write(json.dumps({
            "kit": kit,
            "reference": ref,
            "referenceKit": is_reference,
            "checks": checks,
            "failures": failures,
            "ok": not failures,
        }, indent=2, ensure_ascii=False) + "\n")
    else:
        print("check-sync · %s" % kit_name)
        for group, heading in (
            ("shared", "shared files vs %s" % REFERENCE_KIT),
            ("palette", "semantic contract"),
            ("scale", "scale sync · %s vs %s" % (TOKENS, TYPE_CSS)),
            ("tokens", "%s · one key structure in every kit" % COLOR_TOKENS),
        ):
            rows = [c for c in checks if c["group"] == group]
            if not rows:
                continue
            print("  %s" % heading)
            for row in rows:
                print("    %-4s %-34s %s" % ("OK" if row["ok"] else "FAIL", row["name"], row["detail"]))
        print("PASS" if not failures else "FAIL · %d problem%s" % (
            len(failures), "" if len(failures) == 1 else "s"))

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
