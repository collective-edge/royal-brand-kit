#!/usr/bin/env python3
"""HOUSE DATA COLOUR v1.0 · palette gate.

Shared, byte-identical in every kit. Proves that a set of data colours is
readable before it ships. Colour is computable, so it is computed here rather
than argued about in review.

Usage:
    python3 validate-palette.py --series                 # the house set, both grounds
    python3 validate-palette.py --series --mode dark
    python3 validate-palette.py "#572e72,#1a9d4b,#d42320"
    python3 validate-palette.py "#a,#b" --pairs all      # scatter, bubble, map
    python3 validate-palette.py "#a,#b" --ordinal        # a single-hue ramp
    python3 validate-palette.py "#a,#b" --surface "#2f193b" --mode dark
    python3 validate-palette.py --series --json

What it checks, for a categorical set:

  1. Lightness band    OKLCH L inside the band for the mode.
  2. Chroma floor      OKLCH C >= 0.10. Below that a hue reads as grey and
                       stops doing identity work.
  3. CVD separation    OKLab dE x100 >= 8 on the worst pair, under protanopia
                       and deuteranopia simulated with Machado 2009 at
                       severity 1.0. 6 to 8 is a floor band, legal only when
                       the chart also carries labels, gaps or texture.
  4. Normal vision     OKLab dE x100 >= 15 on the worst pair, unsimulated.
                       A hard gate. Below it, readers with full colour vision
                       cannot separate the pair either.
  5. Contrast          >= 3:1 against the ground. Below that is legal only
                       with direct labels or a table view beside the chart.

  --ordinal swaps 1 to 5 for the ramp checks: monotone lightness, an adjacent
  step gap of at least 0.06, a lightest step clearing 2:1, and a single hue.

Pairs:
    adjacent (default)  only neighbouring slots touch. Bars, stacks, lines.
    all                 any two marks can sit side by side. Scatter, bubble,
                        choropleth, small multiples. A strictly harder test.

Exit codes:
    0  no hard failure. A floor-band CVD warning or a sub-3:1 contrast
       warning still exits 0 and obliges a second channel.
    1  at least one hard failure.
    2  bad input.
"""

import argparse
import json
import math
import re
import sys

# ---- the standard ----------------------------------------------------------

# OKLCH L. The dark band sits higher than a general dark-mode band because
# the house dark grounds are brand bands, not near-black: Apex #1D225E carries
# twice the relative luminance of a typical dark surface. A mark needs more
# lightness to clear contrast on it.
BAND = {"light": (0.43, 0.77), "dark": (0.60, 0.83)}
CHROMA_FLOOR = 0.10                                     # OKLCH C
CVD_TARGET, CVD_FLOOR = 8.0, 6.0                        # OKLab dE x100
NORMAL_FLOOR = 15.0                                     # OKLab dE x100
CONTRAST_FLOOR = 3.0                                    # WCAG, non-text
ORDINAL_LIGHT_FLOOR = 2.0
ORDINAL_STEP = 0.06

DEFAULT_SURFACE = {"light": "#FFFFFF", "dark": "#2f193b"}

# Machado, Oliveira and Fernandes 2009, severity 1.0.
MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868),
               (0.114503, 0.786281, 0.099216),
               (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968),
               (0.280085, 0.672501, 0.047413),
               (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779),
               (-0.078411, 0.930809, 0.147602),
               (0.004733, 0.691367, 0.303900)),
}

# The house series order. Keep in step with snippets/data-color.css.
SERIES = {
    "light": ["#572e72", "#1a9d4b", "#dca821", "#d42320",
              "#1a97a3", "#e6811c", "#116dce", "#e53975"],
    "dark":  ["#be6df2", "#1ba04d", "#f3ba26", "#e6443a",
              "#22b6c4", "#f78b1f", "#519dfa", "#fb608e"],
}

# Documented, measured exceptions to the band check. Surfaced on every run
# rather than hidden, so the reason stays visible to whoever reads the output.
EXCEPTIONS = {
    "#572e72": "Royal Purple, series slot 1. Sits at L 0.387, below the light "
               "band, because the brand value is fixed and is not restepped. "
               "It clears every other gate and measures 10.30:1 on white, the "
               "highest contrast in the set.",
}

HEX_RE = re.compile(r"^#?[0-9a-fA-F]{6}$")

# ---- colour ----------------------------------------------------------------


def _parse(h):
    h = h.strip()
    if not HEX_RE.match(h):
        sys.stderr.write("error: not a 6-digit hex colour: %r\n" % h)
        raise SystemExit(2)
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def _s2lin(c):
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def _lin(h):
    return tuple(_s2lin(c) for c in _parse(h))


def _oklab_from_lin(rgb):
    r, g, b = rgb
    l = (0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3)
    m = (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3)
    s = (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3)
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)


