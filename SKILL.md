---
name: royal-brand-guidelines
description: Applies the Royal Ambulance brand standard to any document, deck, sheet, PDF or page that carries the Royal name. Royal Ambulance is an operating company under Collective Edge. It runs purple over the shared house neutrals, with the crown wordmark. Type is Montserrat at 400, 600, 700 and 800 with no italic. Covers how to load the kit, logos by role, color, the alert family, chart color, type, the memo, one-pager and deck layouts, the “Powered by Collective Edge” lockup that appears once on every document, voice, and a pre-ship check. Use when producing or reviewing any Royal Ambulance material.
---

# Royal Ambulance · brand standard

Royal Ambulance is a Bay Area medical transportation company and an operating company under Collective Edge. Its color is purple and its mark is the crown.

Collective Edge, Apex Paramedics and Royal Ambulance share one standard. The sections, the order and the rules are the same in all three kits. Color, logo and brand facts differ. Type, layout, alert color, chart color and the co-brand lockup are shared and never forked for one brand.

This file is the whole standard in brief. The references carry the full tables: [reference/brand.md](reference/brand.md) for color, logo, co-brand and voice, [reference/layout.md](reference/layout.md) for the memo, the one-pager and the deck in inches and points, [reference/type-system.md](reference/type-system.md) for type, [reference/data-color.md](reference/data-color.md) for charts, [reference/ui.md](reference/ui.md) for controls. [reference/partner-colors.md](reference/partner-colors.md) holds partner facility colors.

## 1. Brand

| | |
|---|---|
| Role | Operating company under Collective Edge |
| Character | Written for the reader who is between calls. Short declarative sentences |
| Palette | Purple. Dark Purple is the band, Purple is the accent, Royal Purple is the logo |
| Logo | The crown and the `ROYAL AMBULANCE` wordmark. The mark is the crown |

## 2. Load

Every file is public on jsDelivr. No auth, no install. Paths in this file are relative to the kit root.

```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/
```

| File | Holds |
|---|---|
| `brands.json` | All three brands. CDN roots, logo roles, minimum sizes and the co-brand lockup. Identical in every kit |
| `tokens.json` | This brand’s colors as hex and RGB. One key structure in all three kits |
| `snippets/type-tokens.json` | The type scale, weights, measure, spacing and the static font names. Identical in every kit |
| `for-humans/logos/png/` | Transparent PNG logos, for generators that cannot place SVG |
| `for-humans/fonts/static/` | Montserrat Regular, SemiBold, Bold and ExtraBold, as static files |

**Word, PowerPoint, Excel and PDF.** Read color from `tokens.json` and type from `snippets/type-tokens.json`. Place logos as PNG. Name the family `Montserrat`, and install or register the four static files before rendering so the face embeds. `office` in `snippets/type-tokens.json` gives the menu name for each weight. If the render falls back to another face, say so when you hand the work back.

**HTML.** Four stylesheets, in this order: `snippets/type-system.css`, `snippets/palette.css`, `snippets/cobrand.css`, `snippets/data-color.css`. `palette.css` loads from this kit and is the only one that differs by brand. The other three load from the Collective Edge kit. Load `data-color.css` only when the page has a chart or a reported number. Style through the `.bk-*` classes and the `--fg-*`, `--bg-*` and `--border-*` variables. The link tags and the `@font-face` block that embeds the face in a PDF are in `for-agents/README.md`. `assets/colors.json` and `snippets/brand-base.css` predate the house type system. They still ship for pages already loading them. New work never reads them.

## 3. Logo

Ask for a role, never a filename. Filenames differ between brands. `-on-light` is the file placed on a light background. `-on-dark` is the file placed on a dark one. Royal ships no compact lockup and no app icon. Use the horizontal lockup.

