# House type system

**Version 1.0.** This file is identical in every brand kit. Do not edit it for one brand.

Apex Paramedics and Royal Ambulance are operating companies under Collective Edge. Two things vary between brands: **palette** and **logo**. Type is the shared layer and is what makes the three read as one house. Every brand uses this document unchanged.

Use the exact values below. Do not paraphrase them, round them, or substitute a near-equivalent.

---

## 1. Load order

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/type-system.css">
<link rel="stylesheet" href="{THIS_KIT_CDN}snippets/palette.css">
```

`type-system.css` is identical in every kit and is served from the Collective Edge kit, because the type layer belongs to the parent brand. `palette.css` is the only stylesheet that differs.

Style through the `.bk-*` classes and the semantic `--fg-*` / `--bg-*` / `--border-*` variables. Reach for a raw brand color only where the brand color is the point: a logo band, an accent rule, a chart series.

For non-CSS output (PowerPoint, Word, matplotlib, reportlab) read `type-tokens.json` instead of reimplementing these values.

---

## 2. Typeface

**Montserrat. Every brand, every output, no exceptions.**

**There is no italic in this system, at any weight, in any brand.** Do not set italic. Do not synthesize an oblique. `font-synthesis: none` is set in the CSS so nothing can fake one. The Collective Edge heavy-italic signature exists only in the drawn wordmark SVG, where the letterforms are correct.

A second face appears in one place only. Montserrat’s capital I, lowercase l and figure 1 are three identical stems, and its zero and capital O are the same circle. **Any string a person retypes, dictates or reads aloud goes in the mono face:** authorization numbers, unit IDs, run numbers, policy numbers, MRNs. Use `.bk-code`. Everything else is Montserrat.

### Measured metrics

Every rule in this document derives from these, measured from the shipping variable font **at wght 400**. Measure at 400, not at the file’s default instance: Montserrat’s variable default is wght 100, and its Thin metrics are narrower than the Regular that actually sets body copy.

| Metric | Value | Consequence |
|---|---|---|
| unitsPerEm | 1000 | |
| Cap height | 0.700em | Caps read smaller than their point size |
| x-height | 0.525em | Ordinary, close to Helvetica |
| Ascender | 0.968em | |
| Descender | 0.251em | |
| **Natural line box** | **1.219em** | **No wrapping text may lead below 1.05** |
| Digit zero | 0.662em | This is the CSS `ch` unit |
| Average letter | 0.5567em | **16.7% wider than Helvetica** |
| Average running char | 0.5084em | |
| **Real chars per 1ch** | **1.302** | A measure in `ch` runs a third longer than it reads |

---

## 3. Weight

Four weights. Each has exactly one job. **Never use 100, 200, 300 or 900 at document sizes.**

| Weight | Name | Class | Job |
|---|---|---|---|
| 400 | Regular | `.bk-body`, `.bk-caption` | Body, captions, footers, table cells |
| 600 | SemiBold | `.bk-h3`, `.bk-h4`, `.bk-eyebrow` | Subheads, uppercase labels, table headers |
| 700 | Bold | `.bk-h1`, `.bk-h2`, `.bk-emphasis`, `.bk-stat` | Headings, emphasis in body, stat numerals |
| 800 | ExtraBold | `.bk-display-*` | Hero and title bands only |

**Maximum three weights in one piece. Maximum three sizes above body in one piece.**

Emphasis inside running text is 700. Never italic, never underline, never a color change alone.

### Reversed type

Light letterforms on a dark ground bloom optically: the same weight reads heavier and the counters close. Every brand opens documents with a dark header band, so this applies to nearly every deliverable.

**On any dark surface, add 0.005em tracking at every step, and drop one weight where the step is 700 or heavier.** 600 is the floor: 500 is not in the ladder, so 600 stays 600 and only gains the tracking. Put `.bk-on-dark` on the container and the CSS handles it. Display drops 800 to 700.

---

## 4. Scale

One ladder. Display steps are fluid so one token serves phone and desktop. Every desktop value converts to a whole point size. The top of the ladder is 72pt, the largest standard PowerPoint title size.

| Class | Web | Deck / Doc | Weight | Leading | Tracking | Caps tracking |
|---|---|---|---|---|---|---|
| `.bk-display-xl` | 96px | 72pt | 800 | 1.05 | −0.020em | +0.020em |
| `.bk-display-lg` | 72px | 54pt | 800 | 1.08 | −0.018em | +0.020em |
| `.bk-display-md` | 56px | 42pt | 800 | 1.10 | −0.015em | +0.025em |
| `.bk-h1` | 40px | 30pt | 700 | 1.18 | −0.012em | +0.030em |
| `.bk-h2` | 32px | 24pt | 700 | 1.25 | −0.008em | +0.040em |
| `.bk-h3` | 24px | 18pt | 600 | 1.35 | −0.004em | +0.050em |
| `.bk-h4` | 20px | 15pt | 600 | 1.45 | 0 | +0.060em |
| `.bk-body-lg` | 20px | 15pt | 400 | 1.55 | 0 | +0.060em |
| `.bk-body` | 16px | 12pt | 400 | 1.60 | 0 | +0.070em |
| `.bk-body-sm` | 14px | 10.5pt | 400 | 1.55 | +0.005em | +0.080em |
| `.bk-caption` | 12px | 9pt | 400 | 1.45 | +0.010em | +0.080em |
| `.bk-eyebrow` | 12px | 9pt | 600 | 1.45 | · | +0.080em |

**Tracking is always em, never px.** A px value is a different optical amount at every size, which is why one title rule cannot serve a one-pager and a slide.

Roman tightens as it grows. Uppercase opens as it shrinks. Uppercase is **always** tracked.

Caps labels sit at the **same** size as the body they label, never smaller. Montserrat’s caps are short against its lowercase, so an all-caps line already reads smaller than its size suggests.

---

## 5. Measure

`ch` is the width of the digit zero, not a character. In Montserrat at wght 400 **1ch buys 1.302 real characters**, so these values are smaller than the character counts they produce.

| Class / variable | Value | Real characters |
|---|---|---|
| `--measure-body` | 54ch | 70 |
| `--measure-caption` | 40ch | 52 |
| `--measure-heading` | 28ch | 36 |
| `--measure-display` | 16ch | 21 |

The classical comfortable range is 66 to 75 characters, which at wght 400 is 51ch to 58ch. `54ch` sits at 70.

Never let body text run the full width of a wide container.

---

## 6. Composition

| Rule | Value |
|---|---|
| Alignment | Flush left, ragged right |
| Justified | Never |
| Centered | Never past three lines |
| Headings | `text-wrap: balance` |
| Paragraphs | `text-wrap: pretty` |
| Print | `orphans: 3; widows: 3` |
| Heading case | Sentence case inside a document |
| Display case | Uppercase permitted on a title, band or divider surface |
| Label case | Uppercase, always tracked, never past four words |
| Body case | Never all caps |

Justified text opens rivers of white through a column, and Montserrat’s wide even letterforms make them worse than a narrower face would.

### Spacing

4px base. **Every vertical value is a multiple of 4:** 4, 8, 12, 16, 24, 32, 48, 64, 96, 128.

**Space above a heading is three times the space below it,** so the heading visibly belongs to the text it introduces rather than floating between two blocks. Defaults are 48px above, 16px below.

Paragraphs get space between them or a first-line indent. Never both.

---

## 7. Micro-typography

| Where | Wrong | Right |
|---|---|---|
| Quotation | `"Royal"` | `“Royal”` |
| Apostrophe | `crew's` | `crew’s` |
| Date range | `2024-2026` | `2024–2026` (en dash) |
| Truncation | `...` | `…` |
| Number and unit | `12 min` | `12&nbsp;min` |
| Revision marker | `Rev. 08.26` | `Rev.&nbsp;08.26` |
| Separator | `Facility \| Payer` | `Facility · Payer` |
| Em dash | any use | Never. Use a period, a comma or `·` |

