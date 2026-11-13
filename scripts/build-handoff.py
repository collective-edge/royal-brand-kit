#!/usr/bin/env python3
"""Build the binary half of for-humans/ from for-humans/pack.json.

Usage:
    python3 scripts/build-handoff.py
    python3 scripts/build-handoff.py --out /tmp/preview-pack
    python3 scripts/build-handoff.py --only swatches

Reads for-humans/pack.json in the kit this script sits in and writes:

  logos/svg/        the master SVGs from assets/logos/, renamed for a person
  logos/png/        transparent PNG exports at the widths the pack lists
  previews/         each logo on the ground it is for, as shown in the README
  previews/swatches one chip per brand color
  previews/data     one chip per house data color, read from snippets/data-color.css
  fonts/            the variable font, copied from assets/fonts/

The prose in for-humans/README.md is written by hand. Nothing here touches it.

Rendering uses headless Chrome or Chromium, because it is the one SVG renderer
that is on every machine that builds this kit. Swatches need Pillow. Set CHROME
to the binary if it is not in a standard place.

Exit codes:
    0  built
    2  a needed file or tool is missing
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)

CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


def fail(msg):
    sys.stderr.write("error: %s\n" % msg)
    raise SystemExit(2)


def find_chrome():
    for c in CHROME_CANDIDATES:
        if not c:
            continue
        if os.path.isfile(c) or shutil.which(c):
            return c
    fail("no Chrome or Chromium found. Set CHROME=/path/to/binary")


def viewbox(svg_path):
    with open(svg_path, encoding="utf-8") as fh:
        m = re.search(r'viewBox="([^"]+)"', fh.read())
    if not m:
        fail("no viewBox in %s" % svg_path)
    x, y, w, h = [float(v) for v in m.group(1).replace(",", " ").split()]
    return w, h


def shoot(chrome, html, out, width, height):
    """Screenshot an HTML string at exactly width x height, transparent ground."""
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "page.html")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(html)
        cmd = [
            chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1",
            "--default-background-color=00000000",
            "--user-data-dir=%s" % os.path.join(tmp, "profile"),
            "--window-size=%d,%d" % (width, height),
            "--screenshot=%s" % out,
            "file://" + page,
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0 or not os.path.isfile(out):
            fail("Chrome could not render %s\n%s" % (out, res.stderr.decode()[-400:]))
    # Chrome can hand back a frame a few pixels off the asked size. Hold the contract.
    from PIL import Image
    im = Image.open(out)
    if im.size != (width, height):
        im = im.crop((0, 0, width, height))
        im.save(out)


PAGE = """<!doctype html><meta charset="utf-8">
<style>html,body{margin:0;padding:0;background:transparent;overflow:hidden}
.plate{width:%(w)dpx;height:%(h)dpx;display:flex;align-items:center;justify-content:center;
background:%(bg)s;border-radius:%(r)dpx;box-sizing:border-box;%(border)s}
img{display:block;width:%(lw)dpx;height:auto}</style>
<div class="plate"><img src="file://%(src)s"></div>"""


def build_logos(pack, out, chrome):
    svg_dir = os.path.join(out, "logos", "svg")
    png_dir = os.path.join(out, "logos", "png")
    prev_dir = os.path.join(out, "previews")
    for d in (svg_dir, png_dir, prev_dir):
        os.makedirs(d, exist_ok=True)
    grounds = pack["grounds"]
    for logo in pack["logos"]:
        src = os.path.join(KIT, logo["source"])
        if not os.path.isfile(src):
            fail("missing %s" % src)
        name = "%s-%s" % (pack["filePrefix"], logo["name"])
        shutil.copyfile(src, os.path.join(svg_dir, name + ".svg"))
        vw, vh = viewbox(src)
        for width in logo["png"]:
            height = int(round(width * vh / vw))
            html = PAGE % dict(w=width, h=height, bg="transparent", r=0, border="",
                               lw=width, src=src)
            shoot(chrome, html, os.path.join(png_dir, "%s-%dw.png" % (name, width)),
                  width, height)
        pw, ph = logo["preview"]["plate"]
        ground = grounds[logo["ground"]]
        border = "border:2px solid %s;" % pack["previewBorder"] if logo["ground"] == "light" else ""
        html = PAGE % dict(w=pw, h=ph, bg=ground, r=24, border=border,
                           lw=logo["preview"]["logoWidth"], src=src)
        shoot(chrome, html, os.path.join(prev_dir, logo["name"] + ".png"), pw, ph)
        print("logo      %s" % name)


def chip(hex_value, path):
    from PIL import Image, ImageDraw
    h = hex_value.lstrip("#")
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    im = Image.new("RGB", (64, 64), rgb)
    # A pale chip disappears into a white page. Give it an edge.
    lum = (0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]) / 255
    if lum > 0.80:
        ImageDraw.Draw(im).rectangle([0, 0, 63, 63], outline=(203, 213, 225), width=2)
    im.save(path)


def build_swatches(pack, out):
    d = os.path.join(out, "previews", "swatches")
    os.makedirs(d, exist_ok=True)
    for hex_value in pack["swatches"]:
        chip(hex_value, os.path.join(d, hex_value.lstrip("#") + ".png"))
    print("swatches  %d" % len(pack["swatches"]))


def build_data(out):
    """Data chips come from the shared stylesheet, so they cannot drift from it."""
    css_path = os.path.join(KIT, "snippets", "data-color.css")
    with open(css_path, encoding="utf-8") as fh:
        css = fh.read()
    light = css.split("{", 1)[1]
    d = os.path.join(out, "previews", "data")
    os.makedirs(d, exist_ok=True)
    n = 0
    for i in range(1, 9):
        m = re.search(r"--series-%d:\s*(#[0-9a-fA-F]{6})" % i, light)
        if not m:
            fail("no --series-%d in %s" % (i, css_path))
        chip(m.group(1), os.path.join(d, "series-%d.png" % i))
        n += 1
    for role in ("favorable", "unfavorable", "caution", "neutral"):
        m = re.search(r"--dir-%s:\s*(#[0-9a-fA-F]{6})" % role, light)
        if not m:
            fail("no --dir-%s in %s" % (role, css_path))
        chip(m.group(1), os.path.join(d, "dir-%s.png" % role))
        n += 1
    print("data      %d" % n)


def build_fonts(pack, out):
    d = os.path.join(out, "fonts")
    os.makedirs(d, exist_ok=True)
    for rel in pack.get("fonts", []):
        src = os.path.join(KIT, rel)
        if not os.path.isfile(src):
            fail("missing %s" % src)
        shutil.copyfile(src, os.path.join(d, os.path.basename(rel)))
    print("fonts     %d" % len(pack.get("fonts", [])))


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", help="write somewhere other than for-humans/")
    ap.add_argument("--only", choices=["logos", "swatches", "data", "fonts"])
    args = ap.parse_args()

    pack_path = os.path.join(KIT, "for-humans", "pack.json")
    try:
        with open(pack_path, encoding="utf-8") as fh:
            pack = json.load(fh)
    except (OSError, ValueError) as exc:
        fail("cannot read %s · %s" % (pack_path, exc))

    out = os.path.abspath(args.out) if args.out else os.path.join(KIT, "for-humans")
    os.makedirs(out, exist_ok=True)

    if args.only in (None, "logos"):
        build_logos(pack, out, find_chrome())
    if args.only in (None, "swatches"):
        build_swatches(pack, out)
    if args.only in (None, "data"):
        build_data(out)
    if args.only in (None, "fonts"):
        build_fonts(pack, out)
    print("built     %s" % out)


if __name__ == "__main__":
    main()
