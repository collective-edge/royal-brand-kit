# Royal Ambulance · for agents

Read this page before you build anything that carries the Royal Ambulance name. It is written so a Word, PowerPoint, PDF or Google file comes out right without rendering a page. For a document, a deck or a sheet, this page and [`reference/layout.md`](../reference/layout.md) win. [`SKILL.md`](../SKILL.md) wins on logo, color and voice.

## 1. The brand

Royal Ambulance is a Bay Area medical transportation company and an operating company under Collective Edge. Its color is purple over the shared house neutrals, and its mark is the crown.

Working for a person instead? Send them to [`for-humans/`](../for-humans/) for logo, font and color files, and to the guidelines page at `https://collective-edge.github.io/royal-brand-kit/`.

## 2. Load the brand

Every file is public on jsDelivr. No auth, no install. Every path on this page is relative to this base: `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/`

**Word, PowerPoint, Excel, PDF and Google files.** Install or register these four files before you render. Set the font on every style you use and on every run. Never leave a default face in the file.

| Weight | File, in `for-humans/fonts/static/` | Font name to set |
|---|---|---|
| 400 | `Montserrat-Regular.ttf` | `Montserrat` |
| 600 | `Montserrat-SemiBold.ttf` | `Montserrat SemiBold`, bold off |
| 700 | `Montserrat-Bold.ttf` | `Montserrat`, bold on |
| 800 | `Montserrat-ExtraBold.ttf` | `Montserrat ExtraBold`, bold off |

Before converting with LibreOffice, copy the four files to `~/.fonts/` and run `fc-cache -f`. Confirm with `fc-list | grep -c Montserrat`, which must print 4 or more. The variable font alone does not provide the names `Montserrat SemiBold` or `Montserrat ExtraBold`. Those runs fall back to a serif. In the PDF, run `pdffonts` and confirm every font name starts with Montserrat.

Google Docs and Slides carry Montserrat. Set the family `Montserrat` and the numeric weight. No italic, at any weight. Read sizes from [`snippets/type-tokens.json`](../snippets/type-tokens.json) and colors from [`tokens.json`](../tokens.json). If the render falls back to another face, say so when you hand the work back.

**HTML.** Four stylesheets, in this order. `palette.css` is the only one that differs by brand. Load `data-color.css` only when the page has a chart or a reported number.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/type-system.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/palette.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/cobrand.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/data-color.css">
```

For a PDF made from HTML, embed the face inline:

```css
@font-face { font-family: "Montserrat"; font-weight: 400 800; font-style: normal;
  src: url("https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.woff2") format("woff2-variations"),
       url("https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf") format("truetype-variations"); }
html, body { font-family: "Montserrat", "Helvetica Neue", Helvetica, Arial, sans-serif; }
```

## 3. Logos by role

Ask for a role, never a filename. Filenames differ between brands. `-on-light` is the file placed on a light ground. `-on-dark` is the file placed on a dark one. Word, PowerPoint and Google files take the PNG, which is transparent. HTML takes the SVG in an `<img>`. `brands.json` lists the SVG under `logos` and the PNG under `logosPng`, by the same role.

| Role | SVG | PNG | Ground | Minimum width |
|---|---|---|---|---|
| `horizontal-on-light` | `assets/logos/horizontal-purple.svg` | `for-humans/logos/png/Royal-Ambulance-horizontal-purple-1200w.png` | White and tints | 110px · 1in |
| `horizontal-on-dark` | `assets/logos/horizontal-white.svg` | `for-humans/logos/png/Royal-Ambulance-horizontal-white-1200w.png` | The band and dark slides | 110px · 1in |
| `mark-on-light` | `assets/logos/crown-purple.svg` | `for-humans/logos/png/Royal-Ambulance-crown-purple-512w.png` | White and tints | 32px · 0.33in |
| `mark-on-dark` | `assets/logos/crown-white.svg` | `for-humans/logos/png/Royal-Ambulance-crown-white-512w.png` | The band and dark slides | 32px · 0.33in |
| `stacked-on-light` | `assets/logos/stacked-purple.svg` | `for-humans/logos/png/Royal-Ambulance-stacked-purple-1200w.png` | White and tints. Portrait and square formats | Use the horizontal lockup under 1.5in wide |
| `stacked-on-dark` | `assets/logos/stacked-white.svg` | `for-humans/logos/png/Royal-Ambulance-stacked-white-1200w.png` | Dark grounds. Portrait and square formats | Use the horizontal lockup under 1.5in wide |

- A full URL is the base plus the path: `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/for-humans/logos/png/Royal-Ambulance-horizontal-white-1200w.png`. Each PNG also ships at double width: replace `1200w` with `2400w`, or `512w` with `1024w`.
- `compact-on-light`, `compact-on-dark` and `app-icon` do not exist for this brand. Use `horizontal-on-light` or `horizontal-on-dark`.
- The logo appears once in a document and at most once on a slide. A memo, a one-pager and a report carry it in the band. A working-doc carries it top left of page 1. A sheet carries none. Never recolor, invert, stretch, rotate, outline or shadow a logo.

## 4. Color

Purple is the whole palette. Text and rules come from the shared neutrals. Every value as JSON, with RGB: `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/tokens.json`.

| Name | Token | Hex | Use |
|---|---|---|---|
| Dark Purple | `--royal-dark-purple` | `#2f193b` | The band. Title, divider and closing slides. Table header rows |
| Purple | `--royal-purple` | `#572e72` | Primary. Accent text: subheads, slide headlines, action numbers |
| Royal Purple | `--royal-royal-purple` | `#43205b` | The logo fill on light |
| Light Purple | `--royal-light-purple` | `#8260a2` | Tertiary accents. Never text. Never a large background |
| Surface | `--royal-surface` | `#faf5fd` | Callout fill |
| White | `--royal-white` | `#FFFFFF` | The page. Text on a dark purple ground |