| Role | SVG, in `assets/logos/` | PNG, in `for-humans/logos/png/` | Use |
|---|---|---|---|
| `horizontal-on-light` | `horizontal-purple.svg` | `Royal-Ambulance-horizontal-purple-1200w.png` | The primary lockup, on white and tints |
| `horizontal-on-dark` | `horizontal-white.svg` | `Royal-Ambulance-horizontal-white-1200w.png` | The primary lockup, on the band |
| `mark-on-light` | `crown-purple.svg` | `Royal-Ambulance-crown-purple-512w.png` | The crown, on light. Avatars, badges |
| `mark-on-dark` | `crown-white.svg` | `Royal-Ambulance-crown-white-512w.png` | The crown, on dark |
| `stacked-on-light` | `stacked-purple.svg` | `Royal-Ambulance-stacked-purple-1200w.png` | The vertical lockup, on light. Portrait and square formats |
| `stacked-on-dark` | `stacked-white.svg` | `Royal-Ambulance-stacked-white-1200w.png` | The vertical lockup, on dark |

Minimum width: horizontal 110px on screen and 1in in print, mark 32px and 0.33in. Clear space on all four sides: the height of the crown. Each PNG also ships at double width: replace `1200w` with `2400w`, or `512w` with `1024w`.

1. The brand’s logo appears once in a document, in the band on page 1, and at most once on a slide.
2. Match the file to the ground. Never recolor a logo and never invert one with a filter.
3. Never stretch, skew, rotate, outline or shadow a logo.
4. Hold the clear space. If it is short, shrink the logo, down to the minimum.
5. Never place a logo on a photograph without a solid backing.
6. Never separate the crown from the wordmark in the horizontal or stacked lockup.
7. Use the horizontal lockup wherever it fits. The fill is `#43205b` or white, and nothing else.

## 4. Color

### 4.1 Palette

Purple is the whole palette. Text and rules come from the shared neutrals.

| Name | Token | Hex | Use |
|---|---|---|---|
| Dark Purple | `--royal-dark-purple` | `#2f193b` | The band. Hero grounds, section dividers, table header rows |
| Purple | `--royal-purple` | `#572e72` | Primary. Accent bars, callout borders, buttons, links. Accent text |
| Royal Purple | `--royal-royal-purple` | `#43205b` | The logo fill on light. The action node in a flowchart |
| Light Purple | `--royal-light-purple` | `#8260a2` | Tertiary accents and hover states. Never text. Never a large background |
| Surface | `--royal-surface` | `#faf5fd` | Callout fill |
| White | `--royal-white` | `#FFFFFF` | The page. Text on a dark purple ground |

### 4.2 Grounds and neutrals

Every brand has the same six grounds, and one neutral family sets text and rules in all three brands. White is the page. The last column lists the only text that sits on each ground.

| Ground | Token | Hex | Text on it |
|---|---|---|---|
| Canvas | `--bg-canvas` | `#FFFFFF` | `#23232A` body, `#565860` secondary, `#6D6D77` captions |
| Surface | `--bg-surface` | `#faf5fd` | The same three |
| Surface 2 | `--bg-surface-2` | `#f0e1fd` | `#23232A` and `#565860` only |
| Mid | `--bg-mid` | `#572e72` | `#FFFFFF` and `#DDDDE3` only |
| Band | `--bg-band` | `#2f193b` | `#FFFFFF` headings, `#DDDDE3` body, `#A3A4AC` captions |
| Hero | `--bg-inverse` | `#2f193b` | The same three |

Ink `#23232A` is `--fg-1`. Secondary `#565860` is `--fg-2`. Tertiary `#6D6D77` is `--fg-3`, the dimmest text. On-dark body `#DDDDE3` is `--fg-on-dark-2`. On-dark caption `#A3A4AC` is `--fg-on-dark-3`. Hairline `#E4E4E9` is `--border-1`. Border `#D0D0D6` is `--border-2`. Dimmed `#8A8B93`, `--fg-4`, is for marks only.