def oklch(h):
    L, a, b = _oklab_from_lin(_lin(h))
    return L, math.hypot(a, b), (math.degrees(math.atan2(b, a)) % 360)


def rel_lum(h):
    r, g, b = _lin(h)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    hi, lo = sorted((rel_lum(a), rel_lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def _simulate(h, kind):
    r, g, b = _lin(h)
    M = MACHADO[kind]
    return tuple(min(1.0, max(0.0, M[i][0] * r + M[i][1] * g + M[i][2] * b))
                 for i in range(3))


def delta_e(h1, h2, kind=None):
    a = _oklab_from_lin(_simulate(h1, kind) if kind else _lin(h1))
    b = _oklab_from_lin(_simulate(h2, kind) if kind else _lin(h2))
    return 100 * math.dist(a, b)


def _pairlist(n, mode):
    if mode == "all":
        return [(i, j) for i in range(n) for j in range(i + 1, n)]
    return [(i, i + 1) for i in range(n - 1)]


# ---- checks ----------------------------------------------------------------


def validate(palette, mode="light", surface=None, pairs="adjacent"):
    surface = surface or DEFAULT_SURFACE[mode]
    lo, hi = BAND[mode]
    report, hard_fail = [], False

    off = [(c, round(oklch(c)[0], 3)) for c in palette
           if not lo <= oklch(c)[0] <= hi]
    waived = [c for c, _ in off if c.lower() in EXCEPTIONS]
    real = [x for x in off if x[0].lower() not in EXCEPTIONS]
    if real:
        hard_fail = True
    if real:
        detail = "outside band: %s" % real
    elif waived:
        detail = ("all %d inside L %s to %s, except documented: %s"
                  % (len(palette), lo, hi, ", ".join(waived)))
    else:
        detail = "all %d inside L %s to %s" % (len(palette), lo, hi)
    report.append(("Lightness band", "FAIL" if real else
                   "WARN" if waived else "PASS", detail))

    low = [(c, round(oklch(c)[1], 3)) for c in palette
           if oklch(c)[1] < CHROMA_FLOOR]
    if low:
        hard_fail = True
    report.append(("Chroma floor", "FAIL" if low else "PASS",
                   "below floor, reads grey: %s" % low if low
                   else "all %d >= %s" % (len(palette), CHROMA_FLOOR)))

    pl = _pairlist(len(palette), pairs)
    if pl:
        worst_cvd, wc = None, None
        for i, j in pl:
            d = min(delta_e(palette[i], palette[j], "protan"),
                    delta_e(palette[i], palette[j], "deutan"))
            if worst_cvd is None or d < worst_cvd:
                worst_cvd, wc = d, (palette[i], palette[j])
        state = ("PASS" if worst_cvd >= CVD_TARGET
                 else "WARN" if worst_cvd >= CVD_FLOOR else "FAIL")
        if state == "FAIL":
            hard_fail = True
        tri = delta_e(wc[0], wc[1], "tritan")
        report.append(("CVD separation", state,
                       "worst %s pair %s vs %s dE %.1f (red-green) · tritan %.1f%s"
                       % (pairs, wc[0], wc[1], worst_cvd, tri,
                          "" if state == "PASS" else
                          " · floor band, needs labels, gaps or texture"
                          if state == "WARN" else " · below %.0f" % CVD_FLOOR)))

        worst_n, wn = None, None
        for i, j in pl:
            d = delta_e(palette[i], palette[j])
            if worst_n is None or d < worst_n:
                worst_n, wn = d, (palette[i], palette[j])
        ok_n = worst_n >= NORMAL_FLOOR
        if not ok_n:
            hard_fail = True
        report.append(("Normal vision", "PASS" if ok_n else "FAIL",
                       "worst %s pair %s vs %s dE %.1f%s"
                       % (pairs, wn[0], wn[1], worst_n,
                          "" if ok_n else
                          " · below %.0f, hard to separate with full colour vision"
                          % NORMAL_FLOOR)))

    thin = [(c, round(contrast(c, surface), 2)) for c in palette
            if contrast(c, surface) < CONTRAST_FLOOR]
    report.append(("Contrast vs ground", "WARN" if thin else "PASS",
                   "below %.0f:1, needs direct labels or a table: %s"
                   % (CONTRAST_FLOOR, thin) if thin
                   else "all %d >= %.0f:1 on %s"
                   % (len(palette), CONTRAST_FLOOR, surface)))

    return report, not hard_fail


def validate_ordinal(palette, mode="light", surface=None):
    surface = surface or DEFAULT_SURFACE[mode]
    report, hard_fail = [], False
    ls = [oklch(c)[0] for c in palette]

    desc = all(b < a for a, b in zip(ls, ls[1:]))
    asc = all(b > a for a, b in zip(ls, ls[1:]))
    mono = desc or asc
    if not mono:
        hard_fail = True
    report.append(("Lightness monotone", "PASS" if mono else "FAIL",
                   "steps read %s" % ("light to dark" if desc else "dark to light")
                   if mono else "lightness is not monotone: %s"
                   % [round(x, 3) for x in ls]))

    gaps = [round(abs(b - a), 3) for a, b in zip(ls, ls[1:])]
    tight = [g for g in gaps if g < ORDINAL_STEP]
    if tight:
        hard_fail = True
    report.append(("Adjacent step", "FAIL" if tight else "PASS",
                   "gaps below %s: %s" % (ORDINAL_STEP, tight) if tight
                   else "all gaps >= %s" % ORDINAL_STEP))

    lightest = max(palette, key=rel_lum)
    cr = contrast(lightest, surface)
    ok = cr >= ORDINAL_LIGHT_FLOOR
    if not ok:
        hard_fail = True
    report.append(("Light-end contrast", "PASS" if ok else "FAIL",
                   "%s at %.2f:1 vs %s%s" % (lightest, cr, surface,
                   "" if ok else " · below %.1f:1. Fine for a continuous scale, "
                   "not for discrete ordered marks" % ORDINAL_LIGHT_FLOOR)))

    hues = [oklch(c)[2] for c in palette]
    spread = max(hues) - min(hues)
    spread = min(spread, 360 - spread)
    one = spread <= 20
    if not one:
        hard_fail = True
    report.append(("Single hue", "PASS" if one else "FAIL",
                   "hue spread %.0f degrees" % spread))

    return report, not hard_fail


# ---- output ----------------------------------------------------------------

GLYPH = {"PASS": "ok  ", "WARN": "warn", "FAIL": "FAIL"}


def emit(report, ok, palette, mode, surface, pairs, ordinal):
    kind = "ordinal ramp" if ordinal else "categorical, %s pairs" % pairs
    print("\n%s · %s · ground %s · %d colours"
          % (kind, mode, surface, len(palette)))
    print("  " + "  ".join(palette))
    print()
    for name, state, detail in report:
        print("  [%s] %-20s %s" % (GLYPH[state], name, detail))
    noted = sorted({c for c in palette if c.lower() in EXCEPTIONS})
    for c in noted:
        print("\n  note · %s: %s" % (c, EXCEPTIONS[c]))
    print("\n  %s\n" % ("PASSED" if ok else "FAILED · fix the marked checks"))


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("palette", nargs="?",
                    help='comma separated hex, e.g. "#572e72,#1a9d4b"')
    ap.add_argument("--series", action="store_true",
                    help="validate the house series order instead")
    ap.add_argument("--mode", choices=("light", "dark"), default="light")
    ap.add_argument("--surface", help="ground to measure contrast against")
    ap.add_argument("--pairs", choices=("adjacent", "all"), default="adjacent")
    ap.add_argument("--ordinal", action="store_true",
                    help="check as a single-hue ramp")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.series:
        modes = [args.mode] if args.mode else ["light", "dark"]
        modes = ["light", "dark"] if "--mode" not in sys.argv else [args.mode]
        results, all_ok = [], True
        for m in modes:
            surface = args.surface or DEFAULT_SURFACE[m]
            rep, ok = validate(SERIES[m], m, surface, args.pairs)
            all_ok = all_ok and ok
            results.append((SERIES[m], m, surface, rep, ok))
        if args.json:
            print(json.dumps([{"mode": m, "surface": s, "palette": p,
                               "ok": ok,
                               "report": [{"check": c, "state": st,
                                           "detail": d} for c, st, d in rep]}
                              for p, m, s, rep, ok in results], indent=2))
        else:
            for p, m, s, rep, ok in results:
                emit(rep, ok, p, m, s, args.pairs, False)
        raise SystemExit(0 if all_ok else 1)

    if not args.palette:
        ap.error("give a palette, or --series")

    palette = [c if c.startswith("#") else "#" + c
               for c in (x.strip() for x in args.palette.split(",")) if c]
    if len(palette) < 2:
        sys.stderr.write("error: need at least two colours\n")
        raise SystemExit(2)

    surface = args.surface or DEFAULT_SURFACE[args.mode]
    if args.ordinal:
        rep, ok = validate_ordinal(palette, args.mode, surface)
    else:
        rep, ok = validate(palette, args.mode, surface, args.pairs)

    if args.json:
        print(json.dumps({"mode": args.mode, "surface": surface,
                          "palette": palette, "ok": ok,
                          "report": [{"check": c, "state": s, "detail": d}
                                     for c, s, d in rep]}, indent=2))
    else:
        emit(rep, ok, palette, args.mode, surface, args.pairs, args.ordinal)
    raise SystemExit(0 if ok else 1)


if __name__ == "__main__":
    main()