**Shared neutrals.** Identical in every brand. They set all text and rules.

| Token | Hex | Use | Token | Hex | Use |
|---|---|---|---|---|---|
| `--fg-1` | `#23232A` | Body text and headlines on white | `--fg-on-dark-1` | `#FFFFFF` | Headings on a dark ground |
| `--fg-2` | `#565860` | Secondary text | `--fg-on-dark-2` | `#DDDDE3` | Body on a dark ground |
| `--fg-3` | `#6D6D77` | Captions, labels, footers. The lightest text | `--fg-on-dark-3` | `#A3A4AC` | Captions on a dark ground |
| `--fg-4` | `#8A8B93` | Marks only. Never text | `--bg-canvas` | `#FFFFFF` | The page |
| `--border-1` | `#E4E4E9` | Hairlines. Never text | `--border-2` | `#D0D0D6` | Stronger rule, chart baseline. Never text |

**The alert family.** Identical in every brand. Green means good and nothing else. A brand color is never a status color. A word or an icon always travels with the color.

| Meaning | Base | Text | Tint | Text on tint | On dark |
|---|---|---|---|---|---|
| Go · cleared, on time, in service | `#1E7A4D` | `#1E7A4D` | `#DAF8DF` | `#1E7A4D` | `#56B580` |
| Warn · at risk, pending, watch | `#B5821A` | `#926603` | `#FFEFDD` | `#926603` | `#E9B457` |
| Stop · failed, out of service, blocked | `#B0322B` | `#B0322B` | `#FDE9E6` | `#B0322B` | `#EB685C` |
| Info · neutral notice | `#2A5A8C` | `#2A5A8C` | `#E3F0FF` | `#2A5A8C` | `#5796D9` |

Base is a fill, a rule or a dot on a light ground. Text is text on white. Tint is a pill or callout fill. On dark is text, dots and rules on a dark ground. Warn base #B5821A is never text, and text on it is #23232A.

**Charts.** Chart colors come from the house data set, never from the brand palette. Assign series 1 to 7 in order. Never cycle. There is no eighth.

- On a light ground: `#2063e6` `#eb6f32` `#b93388` `#7f3810` `#8a72f7` `#819808` `#259cde`
- On a dark ground: `#0986e4` `#fc803e` `#c4588d` `#ac772e` `#ac94fd` `#b1d454` `#74c8fc`

## 5. Make a document

**Start here.**

1. Is there an existing file? Follow the editing rules. Do not restyle it.
2. Did they point at a document to imitate? Copy it.
3. Otherwise pick a type from the table below. The first row that fits wins.
4. Keep it short. The wording budget sits under the type table.

### Editing rules

Most requests change a file that already exists. These eight rules come before everything else on this page.