### 4.3 Alerts

Four meanings, one family, identical in every brand. Green means good and nothing else. A brand color is never a status color. A word or an icon always travels with the color.

| Meaning | Base | Text | Tint | Text on tint | On dark |
|---|---|---|---|---|---|
| Go · cleared, on time, in service | `#1E7A4D` | `#1E7A4D` | `#DAF8DF` | `#1E7A4D` | `#56B580` |
| Warn · at risk, pending, watch | `#B5821A` | `#926603` | `#FFEFDD` | `#926603` | `#E9B457` |
| Stop · failed, out of service, blocked | `#B0322B` | `#B0322B` | `#FDE9E6` | `#B0322B` | `#EB685C` |
| Info · neutral notice | `#2A5A8C` | `#2A5A8C` | `#E3F0FF` | `#2A5A8C` | `#5796D9` |

- **Steps.** Base is a fill, a rule or a dot on a light ground. Text is text on white and on a surface. Tint is a pill or a callout fill. On dark is text, dots and rules on a dark ground.
- **Names.** The canonical names are `--alert-<name>`, `-text`, `-tint`, `-on-tint` and `-on-dark` in `palette.css`, and `alert` in `tokens.json`. `--status-*`, `--dir-*` and `--diagram-*` are aliases of this family.
- **Dark grounds.** Status works on a band. Use the on-dark step there. In CSS, `--status-*` moves to that step under `.bk-on-dark`.
- **Warn.** The base `#B5821A` measures 3.40:1 on white and is never text. Warn text is `#926603`. Text on an amber fill is `#23232A`, never white.
- **Diagrams.** Decision `#1E7A4D` with `#FFFFFF` text. Warning `#B5821A` with `#23232A` text. Process `#4E4F58` with `#FFFFFF` text. Connector `#4E4F58` at 1.8pt. Rectangles, 6px radius. Fill carries the role, never shape.

### 4.4 Charts

Chart colors come from the house data set, never from the brand palette. Full standard: [reference/data-color.md](reference/data-color.md).

| Job | Colors |
|---|---|
| Series on light, in order | `#2063e6` `#eb6f32` `#0f9b89` `#7f3810` `#8a72f7` `#819808` `#259cde` `#b93388` |
| Series on dark, in order | `#0986e4` `#fc803e` `#06bfa8` `#ac772e` `#ac94fd` `#b1d454` `#74c8fc` `#c4588d` |
| Magnitude, light to dark | `#f0e1fd` `#e2c2fb` `#d29ef8` `#ba7ce4` `#9d60c6` `#7f42a6` `#572e72` |
| Good, bad, caution, neutral | `#1E7A4D` `#B0322B` `#926603` `#6D6D77`, each with an arrow or icon and a word |

- Assign series in order. Never cycle. There is no ninth: fold the tail into “Other” or split the chart. On a scatter, a bubble chart, a map or small multiples, four series at most on light and three on dark.
- Good or bad follows the meaning, never the sign of the number. A cost that falls is good. Never two tints of one hue for two different things: a before and after chart sets a `#D0D0D6` baseline against series 1.

### 4.5 Color rules

1. White is the page. The band opens a document. It is never the reading surface.
2. Body text is `#23232A` on white. On a dark ground, headings are `#FFFFFF` and body is `#DDDDE3`.
3. `#8A8B93`, `#D0D0D6` and `#E4E4E9` are never text.
4. A brand color is never a status color and never a chart series. Every color is an exact hex from `tokens.json`. Never invent one and never tint one.
5. Light Purple `#8260a2` is never text and never a large background. It never sits on `#2f193b`, where it measures 3.13:1.
6. Accent text on white is Purple `#572e72`, which measures 10.30:1. White text sits on `#2f193b`, `#572e72` or `#43205b` only.
7. Dark grounds are `#2f193b` and `#572e72` only. Tints are `#faf5fd` and `#f0e1fd` only.
8. Partner facility colors are gated. Read `reference/partner-colors.md` first. Never sample a color from a logo.

