#!/usr/bin/env python3
"""Build the letterhead as a Word file. Identical in every brand kit.

Usage:
    python3 scripts/build-letterhead.py
    python3 scripts/build-letterhead.py --facts FILE.json --out FILE.docx

It reads documents.json types.letter for the page, the slots and the spacing,
brandFacts.<brand> for the logo width and the footer line, brands.json for the
logo file, and tokens.json for the two text colors. It writes
brandFacts.<brand>.letterFile.

The file is the letter of reference/layout.md section 15 with bracketed text
in every slot. Each bracketed line is one paragraph holding one run. It opens
in Word and converts to Google Docs unchanged: one section, one named style,
an inline logo, proportional line spacing, a one-line footer. No header, text
box, table, tab stop or page field.

--facts builds the same page for a brand that has no public kit. The file
holds name, logo (a PNG path beside it), logoWidthIn and footer.

Needs python-docx.
"""

import argparse
import datetime
import json
import os
import sys

from docx import Document
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = "Montserrat"

# The bracketed text of the ready file, by slot. A list is one paragraph each.
PLACEHOLDER = {
    "date": "[Date, as 16 November 2026]",
    "recipient": ["[Recipient name]", "[Title]", "[Organization]", "[Street address]", "[City, State ZIP]"],
    "subject": "Re: [Subject. Delete this line if there is none]",
    "salutation": "Dear [Name],",
    "body": ["[Write the letter here. The first paragraph states why you are writing.]",
             "[Copy this paragraph to add another. One page holds three.]"],
    "closing": "Sincerely,",
    "sign-name": "[Your name]",
    "sign-title": "[Your title]",
}


def load(name):
    with open(os.path.join(KIT, name), encoding="utf-8") as f:
        return json.load(f)


def set_font(element):
    """Name the face on a style or a run and drop every theme font attribute."""
    rfonts = element.get_or_add_rPr().get_or_add_rFonts()
    for attr in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        rfonts.attrib.pop(qn("w:" + attr), None)
    for attr in ("ascii", "hAnsi", "cs", "eastAsia"):
        rfonts.set(qn("w:" + attr), FONT)


def this_brand(brands):
    """The brand this kit belongs to, from the repository name in brands.json."""
    kit_name = os.path.basename(KIT)
    for key, entry in brands["brands"].items():
        if entry["repo"].split("/")[-1] == kit_name:
            return key, entry
    sys.exit("build-letterhead: no brand in brands.json has the repo " + kit_name)


def build(spec, steps, colors, name, logo, logo_width_in, footer_line, out):
    slots = {s["name"]: s for s in spec["slots"]}
    doc = Document()

    section = doc.sections[0]
    section.page_width = Inches(spec["page"]["widthIn"])
    section.page_height = Inches(spec["page"]["heightIn"])
    m = spec["margins"]
    section.top_margin = Inches(m["topIn"])
    section.bottom_margin = Inches(m["bottomIn"])
    section.left_margin = Inches(m["leftIn"])
    section.right_margin = Inches(m["rightIn"])
    section.header_distance = Inches(m["footerDistanceIn"])
    section.footer_distance = Inches(m["footerDistanceIn"])
    section.different_first_page_header_footer = False

    body = slots["body"]
    normal = doc.styles["Normal"]
    set_font(normal.element)
    normal.font.size = Pt(steps[body["step"]]["pt"])
    normal.font.bold = False
    normal.font.color.rgb = RGBColor.from_string(colors[body["color"]])
    fmt = normal.paragraph_format
    fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    fmt.line_spacing = float(body["lineSpacing"])
    fmt.space_before = Pt(0)
    fmt.space_after = Pt(body["spaceAfterPt"])
    fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
    fmt.widow_control = True

    def para(p, text, slot, after=None, keep=False):
        p.style = normal
        fmt = p.paragraph_format
        fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        fmt.line_spacing = float(slot["lineSpacing"])
        fmt.space_before = Pt(slot["spaceBeforePt"])
        fmt.space_after = Pt(slot["spaceAfterPt"] if after is None else after)
        fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fmt.keep_with_next = keep
        run = p.add_run(text)
        set_font(run._r)
        run.font.size = Pt(steps[slot["step"]]["pt"])
        run.font.bold = slot["weight"] >= 700
        run.font.color.rgb = RGBColor.from_string(colors[slot["color"]])
        return p

    # Logo. The first paragraph, inline.
    p = doc.paragraphs[0] if doc.paragraphs else doc.add_paragraph()
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    p.paragraph_format.line_spacing = float(spec["logo"]["lineSpacing"])
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(spec["logo"]["spaceAfterPt"])
    picture = p.add_run().add_picture(logo, width=Inches(logo_width_in))
    # No spacing around the inline picture. Left unset, LibreOffice pads it
    # and the logo sits about 9pt inside the text edge in a PDF it makes.
    for side in ("distT", "distB", "distL", "distR"):
        picture._inline.set(side, "0")

    para(doc.add_paragraph(), PLACEHOLDER["date"], slots["date"])
    lines = PLACEHOLDER["recipient"]
    for i, line in enumerate(lines):
        last = i == len(lines) - 1
        para(doc.add_paragraph(), line, slots["recipient"],
             slots["recipient"]["lastLineSpaceAfterPt"] if last else None)
    para(doc.add_paragraph(), PLACEHOLDER["subject"], slots["subject"])
    para(doc.add_paragraph(), PLACEHOLDER["salutation"], slots["salutation"])
    for text in PLACEHOLDER["body"]:
        para(doc.add_paragraph(), text, slots["body"])
    para(doc.add_paragraph(), PLACEHOLDER["closing"], slots["closing"], keep=True)
    para(doc.add_paragraph(), PLACEHOLDER["sign-name"], slots["sign-name"], keep=True)
    para(doc.add_paragraph(), PLACEHOLDER["sign-title"], slots["sign-title"])

    # Footer. One left-aligned line on every page. The text only.
    para(section.footer.paragraphs[0], footer_line, slots["footer"])

    props = doc.core_properties
    props.title = name + " letterhead"
    props.author = name
    props.last_modified_by = name
    props.comments = "reference/layout.md section 15 · documents.json types.letter"
    stamp = datetime.datetime(2026, 11, 16)
    props.created = stamp
    props.modified = stamp

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    doc.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--facts", help="JSON with name, logo, logoWidthIn and footer, for a brand with no public kit")
    ap.add_argument("--out", help="Where to write the file. Required with --facts")
    args = ap.parse_args()

    docs = load("documents.json")
    spec = docs["types"]["letter"]
    steps = docs["steps"]
    tokens = load("tokens.json")
    colors = {name: tokens["foreground"][name.lstrip("-")]["hex"].lstrip("#") for name in ("--fg-1", "--fg-3")}

    if args.facts:
        if not args.out:
            ap.error("--facts needs --out")
        with open(args.facts, encoding="utf-8") as f:
            facts = json.load(f)
        base = os.path.dirname(os.path.abspath(args.facts))
        out = build(spec, steps, colors, facts["name"], os.path.join(base, facts["logo"]),
                    facts["logoWidthIn"], facts["footer"], args.out)
    else:
        key, entry = this_brand(load("brands.json"))
        facts = docs["brandFacts"][key]
        logo = os.path.join(KIT, entry["logosPng"][facts["letterLogoRole"]])
        out = build(spec, steps, colors, entry["name"], logo, facts["letterLogoWidthIn"],
                    facts["letterFooter"], args.out or os.path.join(KIT, facts["letterFile"]))
    print("wrote", os.path.relpath(out))


if __name__ == "__main__":
    main()