1. **Edit in place.** Asked to edit, update, fix or add to an existing file: keep its layout, styles, fonts, sizes, colors, column order and wording. Change only what was asked. Same file, same link. Do not convert its format, move it or make a copy unless asked.
2. **Match the neighbors.** New content inside an existing file takes the style of the nearest existing content of the same kind. A new row looks like the rows around it. A new slide uses the deck’s own layout.
3. **A named example is the template.** Asked to make it look like another document: copy that document’s structure, styles and order. This kit does not override it.
4. **Restyle only when asked.** “Brand this”, “clean up the formatting”, “make it consistent”. Then apply the working-doc styles to what is there: font, sizes, heading colors, table style, logo, footer. Do not reorder, rewrite or shorten the words. Do not add a band. Where the file has a band, take it out: the logo goes top left and the band’s words go only if they are not already the title.
5. **An accepted format is fixed.** A recurring report or an agenda a person approved is reused exactly next time. Never improve it unprompted.
6. **Leave the words alone.** Shorten or rewrite only when asked. Asked to tighten: cut at least half and keep every fact, name, number and date.
7. **Delete nothing that is not yours.** Never delete someone else’s content, comments, formulas, data validation or tabs. Before a large change, say what will change. After, list what changed in three bullets or fewer.
8. **Never resize to fit.** Never change the spacing, sizes or margins of an existing file to make an edit fit a page. If an edit pushes content onto a new page, leave it there and say so when you hand the work back.

### Pick a type

| Type | Use it when |
|---|---|
| sheet | Rows and columns people will sort, filter or fill in. Tracker, list, log, roster, budget, workbook. Google Sheets or Excel |
| deck | Anything presented on a screen, in Google Slides or PowerPoint. One slide and a graphic for a slide count |
| working-doc | The default. Anything in Google Docs or Word that people will keep editing. Agenda, meeting guide, prep packet, status report, plan, charter, brief, notes, job description, scorecard, policy draft, proposal draft |
| one-pager | A designed single page for an outside reader, delivered as a PDF. Fact sheet, flyer, leave-behind, case study |
| report | A designed document of three pages or more for an outside reader, delivered as a PDF. Proposal, review, analysis |
| memo | Only when the request asks for a memo by name |

The band is for PDF, print and slides. A document that will live in Google Docs is a working-doc unless the person asks for a designed one-pager. The earlier `generic` type is now working-doc.

**Wording budget.** It applies to every type. The first line states the decision, the ask or the status. In an agenda it states what the meeting is for. No paragraph restates the title. No closing summary. No sentence about the document itself. A sentence runs 20 words at most. Items that share the same fields go in a table. Parallel items go in bullets. An agenda and a status report fit 1 page. Every other working-doc is as short as the content allows.

### Working-doc

Plain on purpose, so it survives Google Docs untouched. US Letter, portrait, 0.75in margins on all four sides, text block 7.0in. Montserrat at 400 and 700 only: bold off and bold on. No band, callout box, card, shadow, tinted panel, icon, emoji, uppercase label, sub-banner or stat numeral.

| Part | Specification |
|---|---|
| Logo | Role `horizontal-on-light`, PNG, 1.3in wide. Once, top left of page 1, inline, as its own paragraph, 12pt after |
| Title | Named style `Title`. 24pt, 700, `--fg-1` #23232A, line spacing 1.15, 3pt after. Sentence case, 60 characters at most, no period |
| Meta line | Directly under the title. One line, 10.5pt, 400, `--fg-3` #6D6D77, items joined by ` · `: owner or team · date as `13 November 2026` · audience or status if needed. A 0.75pt `--border-1` #E4E4E9 bottom border on the paragraph, 6pt under the text. 12pt after |
| Heading 1 | Named style `Heading 1`. 15pt, 700, #23232A, line spacing 1.15. 18pt before, 6pt after |
| Heading 2 | Named style `Heading 2`. 12pt, 700, `--fg-accent` #572e72, line spacing 1.15. 12pt before, 3pt after. Two heading levels at most. A heading is a plain label: sentence case, 6 words at most, no colon, no period |
| Body | Named style `Normal`. 10.5pt, 400, #23232A, line spacing 1.35, 6pt after. Flush left, never justified |
| Bullets | The standard bullet list of the application. Hanging indent 0.25in, 3pt after. One line each, two at most. Six in a group at most. One nesting level at most. A numbered list only for steps in order or agenda items |
| Table | The full text width, the left edge of the table on the left margin. In a Word or Google file that takes a table indent equal to the left cell padding, 6pt, and column widths that sum to the text block less 6pt. Header row: 10.5pt, 700, #23232A, fill `--bg-surface-2` #f0e1fd, a 0.75pt #23232A bottom border. Body cells: 10.5pt, 400, #23232A, a 0.75pt #E4E4E9 bottom border. Cell padding 4pt top and bottom, 6pt left and right. No vertical rules, no zebra, no frame, no dark header fill. Numbers right-aligned. One empty paragraph between two adjacent tables |
| Status cell | The character U+25A0, a no-break space, then the word, in one run. 700, in the alert Text color from section 4. One or two words |
| Patterns | Agenda: a 3-column table of Time or minutes, Topic, Owner. Or a numbered list with the owner and the minutes at the end of each line. Never both. Status report: one line of overall status, then a table of Item, Owner, Due, Status, then bullets under the heading Needs a decision, if any |
| Footer | The document footer, on every page. One left-aligned line, 9pt, 400, #6D6D77: `Royal Ambulance · Page N`, where N is the page number field. No rule, no logo, no table. No “Powered by Collective Edge”, as words or as a lockup |
| Build, python-docx | Set `Title`, `Heading 1`, `Heading 2` and `Normal` to the values above and use them. Line spacing is a float multiple: `paragraph_format.line_spacing = 1.35`, rule `WD_LINE_SPACING.MULTIPLE`. Never `EXACTLY`, never a point value. Name `Montserrat` on every style and every run, in `w:ascii`, `w:hAnsi`, `w:eastAsia` and `w:cs`. 700 is bold on. Do not name `Montserrat SemiBold`. Logo inline with `add_picture`. Footer: one plain paragraph with a `PAGE` field. No text boxes, floating images, section breaks, columns or tab stops |