## 5. Type

Montserrat for every word, in every brand. Full standard: [reference/type-system.md](reference/type-system.md).

| Step | pt | px | Weight | Leading | Use |
|---|---|---|---|---|---|
| `bk-display-xl` | 72 | 96 | 800 | 1.05 | Hero and title bands only |
| `bk-display-lg` | 54 | 72 | 800 | 1.08 | Hero and title bands only |
| `bk-display-md` | 42 | 56 | 800 | 1.10 | Slide headlines |
| `bk-h1` | 30 | 40 | 700 | 1.18 | Page title |
| `bk-h2` | 24 | 32 | 700 | 1.25 | Section heading |
| `bk-h3` | 18 | 24 | 600 | 1.35 | Subhead |
| `bk-h4` | 15 | 20 | 600 | 1.45 | Subhead |
| `bk-body-lg` | 15 | 20 | 400 | 1.55 | Lead paragraph, deck body |
| `bk-body` | 12 | 16 | 400 | 1.60 | Body |
| `bk-body-sm` | 10.5 | 14 | 400 | 1.55 | Table cells, secondary body |
| `bk-caption` | 9 | 12 | 400 | 1.45 | Captions, footers. The print floor |
| `bk-eyebrow` | 9 | 12 | 600 | 1.45 | Uppercase labels, tracked 0.080em |

1. No italic, at any weight. Never synthesize one.
2. Weights 400, 600, 700 and 800 only. Three at most in one piece.
3. On a dark ground, drop one weight where the step is 700 or heavier and add 0.005em tracking. 600 is the floor.
4. Tracking is in em, never px or pt. Uppercase is always tracked and never longer than four words.
5. Sentence case for every heading. Uppercase for the band title, the title slide title and the lockup label only.
6. Flush left, ragged right. Never justify. Never center past three lines. A body line stops at 70 characters, which is 54ch. Captions 40ch. Headings 28ch.
7. Space above a heading is three times the space under it. Subhead 18pt above, 6pt under. Section heading 36pt above, 12pt under.
8. The mono face is for color values, paths and filenames, code, and record identifiers. Everything else is Montserrat.

## 6. Layout

Three document types. A report takes the memo page and margins. Full specification, with every position in inches and points: [reference/layout.md](reference/layout.md).

| | Memo | One-pager | Deck |
|---|---|---|---|
| Page | US Letter, 8.5 by 11in, portrait | US Letter, 8.5 by 11in, portrait. Exactly one page | 13.333 by 7.5in, 16:9 |
| Margins | 0.75in | 0.6in | 0.67in top, 0.83in left and right, 0.42in bottom |
| Opens on | The band, with the logo | The band, with the logo | A title slide on the dark ground |
| Headline | None. The Re line states the subject | One finding, `bk-h1`, 30pt | One finding per slide, sentence case |
| Body | `bk-body`, 12pt, on white | `bk-body`, 12pt, on white | 15pt, on white |

A report and a generic document take the memo page and margins. They open with a headline, `bk-h1`, 30pt, and a lead.

1. Content slides are white. The dark band is for the title, divider and closing slides.
2. A document opens on one band. The band title is `bk-h2`, 24pt, uppercase, four words at most. Everything under it runs on white.
3. Body text holds the 70 character measure. A table or a figure may run the full width.
4. Lead paragraph `bk-body-lg`, 15pt. Subheads `bk-h3`, 18pt. Table cells `bk-body-sm`, 10.5pt. Footer `bk-caption`, 9pt.

## 7. Co-brand

Apex Paramedics and Royal Ambulance are operating companies under Collective Edge, and the reader should be able to see it.