**Figures.** Any column of numbers gets `font-variant-numeric: tabular-nums lining` so digits align down the column. Running prose keeps proportional figures.

**Never synthesize.** Montserrat has no small caps and no oldstyle figures. A small-caps look is 600 uppercase at body size with 0.08em tracking. Never fake bold, never fake italic. Call a real weight.

---

## 8. Content density

**A label, a value, and nothing between them.**

Do not write helper text under a field. Do not write a caption that restates the number above it. Do not add a parenthetical after a heading. Do not add a caveat sentence under a table.

If information can be carried by structure, position or a rendered example, carry it that way instead of writing a sentence about it.

Write a caption only when it carries information the thing above it does not.

---

## 9. Cross-medium

### Web

Load `type-system.css`. Use the `.bk-*` classes. Display sizes are already fluid.

### Print and PDF

The CSS ships a `@media print` block that swaps px for pt. Always include the `@font-face` declaration so the font embeds in the output. Nothing a person reads at length drops below 10.5pt. Nothing at all drops below 9pt.

### PowerPoint and Word

Office has no weight axis. It renders whatever static files are installed, so an 800 headline silently falls back to Bold when Montserrat ExtraBold is absent.

| Weight | File to install | Office menu name | Falls back to |
|---|---|---|---|
| 400 | Montserrat-Regular.ttf | Montserrat | · |
| 600 | Montserrat-SemiBold.ttf | Montserrat SemiBold | Montserrat |
| 700 | Montserrat-Bold.ttf | Montserrat | · |
| 800 | Montserrat-ExtraBold.ttf | Montserrat ExtraBold | Montserrat Bold |