### Sheet

| Part, in Google Sheets or Excel | Specification |
|---|---|
| Layout | One table per tab, starting at A1. The header is row 1. No title row above it, no spacer row or column, no merged cells, no decorative color. No tab that was not asked for: no cover tab, no “How to use” tab. No logo and no lockup, since a growing table has no stable place for one. Never use `=IMAGE()`: it returns `#REF!` |
| Font | Family `Montserrat`, 10pt, in every cell. Whole point sizes only, never 10.5pt. Bold off or bold on, 400 and 700. Never name a weight family such as `Montserrat SemiBold` in a sheet: it falls back to Times New Roman. Text left-aligned, numbers right-aligned |
| Header row | Row 1. 700, #23232A, fill `--bg-surface-2` #f0e1fd, a 1pt #23232A bottom border. Frozen, filter on. Freeze the first column too when it is the name or ID of the row |
| Columns | Wrap text columns and set their widths: short code 80px, date 110px, name 180px, notes 320px. Clip nothing. Row height automatic |
| Formats | Date `d mmm yyyy`. Whole number `#,##0`. Money `$#,##0`, two decimals only when cents matter. Percent `0%` |
| Status column | A dropdown: data validation from a fixed list. Each value is U+25A0, a space, then one or two words. Never free text. Conditional formatting sets the color by value, never a hand fill: the alert Tint as fill and the alert Text on tint as text, 700: go #DAF8DF and #1E7A4D, warn #FFEFDD and #926603, stop #FDE9E6 and #B0322B, info #E3F0FF and #2A5A8C. Default list when none is given: Not started (info), On track (go), At risk (warn), Blocked (stop), Done (go) |
| Due dates | Conditional formatting turns a date in the past #B0322B, the alert stop Text color, unless the status of the row is Done |
| Totals row | At the bottom. 700, a 1pt #23232A top border. Formulas, never typed values |
| Limits | A note is 120 characters at most. Longer context goes in a linked doc. A tab name is 20 characters at most, Title Case, with no date unless the tab is a period |
| Editing a sheet | Never reorder or rename columns. Never overwrite a formula with a value. Keep validations, conditional formats, frozen panes and column widths. New columns go at the right. New rows go at the bottom or where the sort order puts them. Match the surrounding cell format. A sheet that has its own colors and layout keeps them |

### Deck

- **Editing a deck.** The common case, often one slide. Use that deck’s own layouts, fonts, colors and positions, even where they are not this kit’s. Combine, split or reword slides without restyling the rest. Deliver the change inside the same deck. “Combine these two slides” means one slide that carries the content of both in the layout of the first, then delete the second. If the two say the same thing, say so and ask before deleting one.
- **A graphic to paste on a slide.** A 1920 x 1080 PNG on a white ground. The same type rules, no band. Text is 48px or larger, which is 24pt on the slide. An Apex Paramedics or Royal Ambulance graphic or chart made on its own carries one line of words, bottom right: `Powered by Collective Edge`, 24px, 400, #6D6D77. No logo. A Collective Edge graphic carries none.
- **A new deck.** Slide 13.333 x 7.5in, 12192000 x 6858000 EMU. Padding 0.67in top, 0.83in left and right, 0.42in bottom. Content 11.67in wide. Two columns are 5.5in each, at x 0.83in and x 7.0in. A body line is 7.45in at most. One message per slide. The headline is one sentence that states the point. Positions are x, y from the top left corner of the slide. Start from a blank layout and place each part as a fixed box. Switch auto-fit off.