1. “Powered by Collective Edge” appears once on every Apex Paramedics and Royal Ambulance document. Never twice.
2. A Collective Edge document carries the Collective Edge logo and no lockup. Where the Collective Edge mark shares a surface with another brand, the lockup is on that surface, once.
3. The lockup is the label `POWERED BY` over the Collective Edge horizontal lockup, under a 0.75pt (1px) hairline. Label: 600, uppercase, 9pt, tracking 0.080em, `#6D6D77` on white and `#A3A4AC` on a dark ground. Lockup: 2.125in (204px) wide, 0.354in (34px) tall, never under 120px, the Collective Edge `horizontal-on-light` file on white and `horizontal-on-dark` on a dark ground. Every value is in `cobrand` in `brands.json`.
4. A memo and a one-pager carry it in the footer row, at left. A report carries it as the last block of the body on the last page. A deck carries it on the closing slide.
5. It sits beside the brand’s own logo, never inside it. Never merge, nest or recolor either mark.
6. Two exceptions, from `brands.json`: a clinical instruction and a patient-facing consent or safety document carry no lockup.
7. On an Apex Paramedics or Royal Ambulance surface, that company leads. Its logo heads the page and its palette runs the band. Collective Edge adds no hue.
8. On a Royal surface the Collective Edge block mark takes a `#572E72` wedge. Use the shipped files `mark-black-royal.svg` and `mark-white-royal.svg` from the Collective Edge kit. Full construction: [reference/brand.md](reference/brand.md) section 3.

## 8. Voice

Royal writes for the reader who is between calls. Short declarative sentences.

1. Short declarative sentences. Active verbs. No filler and no throat-clearing.
2. No em dashes. Use a period, a comma or `·`. An en dash only in a date or number range.
3. Exact values. The real number, never a rounded one. The hex, never a description of the color.
4. A label, a value, and nothing between them. No helper text, no caption restating the thing above it, no parenthetical after a heading.
5. No emoji, no exclamation points, no rhetorical questions.
6. Clinical and operational terms stay precise. Name people, partners and facilities exactly as they write themselves.
7. The reader is between calls. Keep it short.

## 9. Check before shipping

Check the finished file, not the code that made it.

- [ ] Every text run names Montserrat. No run is italic. Every weight is 400, 600, 700 or 800, three at most.
- [ ] Every size is a step in section 5 and nothing is under 9pt. Every color is a hex from `tokens.json`. No text is set in `#8A8B93`, `#D0D0D6` or `#E4E4E9`.
- [ ] Body text is `#23232A` on white. On a dark ground headings are `#FFFFFF` and body is `#DDDDE3`.
- [ ] Margins are 0.75in on a memo or a report and 0.6in on a one-pager. A one-pager is one page.
- [ ] Slides are 13.333 by 7.5in with 15pt body. Only the title, divider and closing slides are dark.
- [ ] The brand’s logo appears once in a document and at most once on a slide, in the role for its ground, at or above the minimum, clear space held, aspect ratio unchanged.
- [ ] “Powered by Collective Edge” appears exactly once in the document.
- [ ] Every status color is an alert step for its ground and carries a word or an icon. Green marks good only. Every chart color is from the house data set, with series in order.
- [ ] No em dash in any text. No uppercase run is longer than four words. Body lines hold 70 characters. No text is justified.
- [ ] No text is `#8260a2`. White text sits only on `#2f193b`, `#572e72` or `#43205b`.
- [ ] The file was rendered and looked at. Nothing overlaps, clips or overflows. If you could not render it, say so.

For HTML output, also run `python3 scripts/validate.py FILE.html` and `python3 scripts/ui-audit.py FILE.html`. `validate.py` checks type rules 1, 2, 5, 9, 10, 13 and 14 and check L1, retired logo artwork, and exits non-zero on a violation. It cannot see a rendered page. When you hand the work back, state the brand, the document type, the logo role, how the font embedded, and anything you could not verify. `@main` serves the latest. Production pins a tag in place of `@main`.