Read point sizes from the Deck / Doc column in section 4, or from `type-tokens.json`.

---

## 10. The fifteen rules

Copy these into any brief. Following them literally produces correct work.

1. Montserrat everywhere. **No italic, ever, at any weight.**
2. Weights: 400 body, 600 subheads and caps labels, 700 headings and emphasis, 800 hero only. Nothing else.
3. Three weights maximum in one piece. Three sizes above body maximum.
4. On any dark ground, add 0.005em tracking at every step, and drop one weight where the step is 700 or heavier. 600 is the floor, because 500 is not in the ladder.
5. Tracking in **em**, never px. Large type negative, small caps positive.
6. Uppercase is always tracked and never longer than four words.
7. Sentence case for headings inside a document. Uppercase for display statements on a title, band or divider surface, and for labels. Always tracked, never past four words.
8. Flush left, ragged right. Never justify. Never center past three lines.
9. Body measure `max-width: 54ch` = 70 characters. Captions 40ch. Headings 28ch.
10. `text-wrap: balance` on every heading. `text-wrap: pretty` on every paragraph. `orphans: 3; widows: 3` in print.
11. Space above a heading is three times the space below it.
12. Every vertical value is a multiple of 4.
13. Codes, IDs and unit numbers set in the mono face. Never Montserrat.
14. Columns of numbers get `tabular-nums`. Curly quotes, en dashes, non-breaking spaces in units. No em dashes.
15. A label, a value, and nothing between them.

---

## 11. Verify before shipping

Run the validator on any HTML you produce:

```bash
python3 scripts/validate.py path/to/output.html
```

It checks rules 1, 2, 5, 9, 10, 13 and 14 mechanically and exits non-zero on a violation. It cannot check the rest, so also confirm by eye:

- [ ] Rendered, not just written. Open it and look. Overlap, clipping and overflow are invisible in source.
- [ ] Montserrat actually rendered, not a fallback. For PDF, actually embedded.
- [ ] No italic anywhere.
- [ ] Dark bands one weight lighter than the light-surface equivalent.
- [ ] No heading ending on a stranded word.
- [ ] Body text not running the full container width.
- [ ] Contrast holds. Body text clears 4.5:1 on its ground.
- [ ] No helper text, no restating captions, no parentheticals after headings.

State which brand choices you applied when you hand the work back.

---

## 12. Adding a brand

See `NEW-BRAND.md`. A brand is a palette and a set of marks. Everything in this document stays the same.

## 13. Versioning

`@main` serves the latest. Pin to a tag for stability: replace `@main` with `@v1.1`. Bump the minor version for additive changes, the major version when a value in section 3, 4 or 5 changes.