| Part | Specification |
|---|---|
| Grounds | Title, divider and closing slides: fill `--bg-inverse` #2f193b. No rule. Every other slide is white #FFFFFF |
| Layouts | title, divider, statement, text, two-column, chart, table, comparison, timeline, quote, summary, closing. Every box is in `reference/layout.md` section 8 |
| Headline | Box at 0.83in, 0.67in, 10.0in by 1.28in. 42pt, 800, `--fg-accent` #572e72, leading 46.2pt. One sentence. 2 lines and 60 characters at most. Floor 30pt |
| Body zone | Box at 0.83in, 2.53in, 11.67in by 3.78in, on every white slide. Body, bullets and table text 15pt, 400, #23232A, leading 23.3pt. Floor 12pt. Key points 18pt, 600, #23232A, between 0.75pt #E4E4E9 rules |
| Slide footer | White slides only. A 0.75pt #E4E4E9 rule at y 6.55in, from x 0.83in, 11.67in wide. Logo role `horizontal-on-light`, 1.43in wide, at x 0.83in, centered on the row at y 6.73in, 0.35in tall. Page number: the slide’s position in the deck as a bare numeral, 12pt, #6D6D77, in a box at 10.5in, 6.73in, 2.0in by 0.35in, right-aligned, anchored middle. The title slide is 1 and shows no number |
| Title slide | Logo role `horizontal-on-dark`, 2.1in wide, at 0.83in, 0.67in. Title: box at 0.83in, 3.85in, 11.67in by 1.62in, text on the bottom of the box, 54pt, 700, uppercase, tracking 0.025em, #FFFFFF, 4 words and 28 characters at most. Subtitle at y 5.64in, 18pt, 600, #DDDDE3, 60 characters. A 0.75pt #483553 rule at y 6.55in, from x 0.83in, 11.67in wide. Under it at y 6.73in, 12pt, #A3A4AC: brand or presenter at left, date at right |
| Divider slide | Number at y 4.19in, 18pt, 600, #A3A4AC, two digits. Title: box at 0.83in, 4.7in, 10.0in by 1.28in, text on the bottom of the box, 42pt, 700, #FFFFFF, 40 characters. A 0.75pt #483553 rule at y 6.55in, 11.67in wide. Under it at y 6.73in, 12pt, #A3A4AC: brand at left, page number at right. No logo |
| Closing slide | Logo as on the title slide. Closing line: box at 0.83in, 3.14in, 10.0in by 1.28in, text on the bottom of the box, 42pt, 700, #FFFFFF, 60 characters. Contact at y 4.59in, 15pt, #DDDDE3, 3 lines of 48 characters. The lockup, in the footer row, the only one in the deck. A 0.75pt #483553 rule at y 6.55in, 11.67in wide. On the row at y 6.73in, 0.35in tall: the words `Powered by`, 12pt, 400, #A3A4AC, in a box at x 0.83in, 1.1in wide, anchored middle. Then the Collective Edge `horizontal-on-dark` logo at x 2.0in, y 6.80in, 1.25in wide, 0.208in tall. The date at right, 12pt, #A3A4AC. The lockup takes the place of the brand name |
| Table slide | The table rules above at 15pt. 5 body rows and 6 columns at most. Cell padding 9pt above and under, 12pt left and right |
| Chart slide | One quantity is one series, in series color 1. Two series only when comparing two things. Four series at most. Delete the value axis, switch data labels on and set their number format to `#,##0` |

### One-pager, report and memo

Designed documents for an outside reader, delivered as a PDF. Each opens on the band. Every size is in points. Text is Montserrat, flush left. A body line is 5.96in at most, 70 characters.

- **Memo.** US Letter, portrait, 0.75in margins, text block 7.0in. 1 page, 2 at most. Parts, top to bottom: band, To block, body, table, subhead, actions, sign-off, footer.
- **One-pager.** US Letter, portrait, 0.6in margins, text block 7.3in. Exactly 1 page. Parts: band, headline, lead, meta row, subhead, one paragraph, subhead, table, callout, footer.
- **Report.** The memo page and margins. Its parts are in [`reference/layout.md`](../reference/layout.md) section 6.

| Part | Specification |
|---|---|
| Band | Page 1 only, edge to edge, 8.5in wide, 1.11in tall. Fill `--bg-band` #2f193b. No rule. The band is solid to its bottom edge. The body starts 18pt under it |
| Band title | Left, on the left margin, centered vertically. 24pt, 600, uppercase, tracking 0.045em, #FFFFFF. One line, 4 words and 18 characters at most. On a memo it is the word Memo |
| Band logo | Right, on the right margin, centered vertically. Role `horizontal-on-dark`, 1.6in wide. The Royal Ambulance logo appears nowhere else in the document |
| To block, memo | Rows To, From, Date, Re. The date is day, month, year: 13 November 2026. Label column 1.0in, 12pt, #6D6D77. Value 12pt, 400, #23232A, one line, 60 characters. The Re value is 700. A 0.75pt #E4E4E9 rule above the first row and under every row. 6pt above and under the text. 18pt after. A memo has no headline. Band, To block, body, sign-off and footer are required. Table, subhead and actions are optional. A closing line is the last body paragraph |
| Headline, one-pager | 30pt, 700, #23232A. A sentence that states the finding and ends with a period. 2 lines and 56 characters at most |
| Lead, one-pager | 12pt under the headline. 15pt, 400, #23232A. 2 lines and 110 characters at most |
| Meta row, one-pager | 12pt under the lead. 3 equal columns, 0.25in apart. Label 9pt, #6D6D77, 12 characters. Value under it, 10.5pt, 600, #23232A, 24 characters. A 0.75pt #E4E4E9 rule above and under. 6pt padding |
| Subhead | 18pt, 600, `--fg-accent` #572e72. Sentence case. One line, 32 characters. 18pt above, 6pt under. A one-pager has two |
| Body | 12pt, 400, #23232A, leading 19.2pt, 12pt between paragraphs. Emphasis is 700 |
| Table | On a one-pager, and at most one on a memo, under the last paragraph. The width of the text block. Column widths follow the content. The first column is the widest. A status column is 1.2in, 1.9in on a slide. Header: Fill `--bg-band` #2f193b. Text `--fg-on-dark-1` #FFFFFF, with 0.005em added tracking. No rule. Header text 10.5pt, 600, sentence case. Cells 10.5pt, 400, #23232A. Padding 6pt above and under, 9pt left and right. A 0.75pt #E4E4E9 rule under every body row. No frame, no vertical rules, no zebra. Numbers right-aligned. Caption above, 9pt, #6D6D77 |
| Status cell | A square, then the word at 600, both in the alert Text color. In HTML and PDF the square is drawn, 6pt in a document and 9pt on a slide. In Word, PowerPoint and Google files it is the character U+25A0, which Montserrat contains, at 9pt in a document and 12pt on a slide, then one no-break space. A status that is neither good, caution nor bad takes Info #2A5A8C |
| Callout, one-pager | The width of the text block, 12pt above. Fill `--bg-surface` #faf5fd. A 1.5pt #572e72 rule on the top edge. Padding 12pt above and under, 15pt left and right. Text 12pt, #23232A. One per page. No border, no rounded corners, no icon |
| Actions, memo | Numbered rows, 5.96in wide. Number in a 0.33in column, 12pt, 600, #572e72. Text 12pt, #23232A, 90 characters. A 0.75pt #E4E4E9 rule above every row and under the last. 6pt above and under the text |
| Sign-off, memo | 24pt under the last block. Name 12pt, 600, #23232A. Under it the contact, 10.5pt, #6D6D77 |
| Footer | Every page. The last line sits on the bottom margin. A 0.75pt #E4E4E9 rule, the width of the text block, 9pt above the text. Left, the signature: `Royal Ambulance · Internal` when every reader is staff. Otherwise the document title after the dot, 40 characters at most. Right: `Page X of Y`. 9pt, #6D6D77, one line. At least 12pt between the last block and the rule |
| Powered by Collective Edge | Apex Paramedics and Royal Ambulance carry it once, small, on everything delivered as a PDF, a deck or an image. Never on a working-doc or a sheet, even when one is exported to PDF. Never on a Collective Edge document, a clinical instruction, or a patient-facing consent or safety document. **The lockup** is one line: the words `Powered by`, 9pt, 400, #6D6D77, then 6pt to the right the Collective Edge logo, 1.25in wide and never larger: `https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/for-humans/logos/png/Collective-Edge-horizontal-black-1200w.png`. **Where:** memo and one-pager, at the left of the page 1 footer row, with the footer text and page number at the right. Report, the last line of the body, under a 0.75pt #E4E4E9 rule. Deck, the footer row of the closing slide, with the words at 12pt #A3A4AC and the file `Collective-Edge-horizontal-white-1200w.png`. A chart or data graphic made on its own, the words only, no logo |

- **Budgets.** Memo on one page, no table: 4 paragraphs of 520 characters in all, plus 3 actions. Memo on one page with a table of 4 rows by 4 columns at most: 1 paragraph of 130 characters, the table, plus 3 actions. Actions never count as paragraphs. One-pager: 1 paragraph of 210 characters, 1 table of 4 rows by 5 columns, 6 rows when there is no callout, 1 callout of 140 characters. A chart replaces the table, 2.2in tall at most. Text slide: 5 bullets of 80 characters. Two-column slide: 3 key points of 60 characters. Summary slide: 4 takeaways of 70 characters.
- **Tracking and capitals.** In Word and PowerPoint, tracking in points is em times the size: band title 1.08pt, title slide title 1.35pt, document headline -0.36pt, slide headline -0.63pt, subhead -0.07pt. Set no other tracking. Type the capitals. Do not use the all-caps attribute. The attributes are in `reference/layout.md` section 11.
- **When content does not fit.** Take these four steps in order and stop at the first that fits. (1) Tighten: set the overflowing part one step down the scale, to its floor and no further. Floors: one-pager headline 24pt, lead 12pt, body and callout 10.5pt, table text 9pt, slide headline 30pt, slide body 12pt. (2) Shorten: cut the text to the limit of the part. (3) Split: move the overflow to another page or slide. A one-pager cannot split. (4) Switch: a memo or a one-pager becomes a report, a text slide becomes two-column, and a two-column, comparison or timeline slide becomes a table slide. A working-doc never tightens. It shortens.

### When it will be a Google file

Build the `.docx` or `.pptx`, then convert. Conversion changes these things.

1. Line spacing is a multiple: 1.15 for headings, 1.35 for body. Never an exact point value. Google Docs sets those lines about three times too far apart.
2. No full-width band in Google Docs. A band there is a table at text-block width with indent 0. A negative indent loses the cell padding.
3. No right tab stops. A left and right footer is a two-cell borderless table, or one left-aligned line.
4. Tables: indent equal to the left cell padding, 6pt, set explicitly with `w:tblInd w:w="120"`, and column widths that sum to the text block less 6pt. Unset or at 0, the table sits outside the left margin in Google Docs. One empty paragraph between two tables, or they merge and the second loses its column widths.
5. Budget to 90 percent of a page. Google sets lines taller than Word, so a full Word page spills onto a second.
6. `Montserrat SemiBold` and `Montserrat ExtraBold` survive as real faces. Name the family, bold off.
7. Slides: set the size on every run. An inherited bullet size shrinks. Charts: delete the value axis and set the data label number format to `#,##0`. Otherwise an axis appears and the thousands separators drop.

The full standard, with the Word, PowerPoint, Google and spreadsheet mapping in section 11, is [`reference/layout.md`](../reference/layout.md). The same values as data are in [`documents.json`](../documents.json). This page and `reference/layout.md` carry every value a document needs.

## 6. The rules that get broken

1. Light Purple #8260a2 is never text and never a large background.
2. White text sits on #2f193b, #572e72 or #43205b only. The band has no rule under it.
3. Never separate the crown from the wordmark in the horizontal or stacked lockup. The logo fill is #43205b or white, and nothing else.
4. “Powered by Collective Edge” appears exactly once on every Royal Ambulance PDF, deck and image, small, in the footer row. Never twice. Never on a working-doc or a sheet. Never inside or touching the Royal Ambulance logo.
5. Partner facility colors are gated. Without [`reference/partner-colors.md`](../reference/partner-colors.md) in hand, use the house series order. Never sample a color from a logo.
6. White is the page. The band opens page 1 of a memo, a one-pager and a report, and is never the reading surface. A working-doc and a sheet have no band. Content slides are white. Only the title, divider and closing slides are dark.
7. Green means good and nothing else. A brand color is never a status color. Status takes the alert family, with a word.
8. Chart colors come from the house data set, in series order. A brand color is never a chart series. Every color is an exact hex from this page or `tokens.json`. Never invent one and never tint one.
9. Montserrat only, at 400, 600, 700 and 800. Three weights at most in a document. A deck is the one piece that uses all four. A working-doc uses 400 and 700. No italic. Set the font on every style and every run.
10. Every size is a step on the scale: 9, 10.5, 12, 15, 18, 24, 30, 42, 54pt. Nothing in a document is under 9pt. Nothing on a slide is under 12pt. Slide body is 15pt. A sheet is 10pt, the one size outside the scale.
11. Never narrow a margin. Never switch on auto-fit or shrink-on-overflow. Never tighten leading or tracking to make text fit.
12. Uppercase is for the band title and the title slide title only. Four words at most. Every heading is sentence case.
13. The logo appears once in a document, in the band or top left of a working-doc, and at most once on a slide, in the role for its ground. Never rebuild a logo or the lockup as type. The words “Powered by Collective Edge” stand alone as type only on a chart or data graphic.
14. No em dashes in copy. Use a period, a comma or `·`. No row of large stat numerals, no stat card or big-number panel on a page or slide, no label above a heading, no rule under a heading, no sub-banner under the band.

## 7. Check before you deliver

Measure the finished file, not the code that made it. A file that fails one line is not finished.

Lines 5, 6, 7, 10 and 11 describe a memo, a one-pager and a report. For a working-doc or a sheet, check its table in section 5 instead, and these seven things: no band, the logo once at top left, a light table header, the one-line footer, no “Powered by Collective Edge”, no exact line spacing, and no two tables without a paragraph between them. For an edited file, check that nothing changed but what was asked.

1. **Page count.** A one-pager is exactly 1 page. A memo is 1 page, 2 at most. An agenda and a status report are 1 page.
2. **Page size and margins.** Letter, portrait, 0.75in margins, or 0.6in on a one-pager. Slides are 13.333 x 7.5in.
3. **Nothing past the margin.** Only the band crosses a margin. No text box, table or picture ends outside the text block or the slide padding.
4. **Fonts present.** Every run names Montserrat, Montserrat SemiBold or Montserrat ExtraBold. No italic. No fallback face in the file. Every size is a step in rule 10. No box has auto-fit switched on.
5. **Band.** On page 1 only, 1.11in tall. Fill #2f193b. No rule. Title on one line.
6. **Logo.** Role `horizontal-on-dark` in the band, 1.6in wide, once. Aspect ratio unchanged.
7. **Tables.** Header fill #2f193b, text #FFFFFF, no rule. A hairline under every row. No frame, no vertical rules, no zebra.
8. **Slides.** Body text is 15pt. Content slides are #FFFFFF. Only title, divider and closing are #2f193b.
9. **Color.** Status colors are alert steps and nothing else. Chart colors are the house series, in order.
10. **Lockup.** On a PDF, a deck or an image, “Powered by Collective Edge” appears exactly once, the logo 1.25in wide, in the place section 5 names. A working-doc and a sheet carry none.
11. **Footer.** On every page. `Page X of Y` at right, 9pt, the last line on the bottom margin.

For HTML output, also run `python3 scripts/validate.py FILE.html` and `python3 scripts/ui-audit.py FILE.html`. For a chart palette, run `python3 scripts/validate-palette.py --series`. `validate.py` exits non-zero on a violation. No script sees overlap, clipping or a fallback font.

If you could not render the file, say so. When you hand the work back, state the brand, the document type, the logo role, how the font embedded, and anything you could not verify.

## 8. Read next

| Making | Read |
|---|---|
| Anything | [`SKILL.md`](../SKILL.md). It ends with the pre-ship check |
| A report, a slide layout, a Word, PowerPoint, Google or spreadsheet build | [`reference/layout.md`](../reference/layout.md) and [`documents.json`](../documents.json) |
| A chart, dashboard or scorecard | [`reference/data-color.md`](../reference/data-color.md) |
| A type, color, contrast, logo or voice question | [`reference/type-system.md`](../reference/type-system.md) and [`reference/brand.md`](../reference/brand.md) |
| Buttons, inputs, product UI | [`reference/ui.md`](../reference/ui.md) |
| An HTML page | [`templates/`](../templates/): `working-doc.html`, `deck.html`, `one-pager.html`, `document.html`, `memo.html`. [`Examples/royal-one-pager.html`](../Examples/royal-one-pager.html) is a filled reference. `Examples/HPSM_Ordering_Workflow_Manager.html` predates this standard. It carries no lockup and its own layout. Do not copy it. |
| The Collective Edge mark on a Royal surface | [`reference/brand.md`](../reference/brand.md) section 3. Files, in the Collective Edge kit: `https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/logos/mark-black-royal.svg` and `mark-white-royal.svg` |
| A partner facility color | [`reference/partner-colors.md`](../reference/partner-colors.md) |
| A photograph | [`for-humans/photos/`](../for-humans/photos/). Use it unfiltered |

**Install as a skill.** Clone the kit into the skills directory your agent reads: `git clone https://github.com/collective-edge/royal-brand-kit ~/skills/royal-brand-guidelines`. `SKILL.md` at the root carries the frontmatter. `git pull` updates it.

**The other brands.** One registry resolves every brand to its CDN root, tokens and logo roles. It is identical in all three kits: `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/brands.json`. Each kit has this same page at `for-agents/README.md`: [`collective-edge-brand-kit`](https://github.com/collective-edge/collective-edge-brand-kit/tree/main/for-agents) · [`apex-brand-kit`](https://github.com/collective-edge/apex-brand-kit/tree/main/for-agents) · [`royal-brand-kit`](https://github.com/collective-edge/royal-brand-kit/tree/main/for-agents).
