# Royal Ambulance · layout standard

How to build a memo, a one-pager, a report, a deck or any other Royal Ambulance document. The rules are the same in the Collective Edge, Apex Paramedics and Royal Ambulance kits. Only the values in section 2 differ.

This file is written so a page can be built from it without seeing one. [`documents.json`](../documents.json) holds the same values as data, and the two agree exactly. Type steps come from [`snippets/type-tokens.json`](../snippets/type-tokens.json). Colors come from [`tokens.json`](../tokens.json).

**Units.** Page geometry is in inches. Type and space are in points. On screen, 1pt is 4/3px, so 12pt is 16px and 1in is 96px. Slide positions are measured from the top left corner of the slide.

---

## 1. Choose a type

Match the request to the first row that fits.

| Type | Use it when |
|---|---|
| memo | A message from one named sender to named readers, with a date and a subject. Words: memo, note to staff, announcement, notice, update. |
| one-pager | One finding or one offer on exactly one page. Words: one-pager, summary sheet, brief, fact sheet, flyer, case study, handout. |
| deck | Anything presented on a screen. Words: deck, slides, presentation, pitch. |
| report | Three pages or more with sections. Words: report, review, proposal, plan, analysis, white paper. |
| generic | Anything that matches none of the four. Agenda, letter, policy, checklist, form, job description. |

- **Fallback.** A request that matches nothing is a generic branded document. Section 7.
- **Existing file.** Editing an existing file keeps its layout and its brand. Change only what was asked.
- **Spreadsheet.** A spreadsheet is not a layout type. Apply the table rules to its header row and cells. Section 3.7.

### Page setup

| Type | Page | Orientation | Margins | Text block | Body measure | Columns | Pages |
|---|---|---|---|---|---|---|---|
| memo | US Letter, 8.5 x 11in | portrait | 0.75in on all four sides | 7.0in wide | 5.96in, 70 characters | 1 | 1, 2 at most |
| one-pager | US Letter, 8.5 x 11in | portrait | 0.6in on all four sides | 7.3in wide | 5.96in, 70 characters | 1 | exactly 1 |
| report | US Letter, 8.5 x 11in | portrait | 0.75in on all four sides | 7.0in wide | 5.96in, 70 characters | 1 | 3 or more |
| generic | US Letter, 8.5 x 11in | portrait | 0.75in on all four sides | 7.0in wide | 5.96in, 70 characters | 1 | 1 or more |
| deck | 16:9, 13.333 x 7.5in | landscape | 0.67in top, 0.83in left and right, 0.42in bottom | 11.67in wide | 7.45in, 70 characters | 1 or 2 | any |

Body text never runs wider than the body measure, even where the text block is wider. Tables, callouts, the meta row and the footer span the full text block.

---

## 2. Brand values

The values that belong to Royal Ambulance. Every other value in this file is shared by all three brands.

| Value | Royal Ambulance |
|---|---|
| Band fill | `--bg-band` #2f193b |
| Band rule | None. The band is solid `--bg-band` to its bottom edge |
| Dark slide fill | `--bg-inverse` #2f193b |
| Dark slide rule | None |
| Accent, for subheads, slide headlines, action numbers and the callout rule | `--fg-accent` #572e72 |
| Callout fill | `--bg-surface` #faf5fd |
| Table header | Fill `--bg-band` #2f193b. Text `--fg-on-dark-1` #FFFFFF, with 0.005em added tracking. No rule |
| Band logo | Role `horizontal-on-dark`, 1.6in wide |
| Title and closing slide logo | Role `horizontal-on-dark`, 2.1in wide |
| Slide footer logo | Role `horizontal-on-light`, 1.43in wide, 0.35in tall |
| Powered by Collective Edge lockup | Once on every document. Section 3.12 |

Shared by every brand: text `--fg-1` #23232A, secondary text `--fg-2` #565860, captions and footers `--fg-3` #6D6D77, hairline `--border-1` #E4E4E9, stronger rule `--border-2` #D0D0D6, page `--bg-canvas` #FFFFFF. On a dark ground: `--fg-on-dark-1` #FFFFFF, `--fg-on-dark-2` #DDDDE3, `--fg-on-dark-3` #A3A4AC, and the rule `--border-on-dark`, white at 12 percent, which is #483553 on #2f193b.

Resolve a logo by role from [`brands.json`](../brands.json), never by filename: `logos` holds the SVG and `logosPng` the PNG. Use the file for the ground. Never recolor one.

---

## 3. Parts

Every document is built from these parts. Sections 4 to 7 say which parts a type uses and in what order.

### 3.1 Band

| | |
|---|---|
| Where | Top of page 1, edge to edge. No band on later pages |
| Size | 8.5in wide, 1.11in tall |
| Fill | `--bg-band` #2f193b |
| Rule | None. The band is solid `--bg-band` to its bottom edge |
| Title | Left, on the left margin, centered vertically. The band-title slot: h2, 24pt, weight 600, uppercase, tracking 0.045em, `--fg-on-dark-1` #FFFFFF. One line, 4 words and 18 characters at most |
| Logo | Right, on the right margin, centered vertically. Role `horizontal-on-dark`, 1.6in wide. Once |
| Padding | Left and right padding is the page margin |

- The band title names the document kind or the topic: Memo, Coverage plan, Operations report.
- The logo appears once in a document, in the band. Never repeat it in the body or the footer.
- The body starts 18pt under the band.

### 3.2 To block

Memo only. Four rows in this order: To, From, Date, Re.

| | |
|---|---|
| Width | The text block |
| Label column | 1.0in wide. body, 12pt, `--fg-3` #6D6D77 |
| Value | body, 12pt, weight 400, `--fg-1` #23232A. The Re value is weight 700. 60 characters at most, one line |
| Date | Day, month, year: 13 November 2026 |
| Rules | 0.75pt `--border-1` #E4E4E9 above the first row and under every row |
| Row padding | 6pt above and under the text |
| Space after | 18pt |

### 3.3 Title block

| | |
|---|---|
| Headline | h1, 30pt, weight 700, `--fg-1` #23232A. Sentence case, ends with a period. 2 lines and 56 characters at most |
| Lead | 12pt under the headline. body-lg, 15pt, weight 400, `--fg-1` #23232A, 6.67in wide at most |

The headline states the finding. It is a sentence, not a label.

### 3.4 Meta row

| | |
|---|---|
| Where | 12pt under the lead |
| Columns | 3 equal columns, 0.25in apart. 3 items at most |
| Label | caption, 9pt, `--fg-3` #6D6D77. 12 characters at most |
| Value | Under the label. body-sm, 10.5pt, weight 600, `--fg-1` #23232A. One line, 24 characters at most |
| Rules | 0.75pt `--border-1` #E4E4E9 above and under the row |
| Padding | 6pt above and under the text |

### 3.5 Headings

| Level | Step | Style | Space above | Space under | Limit |
|---|---|---|---|---|---|
| Section heading, report and generic only | h2, 24pt | weight 700, `--fg-1` #23232A | 36pt | 12pt | 1 line, 40 characters |
| Subhead | h3, 18pt | weight 600, `--fg-accent` #572e72 | 18pt | 6pt | 1 line, 32 characters |

- Sentence case. A heading ends with a period.
- A heading stays with the block under it. It never sits on the last line of a page.
- No label, number or rule above or under a heading.

### 3.6 Body

body, 12pt, weight 400, `--fg-1` #23232A. Flush left, ragged right. 12pt between paragraphs. 5.96in wide at most, about 70 characters a line. Emphasis is weight 700. No italic.

### 3.7 Table

| | |
|---|---|
| Width | The text block. Column widths follow the content and sum to the text block. The first column is the widest. A status column is 1.2in in a document and 1.9in on a slide. Fixed layout, autofit off |
| Caption | Above the table, 6pt gap. caption, 9pt, `--fg-3` #6D6D77. One line, 80 characters at most |
| Header row | Fill `--bg-band` #2f193b. Text `--fg-on-dark-1` #FFFFFF, with 0.005em added tracking. No rule. Weight 600, sentence case, 10.5pt. Padding 6pt above and under, 9pt left and right |
| Body cells | body-sm, 10.5pt, weight 400, `--fg-1` #23232A. Padding 6pt above and under, 9pt left and right |
| Row rule | 0.75pt `--border-1` #E4E4E9 under every body row |
| Frame | No outer frame, no vertical rules, no zebra fill |
| Text | Left-aligned |
| Numbers | Right-aligned, tabular lining figures. The header of a number column is right-aligned too |
| Totals row | Weight 700, with a 0.75pt `--border-2` #D0D0D6 rule above it |
| Space above | 6pt under a subhead, 12pt under a paragraph |

**Status cells.** A 6pt square, then the word at weight 600, both in the alert text color: good `--alert-go-text` #1E7A4D, caution `--alert-warn-text` #926603, bad `--alert-stop-text` #B0322B, notice `--alert-info-text` #2A5A8C. The word carries the meaning. Green means good only. A brand color is never a status color. A status that is neither good, caution nor bad takes the notice color #2A5A8C. In Word and PowerPoint the square is the character U+25A0 in Montserrat SemiBold, in the alert text color, set at 9pt in a document and 12pt on a slide, followed by one no-break space. Montserrat carries the glyph.

**Charts.** Chart colors come from the house data set in [`reference/data-color.md`](data-color.md), never from the brand palette.

### 3.8 Callout

| | |
|---|---|
| Width | The text block |
| Fill | `--bg-surface` #faf5fd |
| Rule | 1.5pt `--fg-accent` #572e72 on the top edge |
| Padding | 12pt above and under, 15pt left and right |
| Text | body, 12pt, `--fg-1` #23232A |
| Space above | 12pt |
| Limit | One per page |

No border, no rounded corners, no icon. A callout holds the one instruction the reader must act on.

### 3.9 Actions

A numbered list, one action per row.

| | |
|---|---|
| Width | 5.96in, the body measure |
| Number | In a 0.33in column. body, 12pt, weight 600, `--fg-accent` #572e72 |
| Text | body, 12pt, `--fg-1` #23232A. 90 characters at most |
| Rules | 0.75pt `--border-1` #E4E4E9 above every row and under the last |
| Row padding | 6pt above and under the text |

### 3.10 Sign-off

Memo only. 24pt under the last block. The sender name in body, 12pt, weight 600, `--fg-1` #23232A. Under it the address or extension in body-sm, 10.5pt, `--fg-3` #6D6D77.

### 3.11 Footer

| | |
|---|---|
| Where | Bottom of every page, inside the margins. The last line sits on the bottom margin |
| Rule | 0.75pt `--border-1` #E4E4E9 on the top edge, the width of the text block |
| Padding | 9pt between the rule and the text |
| Left | The brand name, a middle dot, then the classification or the document title: Royal Ambulance · Internal. Use Internal only when every reader is staff. Otherwise the document title, 40 characters at most |
| Right | Page X of Y |
| Text | caption, 9pt, `--fg-3` #6D6D77. One line |
| Space above | At least 12pt between the last body block and the rule |

Nothing sits under the footer. Nothing but the band crosses a margin.

### 3.12 Powered by Collective Edge

Every Royal Ambulance document carries the lockup exactly once.

| | |
|---|---|
| Label | The words POWERED BY. eyebrow, 9pt, weight 600, uppercase, tracking 0.08em, `--fg-3` #6D6D77. On a dark slide, `--fg-on-dark-3` #A3A4AC |
| Logo | 9pt under the label. The Collective Edge `horizontal-on-light` logo on white, `horizontal-on-dark` on a dark slide. 2.125in wide, 0.354in tall |
| Memo and one-pager | In the footer row, at left. The signature and the page number move to the right, joined by a middle dot, on the bottom line |
| Report and generic | The last block of the body on the last page, at left. A 0.75pt `--border-1` #E4E4E9 rule above it, with 18pt above the rule and 18pt under it. It never sits alone on a page |
| Deck | The closing slide, bottom left. Section 8 |

- Once. Never twice in one document.
- Never inside or touching the Royal Ambulance logo.
- Never set as type where the logo fits.
- The files are in `cobrand.lockup` in [`brands.json`](../brands.json). On white: `https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/for-humans/logos/png/Collective-Edge-horizontal-black-1200w.png`. On a dark slide: `https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/for-humans/logos/png/Collective-Edge-horizontal-white-1200w.png`.

---

## 4. Memo

A message from a named sender to named readers. The band title is the word Memo.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.75in on all four sides |
| Text block | 7.0in wide, one column |
| Body measure | 5.96in, 70 characters |
| Pages | 1. 2 at most |
| Parts, top to bottom | band, to-block, body, table, subhead, actions, sign-off, footer |
| Lockup | Footer row, left. Signature and page number at right, on the bottom line |
| Template | [`templates/memo.html`](../templates/memo.html) |

| Slot | What it holds | Step | Print | Screen | Weight | Color | Limit | Floor |
|---|---|---|---|---|---|---|---|---|
| band-title | Names the document kind or the topic. Uppercase, tracking 0.045em | h2 | 24pt | 32px | 600 | `--fg-on-dark-1` #FFFFFF | 4 words, 18 characters, 1 line | h3 18pt |
| to-value | To, From, Date and Re values | body | 12pt | 16px | 400 | `--fg-1` #23232A | 60 characters, 1 line | body 12pt |
| body | Running text. Four paragraphs and 520 characters in all on one page | body | 12pt | 16px | 400 | `--fg-1` #23232A | 520 characters, 4 paragraphs | body-sm 10.5pt |
| table-text | Table cells. Header cells take weight 600. Optional. One table under the last paragraph | body-sm | 10.5pt | 14px | 400 | `--fg-1` #23232A | 4 rows, 4 columns | caption 9pt |
| subhead | Heading inside the body | h3 | 18pt | 24px | 600 | `--fg-accent` #572e72 | 32 characters, 1 line | h3 18pt |
| action | One numbered action per row. The number is weight 600 in --fg-accent. Three actions on one page | body | 12pt | 16px | 400 | `--fg-1` #23232A | 90 characters, 3 actions | body-sm 10.5pt |
| sign-name | Sender name | body | 12pt | 16px | 600 | `--fg-1` #23232A | 40 characters | body 12pt |
| sign-contact | Sender address or extension | body-sm | 10.5pt | 14px | 400 | `--fg-3` #6D6D77 | 48 characters | body-sm 10.5pt |
| footer | Signature at left, page number at right | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 60 characters, 1 line | caption 9pt |
| lockup-label | The words POWERED BY above the lockup. Uppercase, tracking 0.08em | eyebrow | 9pt | 12px | 600 | `--fg-3` #6D6D77 | none | eyebrow 9pt |

- No headline. The Re row is the subject.
- Band, To block, body, sign-off and footer are required. Table, subhead and actions are optional. A closing line is the last body paragraph.
- One table at most, 4 body rows and 4 columns, under the last paragraph, built to section 3.7. On one page it takes the place of three paragraphs and 390 characters of the body budget. A memo that needs more is a report.
- Past one page, the memo runs to a second page with the same margins and footer and no band. Past two pages it is a report.

## 5. One-pager

One finding on exactly one page. The headline states it.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.6in on all four sides |
| Text block | 7.3in wide, one column |
| Body measure | 5.96in, 70 characters |
| Pages | Exactly 1 |
| Parts, top to bottom | band, title-block, meta-row, subhead, body, table, callout, footer |
| Lockup | Footer row, left. Signature and page number at right, on the bottom line |
| Template | [`templates/one-pager.html`](../templates/one-pager.html) |

| Slot | What it holds | Step | Print | Screen | Weight | Color | Limit | Floor |
|---|---|---|---|---|---|---|---|---|
| band-title | Names the document kind or the topic. Uppercase, tracking 0.045em | h2 | 24pt | 32px | 600 | `--fg-on-dark-1` #FFFFFF | 4 words, 18 characters, 1 line | h3 18pt |
| headline | States the finding in one sentence | h1 | 30pt | 40px | 700 | `--fg-1` #23232A | 56 characters, 2 lines | h2 24pt |
| lead | One or two sentences under the headline | body-lg | 15pt | 20px | 400 | `--fg-1` #23232A | 110 characters, 2 lines | body 12pt |
| meta-label | Label in the meta row | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 12 characters | caption 9pt |
| meta-value | Value in the meta row | body-sm | 10.5pt | 14px | 600 | `--fg-1` #23232A | 24 characters, 1 line | body-sm 10.5pt |
| subhead | Heading inside the body | h3 | 18pt | 24px | 600 | `--fg-accent` #572e72 | 32 characters, 1 line, 2 subheads | h3 18pt |
| body | Running text. One paragraph of three lines under the first subhead | body | 12pt | 16px | 400 | `--fg-1` #23232A | 210 characters, 1 paragraph | body-sm 10.5pt |
| table-text | Table cells. Header cells take weight 600. One table under the second subhead. Four body rows and five columns. Six rows when the page has no callout | body-sm | 10.5pt | 14px | 400 | `--fg-1` #23232A | 4 rows, 5 columns | caption 9pt |
| callout | The one instruction the reader must act on | body | 12pt | 16px | 400 | `--fg-1` #23232A | 140 characters, 1 callout | body-sm 10.5pt |
| footer | Signature at left, page number at right | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 60 characters, 1 line | caption 9pt |
| lockup-label | The words POWERED BY above the lockup. Uppercase, tracking 0.08em | eyebrow | 9pt | 12px | 600 | `--fg-3` #6D6D77 | none | eyebrow 9pt |

- Exactly one page. Never a second.
- One table or one chart, never both.
- One callout at most.
- The page holds two subheads. The first sits over one paragraph. The second sits over the table.
- A chart takes the place of the table and its height: 2.2in at most.

## 6. Report

A document of three pages or more, in sections. Page 1 opens with the band, the title block and the meta row. The first section follows on the same page.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.75in on all four sides |
| Text block | 7.0in wide, one column |
| Body measure | 5.96in, 70 characters |
| Pages | 3 or more |
| Parts, top to bottom | band, title-block, meta-row, section-heading, subhead, body, table, callout, actions, lockup, footer |
| Lockup | Last block of the body on the last page, left, under a 0.75pt --border-1 rule with 18pt above the rule and 18pt under it |
| Template | [`templates/document.html`](../templates/document.html) |

| Slot | What it holds | Step | Print | Screen | Weight | Color | Limit | Floor |
|---|---|---|---|---|---|---|---|---|
| band-title | Names the document kind or the topic. Uppercase, tracking 0.045em | h2 | 24pt | 32px | 600 | `--fg-on-dark-1` #FFFFFF | 4 words, 18 characters, 1 line | h3 18pt |
| headline | States the finding in one sentence | h1 | 30pt | 40px | 700 | `--fg-1` #23232A | 56 characters, 2 lines | h2 24pt |
| lead | Two or three sentences under the headline | body-lg | 15pt | 20px | 400 | `--fg-1` #23232A | 180 characters, 3 lines | body 12pt |
| meta-label | Label in the meta row | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 12 characters | caption 9pt |
| meta-value | Value in the meta row | body-sm | 10.5pt | 14px | 600 | `--fg-1` #23232A | 24 characters, 1 line | body-sm 10.5pt |
| section-heading | Opens a section | h2 | 24pt | 32px | 700 | `--fg-1` #23232A | 40 characters, 1 line | h2 24pt |
| subhead | Heading inside the body | h3 | 18pt | 24px | 600 | `--fg-accent` #572e72 | 32 characters, 1 line | h3 18pt |
| body | Running text | body | 12pt | 16px | 400 | `--fg-1` #23232A | none | body-sm 10.5pt |
| table-text | Table cells. Header cells take weight 600. Twelve body rows and six columns at most per table | body-sm | 10.5pt | 14px | 400 | `--fg-1` #23232A | 12 rows, 6 columns | caption 9pt |
| caption | Line above a table or figure | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 80 characters, 1 line | caption 9pt |
| callout | The one instruction the reader must act on | body | 12pt | 16px | 400 | `--fg-1` #23232A | 200 characters, 1 callout | body-sm 10.5pt |
| action | One numbered action per row. The number is weight 600 in --fg-accent | body | 12pt | 16px | 400 | `--fg-1` #23232A | 90 characters, 7 actions | body-sm 10.5pt |
| footer | Signature at left, page number at right | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 60 characters, 1 line | caption 9pt |
| lockup-label | The words POWERED BY above the lockup. Uppercase, tracking 0.08em | eyebrow | 9pt | 12px | 600 | `--fg-3` #6D6D77 | none | eyebrow 9pt |

- The band is on page 1 only.
- Every page carries the footer.
- A heading never sits on the last line of a page.
- A table stays whole on one page, with its caption.

## 7. Generic branded document

The fallback. An agenda, a letter, a policy, a checklist, a form. It is a report with fewer parts: the band, a headline, then whatever the content needs, in the order given.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.75in on all four sides |
| Text block | 7.0in wide, one column |
| Body measure | 5.96in, 70 characters |
| Pages | As many as the content needs |
| Parts, top to bottom | band, title-block, section-heading, subhead, body, table, callout, actions, lockup, footer |
| Lockup | Last block of the body on the last page, left, under a 0.75pt --border-1 rule with 18pt above the rule and 18pt under it |
| Template | [`templates/document.html`](../templates/document.html) |

| Slot | What it holds | Step | Print | Screen | Weight | Color | Limit | Floor |
|---|---|---|---|---|---|---|---|---|
| band-title | Names the document kind or the topic. Uppercase, tracking 0.045em | h2 | 24pt | 32px | 600 | `--fg-on-dark-1` #FFFFFF | 4 words, 18 characters, 1 line | h3 18pt |
| headline | Names the document | h1 | 30pt | 40px | 700 | `--fg-1` #23232A | 56 characters, 2 lines | h2 24pt |
| lead | Optional. One or two sentences | body-lg | 15pt | 20px | 400 | `--fg-1` #23232A | 180 characters, 3 lines | body 12pt |
| section-heading | Opens a section | h2 | 24pt | 32px | 700 | `--fg-1` #23232A | 40 characters, 1 line | h2 24pt |
| subhead | Heading inside the body | h3 | 18pt | 24px | 600 | `--fg-accent` #572e72 | 32 characters, 1 line | h3 18pt |
| body | Running text | body | 12pt | 16px | 400 | `--fg-1` #23232A | none | body-sm 10.5pt |
| table-text | Table cells. Header cells take weight 600. Twelve body rows and six columns at most per table | body-sm | 10.5pt | 14px | 400 | `--fg-1` #23232A | 12 rows, 6 columns | caption 9pt |
| caption | Line above a table or figure | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 80 characters, 1 line | caption 9pt |
| callout | The one instruction the reader must act on | body | 12pt | 16px | 400 | `--fg-1` #23232A | 200 characters, 1 callout | body-sm 10.5pt |
| action | One numbered action per row. The number is weight 600 in --fg-accent | body | 12pt | 16px | 400 | `--fg-1` #23232A | 90 characters, 7 actions | body-sm 10.5pt |
| footer | Signature at left, page number at right | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 60 characters, 1 line | caption 9pt |
| lockup-label | The words POWERED BY above the lockup. Uppercase, tracking 0.08em | eyebrow | 9pt | 12px | 600 | `--fg-3` #6D6D77 | none | eyebrow 9pt |

- Build it as a report without the meta row.
- Use only the parts the content needs. Keep their order.
- The band title names the kind of document: Agenda, Policy, Checklist.

---

## 8. Deck

| | |
|---|---|
| Slide | 13.333 x 7.5in, 16:9. 12192000 x 6858000 EMU |
| Padding | 0.67in top, 0.83in left and right, 0.42in bottom |
| Content width | 11.67in. Two columns are 5.5in each, 0.67in apart |
| White slides | Fill `--bg-canvas` #FFFFFF: statement, text, two-column, chart, table, comparison, timeline, quote, summary |
| Dark slides | Fill `--bg-inverse` #2f193b: title, divider, closing |
| Dark slide rule | None |
| Body size | 15pt. Floor 12pt |
| Template | [`templates/deck.html`](../templates/deck.html) |

- One message per slide. The headline states it as a sentence.
- Body text is 15pt. Nothing on a slide is under 12pt, except the POWERED BY label at 9pt.
- Content slides are white. Only title, divider and closing are dark.
- Dark slides are flat `--bg-inverse` #2f193b. No picture background.
- Uppercase is for the title slide title only. Four words at most.
- A headline that takes one line still reserves two. The body zone starts at y 2.53in on every white slide.
- One chart or one table per slide.
- No logo on a dark slide except title and closing.

### Zones

| Zone | x | y | Width | Height |
|---|---|---|---|---|
| Headline | 0.83in | 0.67in | 10.0in | 1.28in |
| Body zone | 0.83in | 2.53in | 11.67in | 3.78in |
| Left column | 0.83in | 2.53in | 5.5in | 3.78in |
| Right column | 7.0in | 2.53in | 5.5in | 3.78in |
| Footer row | 0.83in | 6.73in | 11.67in | 0.35in |
| Footer rule | 0.83in | 6.55in | 11.67in | 0.75pt |

**Footer.** On a white slide: the rule is `--border-1` #E4E4E9. The logo sits at left on the footer row, role `horizontal-on-light`, 1.43in wide, centered on the row. The page number sits at right, ending at x 12.5in, in body, 12pt, `--fg-3` #6D6D77. It is the slide’s position in the deck as a bare numeral, in a box at 10.5in, 6.73in, 2.0in by 0.35in, right-aligned, anchored middle. The title slide is 1 and shows no number. On a dark slide: the rule is `--border-on-dark` #483553, the text is `--fg-on-dark-3` #A3A4AC, and there is no footer logo.

### Type on a slide

| Slot | What it holds | Step | Print | Screen | Weight | Color | Limit | Floor |
|---|---|---|---|---|---|---|---|---|
| headline | The one message of the slide, as a sentence | display-md | 42pt | 56px | 800 | `--fg-accent` #572e72 | 60 characters, 2 lines | h1 30pt |
| body | Paragraphs and bullets | body-lg | 15pt | 20px | 400 | `--fg-1` #23232A | none | body 12pt |
| key-point | A short statement between hairlines | h3 | 18pt | 24px | 600 | `--fg-1` #23232A | 60 characters, 2 lines | h4 15pt |
| table-text | Table cells. Header cells take weight 600 | body-lg | 15pt | 20px | 400 | `--fg-1` #23232A | none | body 12pt |
| caption | Line above a table or chart, and the source line | body | 12pt | 16px | 400 | `--fg-3` #6D6D77 | 60 characters, 1 line | body 12pt |
| footer | Page number, and the meta row on dark slides | body | 12pt | 16px | 400 | `--fg-3` #6D6D77 | none | body 12pt |

- **Bullets.** A round bullet in `--fg-accent` #572e72, text indented 0.33in, 9pt between bullets.
- **Key points.** Each point sits between 0.75pt `--border-1` #E4E4E9 rules, with 12pt above and under the text.
- **Tables.** The table rules of section 3.7 at 15pt. Header padding 6pt above and under, 12pt left and right. Cell padding 9pt above and under, 12pt left and right. The status square is 9pt: U+25A0 set at 12pt.

### Layouts

Twelve layouts. Use these names.

| Layout | Ground | Purpose |
|---|---|---|
| title | dark | Opens the deck |
| divider | dark | Opens a section |
| statement | white | One sentence that stands alone |
| text | white | A headline and one column of text |
| two-column | white | Key points beside one table, image or block of text |
| chart | white | One chart |
| table | white | One table |
| comparison | white | Two options or two states side by side |
| timeline | white | Three to five dated steps in a row |
| quote | white | One quotation with its source |
| summary | white | The takeaways, numbered |
| closing | dark | Ends the deck |

**title**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| logo | Logo, role `horizontal-on-dark` |  | 0.83in, 0.67in | 2.1in wide |  |
| title | display-lg, 54pt, weight 700, `--fg-on-dark-1` #FFFFFF. uppercase, tracking 0.025em | 4 words, 28 characters, 2 lines, floor display-md 42pt | 0.83in, 3.85in | 11.67in, 1.62in | Text sits on the bottom of the box |
| subtitle | h3, 18pt, weight 600, `--fg-on-dark-2` #DDDDE3 | 60 characters, 1 line, floor h4 15pt | 0.83in, 5.64in | 11.67in, 0.34in |  |
| rule | 0.75pt `--border-on-dark` #483553 |  | 0.83in, 6.55in | 11.67in | Above the meta row |
| meta-left | body, 12pt, weight 400, `--fg-on-dark-3` #A3A4AC | 40 characters | 0.83in, 6.73in | 5.5in, 0.35in | Brand or presenter |
| meta-right | body, 12pt, weight 400, `--fg-on-dark-3` #A3A4AC | 24 characters | 7.0in, 6.73in | 5.5in, 0.35in | Date. Right-aligned |

**divider**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| number | h3, 18pt, weight 600, `--fg-on-dark-3` #A3A4AC | 2 characters | 0.83in, 4.19in | 11.67in, 0.34in | Two digits, tabular figures |
| title | display-md, 42pt, weight 700, `--fg-on-dark-1` #FFFFFF | 40 characters, 2 lines, floor h1 30pt | 0.83in, 4.7in | 10.0in, 1.28in | Text sits on the bottom of the box |
| rule | 0.75pt `--border-on-dark` #483553 |  | 0.83in, 6.55in | 11.67in | Above the meta row |
| meta-left | body, 12pt, weight 400, `--fg-on-dark-3` #A3A4AC | 40 characters | 0.83in, 6.73in | 5.5in, 0.35in | Brand name |
| page-number | body, 12pt, weight 400, `--fg-on-dark-3` #A3A4AC |  | 7.0in, 6.73in | 5.5in, 0.35in | Right-aligned |

**statement**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| statement | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 120 characters, 4 lines, floor h1 30pt | 0.83in, 0.67in | 10.0in, 2.57in |  |
| support | body-lg, 15pt, weight 400, `--fg-1` #23232A | 140 characters, 2 lines, floor body 12pt | 0.83in, 3.57in | 7.45in, 0.65in | Optional |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**text**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| headline | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 60 characters, 2 lines | 0.83in, 0.67in | 10.0in, 1.28in | The message, as a sentence |
| body | body-lg, 15pt, weight 400, `--fg-1` #23232A | 80 characters, 5 bullets, floor body 12pt | 0.83in, 2.53in | 7.45in, 3.78in | Up to five bullets of 80 characters, or up to three paragraphs of 420 characters in all |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**two-column**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| headline | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 60 characters, 2 lines | 0.83in, 0.67in | 10.0in, 1.28in | The message, as a sentence |
| key-points | h3, 18pt, weight 600, `--fg-1` #23232A | 60 characters, 3 points, floor h4 15pt | 0.83in, 2.53in | 5.5in, 3.78in | Each point sits between 0.75pt --border-1 rules with 12pt above and under the text |
| right | body-lg, 15pt, weight 400, `--fg-1` #23232A | floor body 12pt | 7.0in, 2.53in | 5.5in, 3.78in | One table of four rows by three columns at most, or three bullets, or one image. A caption may sit above it |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**chart**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| headline | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 60 characters, 2 lines | 0.83in, 0.67in | 10.0in, 1.28in | The message, as a sentence |
| chart |  | 1 chart, 4 series | 0.83in, 2.53in | 7.5in, 3.78in | One chart. Colors from reference/data-color.md. Caption above, source line under, both in the caption slot. A bar chart holds four categories by two series |
| notes | body-lg, 15pt, weight 400, `--fg-1` #23232A | 60 characters, 3 points, floor body 12pt | 8.67in, 2.53in | 3.83in, 3.78in | Optional. Without notes the chart takes the full 11.67in |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**table**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| headline | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 60 characters, 2 lines | 0.83in, 0.67in | 10.0in, 1.28in | The message, as a sentence |
| table | body-lg, 15pt, weight 400, `--fg-1` #23232A | 5 rows, 6 columns, floor body 12pt | 0.83in, 2.53in | 11.67in, 3.78in | Five body rows at 15pt. Six at the 12pt floor. Cell padding 9pt top and bottom, 12pt left and right |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**comparison**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| headline | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 60 characters, 2 lines | 0.83in, 0.67in | 10.0in, 1.28in | The message, as a sentence |
| left | body-lg, 15pt, weight 400, `--fg-1` #23232A | 60 characters, 4 bullets, floor body 12pt | 0.83in, 2.53in | 5.5in, 3.78in | A label in the key-point slot, 24 characters at most, over a 1.5pt --fg-accent rule, then up to four bullets |
| right | body-lg, 15pt, weight 400, `--fg-1` #23232A | 60 characters, 4 bullets, floor body 12pt | 7.0in, 2.53in | 5.5in, 3.78in | The same as the left column |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**timeline**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| headline | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 60 characters, 2 lines | 0.83in, 0.67in | 10.0in, 1.28in | The message, as a sentence |
| steps | body-lg, 15pt, weight 400, `--fg-1` #23232A | 3 to 5 steps, floor body 12pt | 0.83in, 2.53in | 11.67in, 3.78in | Equal columns, 0.33in apart. Each step: a 1.5pt --fg-accent rule, the date at 15pt weight 600 in --fg-accent and 14 characters at most, a title in the key-point slot and 24 characters at most, a description at 15pt and 60 characters at most |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**quote**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| quote | display-md, 42pt, weight 800, `--fg-1` #23232A | 120 characters, 4 lines, floor h1 30pt | 0.83in, 0.67in | 10.0in, 2.57in | Curly quotation marks |
| attribution | body-lg, 15pt, weight 400, `--fg-2` #565860 | 80 characters, 1 line, floor body 12pt | 0.83in, 3.57in | 10.0in, 0.33in | Name at weight 700 in --fg-1, a comma, then the role |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**summary**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| headline | display-md, 42pt, weight 800, `--fg-accent` #572e72 | 60 characters, 2 lines | 0.83in, 0.67in | 10.0in, 1.28in | The message, as a sentence |
| takeaways | h3, 18pt, weight 600, `--fg-1` #23232A | 70 characters, 4 takeaways, floor h4 15pt | 0.83in, 2.53in | 11.67in, 3.78in | One row each between 0.75pt --border-1 rules. The number sits in a 0.5in column at weight 600 in --fg-accent |
| footer | body, 12pt, `--fg-3` #6D6D77 | | 0.83in, 6.73in | 11.67in, 0.35in | Logo left, page number right |

**closing**

| Slot | Style | Limit | x, y | Width, height | Notes |
|---|---|---|---|---|---|
| logo | Logo, role `horizontal-on-dark` |  | 0.83in, 0.67in | 2.1in wide |  |
| closing-line | display-md, 42pt, weight 700, `--fg-on-dark-1` #FFFFFF | 60 characters, 2 lines, floor h1 30pt | 0.83in, 3.14in | 10.0in, 1.28in | Text sits on the bottom of the box |
| contact | body-lg, 15pt, weight 400, `--fg-on-dark-2` #DDDDE3 | 48 characters, 3 lines, floor body 12pt | 0.83in, 4.59in | 10.0in, 1.0in |  |
| lockup |  |  | 0.83in, 6.42in | 2.125in, 0.66in | A 0.75pt `--border-on-dark` #483553 rule at y 6.17in, 11.67in wide. The label POWERED BY at y 6.42in in `--fg-on-dark-3` #A3A4AC: 9pt, weight 600, uppercase, tracking 0.08em, in a box 2.125in by 0.18in. The Collective Edge `horizontal-on-dark` logo at y 6.72in, 2.125in wide, 0.354in tall. The lockup takes the place of the brand and date row. The only place in the deck the lockup appears |

---

## 9. Type by role

One face, Montserrat. Four weights: 400, 600, 700, 800. No italic. Sizes come from the house scale in [`snippets/type-tokens.json`](../snippets/type-tokens.json). Leading is given in points so it can be set exactly.

| Step | Print | Screen | Leading | Used for in a document | Used for on a slide |
|---|---|---|---|---|---|
| display-lg | 54pt | 72px | 58.3pt |  | Title slide title |
| display-md | 42pt | 56px | 46.2pt |  | Headline, statement, quote, divider title, closing line |
| h1 | 30pt | 40px | 35.4pt | Headline | Floor for display-md |
| h2 | 24pt | 32px | 30pt | Band title, section heading |  |
| h3 | 18pt | 24px | 24.3pt | Subhead | Key points, subtitle, column labels |
| h4 | 15pt | 20px | 21.8pt |  | Floor for h3 |
| body-lg | 15pt | 20px | 23.3pt | Lead | Body, bullets, tables |
| body | 12pt | 16px | 19.2pt | Body, To block, actions, callout | Caption, source line, footer, page number. The floor |
| body-sm | 10.5pt | 14px | 16.3pt | Table text, meta value, sign-off contact | Not used |
| caption | 9pt | 12px | 13.1pt | Caption, meta label, footer | Not used |
| eyebrow | 9pt | 12px | 13.1pt | Lockup label | Lockup label only |

- **Weights.** 400 for running text. 600 for subheads, table headers, labels and key points. 700 for headlines, section headings and emphasis. 800 for a slide headline on white only.
- **On a dark ground.** A step at 700 or 800 drops one weight: the band title is 600, a dark slide title is 700. Every step gains 0.005em of tracking. In Word and PowerPoint, skip that gain under 24pt.
- **Tracking.** Band title 0.045em. Title slide title 0.025em. Lockup label 0.08em. Document headline -0.012em. Slide headline -0.015em. Subhead -0.004em. No other slot is tracked. Section 11 gives each in points.
- **Color.** Text is `--fg-1` #23232A. `--fg-accent` #572e72 is for subheads, slide headlines, action numbers and bullets. `--fg-3` #6D6D77 is the lightest text color.
- **Uppercase.** The band title, the title slide title and the lockup label. Nowhere else. Always tracked, never past four words.
- **Office fonts.** Word and PowerPoint need the static files installed: Montserrat for 400 and 700, Montserrat SemiBold for 600, Montserrat ExtraBold for 800. Name the family, not a synthetic bold.

---

## 10. When content does not fit

Work down this list and stop at the first step that fits.

1. **Tighten.** Set the overflowing slot one step down the scale, to its floor and no further.
2. **Shorten.** Cut the text to the limit of the slot.
3. **Split.** Move the overflow to another page or slide. A one-pager cannot split.
4. **Switch.** Rebuild in the denser sibling type or layout.

| Type or layout | Denser sibling |
|---|---|
| memo | report |
| one-pager | report |
| text slide | two-column slide |
| two-column slide | table slide |
| statement slide | text slide |
| quote slide | text slide |
| summary slide | text slide |
| comparison slide | table slide |
| timeline slide | table slide |

- Never set type under its floor.
- Never rely on auto-fit or shrink-on-overflow.
- Never narrow a margin.
- Never tighten leading or tracking to make text fit.
- A table past its row limit splits into two tables with the header row repeated.

---

## 11. Tools

The same page in each tool. A value not listed here comes from the section named.

### Word, with python-docx

| Rule | How |
|---|---|
| Page and margins | `section.page_width = Inches(8.5)`, `section.page_height = Inches(11)`. All four margins `Inches(0.75)`, or `Inches(0.6)` for a one-pager |
| Body | Style `Normal`: Montserrat, 12pt, color #23232A, line spacing exactly 19.2pt, space after 0, no indent, left-aligned. Body paragraphs add space after 12pt and right indent 1.04in, or 1.34in on a one-pager, so a line is 5.96in wide. Every paragraph in a table cell, the band, the To block, the meta row, the callout and the footer sets right indent 0, space before 0, space after 0, and line spacing exactly at its own step from section 9 |
| Fonts in XML | On every style and run, replace `w:rFonts` with one element carrying `w:ascii`, `w:hAnsi`, `w:cs` and `w:eastAsia`, all set to the font name. Remove every `w:asciiTheme`, `w:hAnsiTheme`, `w:cstheme` and `w:eastAsiaTheme`. Remove `w:pBdr` from `Title`. Set the color on every style |
| Tracking | Tracking in points is em times the size. `w:spacing w:val` on the run, in twentieths of a point. Band title 1.08pt, `w:val="22"`. Lockup label 0.72pt, `w:val="14"`. Headline -0.36pt, `w:val="-7"`. Subhead -0.07pt, `w:val="-1"`. Set no other tracking. Type the capitals of the band title and the lockup label. Do not use the all-caps attribute |
| Headline | Style `Title`: Montserrat, 30pt, bold, line spacing exactly 35.4pt, space after 12pt |
| Lead | Style `Subtitle`: Montserrat, 15pt, line spacing exactly 23.3pt, right indent 0.33in, or 0.63in on a one-pager, so a line is 6.67in wide |
| Section heading | Style `Heading 1`: Montserrat, 24pt, bold, #23232A, space before 36pt, after 12pt, keep with next |
| Subhead | Style `Heading 2`: font `Montserrat SemiBold`, 18pt, not bold, #572e72, space before 18pt, after 6pt, keep with next |
| Caption and footer | Style `Caption`: Montserrat, 9pt, #6D6D77, line spacing exactly 13.1pt |
| Band | A one-row, two-cell table in the first-page header. `section.different_first_page_header_footer = True`, `section.header_distance = 0`. Table indent minus the left margin, width 8.5in, row height exactly 1.11in, cell shading #2f193b, no borders. Left cell: the band title, vertically centered, left cell margin equal to the page margin. Right cell: the logo, right-aligned, right cell margin equal to the page margin. Word starts the body under a header that is taller than the top margin. Move the header’s empty paragraph to after the table and set its line spacing to exactly 18pt, space before and after 0. It is the 18pt gap under the band. Leave no paragraph above the table |
| To block | A 4-row, 2-column table, no table style, columns 1.0in and the rest of the text block. Top border 0.75pt #E4E4E9 on row 1, bottom border 0.75pt #E4E4E9 on every row, no other border. Cell margins 6pt top and bottom, 0 left and right. Labels To, From, Date, Re, weight 400, no colon. An empty paragraph after it, line spacing exactly 18pt |
| Meta row | A 1-row, 3-column table the width of the text block. Top and bottom border 0.75pt #E4E4E9, no other border. Cell margins 6pt top and bottom, 0 left, 0.25in right on the first two cells. In each cell the label paragraph, then the value paragraph |
| Table | `doc.add_table` with no table style. Header cells shaded #2f193b, text #FFFFFF. Every body cell: bottom border 0.75pt #E4E4E9, no other border. Cell margins 6pt top and bottom, 9pt left and right. Number cells `WD_ALIGN_PARAGRAPH.RIGHT` |
| Callout | A one-cell table the width of the text block. Shading #faf5fd, top border 1.5pt #572e72, cell margins 12pt top and bottom, 15pt left and right |
| Actions | A 2-column table, no table style, columns 0.33in and 5.63in. Top border 0.75pt #E4E4E9 on every row and a bottom border on the last. Cell margins 6pt top and bottom, 0 left and right. The number in the first cell, `Montserrat SemiBold`, #572e72 |
| Sign-off | Two paragraphs. The first, the name, has space before 24pt |
| Footer | `section.footer_distance` equal to the bottom margin. A paragraph with a 0.75pt #E4E4E9 top border, 9pt between border and text, and a right tab stop at the text block width. Page numbers are `PAGE` and `NUMPAGES` fields. Build the footer twice, in `section.first_page_footer` and in `section.footer`. With a different first page switched on, page 1 shows only the first-page footer |
| Lockup | Memo and one-pager: a 1-row, 2-column table in both footers, in place of the footer paragraph, the width of the text block, columns 2.4in and the rest. Top border 0.75pt #E4E4E9 on both cells, top cell margin 9pt, other margins 0. Left cell: the label paragraph with space after 9pt, then the logo paragraph. Right cell: vertical alignment bottom, one right-aligned 9pt paragraph: brand, middle dot, Page X of Y. Set the paragraph Word leaves after the table to line spacing exactly 1pt. Report and generic: the last body paragraphs, kept with the block before, under a paragraph with a 0.75pt #E4E4E9 top border. Logo `add_picture(path, width=Inches(2.125))` |
| Logo | `add_picture(path, width=Inches(1.6))`. PNG from `for-humans/logos/png/`, by role, from `logosPng` in `brands.json`, since Word does not place SVG through python-docx |

### PowerPoint, with python-pptx

| Rule | How |
|---|---|
| Slide size | `prs.slide_width = Emu(12192000)`, `prs.slide_height = Emu(6858000)` |
| Layout | Start every slide from the blank layout. Place each slot as a text box at the x, y, width and height in section 8 |
| Text boxes | `word_wrap = True`, `auto_size = MSO_AUTO_SIZE.NONE`, all four insets 0. Set font name, size and color on every run. Set `a:latin`, `a:ea` and `a:cs` on every run |
| Tracking | Tracking in points is em times the size. `spc` on `a:rPr`, in hundredths of a point. Title slide title 1.35pt, `spc="135"`. Slide headline -0.63pt, `spc="-63"`. Lockup label 0.72pt, `spc="72"`. Set no other tracking. Type the capitals of the title slide title and the lockup label. Do not use the all-caps attribute |
| Ground | White slides: background #FFFFFF. Dark slides: background #2f193b |
| Headline | Text box at 0.83in, 0.67in, 10.0in by 1.28in. `Montserrat ExtraBold`, 42pt, #572e72, line spacing 46.2pt, anchored top |
| Body | `Montserrat`, 15pt, #23232A, line spacing 23.3pt |
| Bullets | `a:buChar` U+2022, `a:buClr` #572e72, `marL` 0.33in, `indent` -0.33in, space before 9pt |
| Rules | A line shape, 0.75pt, #E4E4E9 on white or #483553 on dark |
| Table | `shapes.add_table` in the body zone. Set `a:tableStyleId` to `{2D5ABB26-0587-4C30-8999-92F81FD0307C}` and `firstRow` and `bandRow` to 0. On every cell write `a:lnL`, `a:lnR`, `a:lnT` and `a:lnB` in `a:tcPr`: `a:noFill` for no border, or `w` in EMU with a solid fill. 0.75pt is 9525. 1.5pt is 19050. Header cells: fill #2f193b, text #FFFFFF, no border. Body cells no fill, bottom border 0.75pt #E4E4E9, no other border. Header row height 0.49in, body rows 0.57in. Columns in proportion to content, summing to 11.67in |
| Chart | In the chart box of the chart layout. Series colors from `reference/data-color.md`, in order |
| Footer | Logo picture at x 0.83in, 1.43in wide, centered on the 0.35in row at y 6.73in. Page number text box at 10.5in, 6.73in, 2.0in by 0.35in, right-aligned, anchored middle. Static text, the bare slide number |

### Google Docs

| Named style | Role |
|---|---|
| Title | Headline, 30pt, bold |
| Subtitle | Lead, 15pt |
| Heading 1 | Section heading, 24pt, bold |
| Heading 2 | Subhead, 18pt, Montserrat SemiBold, #572e72 |
| Normal text | Body, 12pt, line spacing 1.31, 12pt after a paragraph |

Page setup: Letter, portrait, margins from section 1. Apply named styles only. The band is a two-cell table at the top of page 1 with cell fill #2f193b and no borders, set to the full text block width where the page edge cannot be reached. Tables, the callout and the footer follow the Word rows above.

### Google Slides

Page size 13.333 x 7.5in. One layout per name in section 8, with the same twelve names. Each placeholder sits at the x, y, width and height given there. Autofit is off on every placeholder.

### HTML

The templates carry every rule as a class. Load `type-system.css`, then this kit’s `palette.css`, then `cobrand.css`.

| Part | Class |
|---|---|
| Page | `.sheet`, with `--page-margin` set to 0.75in or 0.6in |
| Band | `.doc-band`, `.doc-band-title` with `.bk-h2 .bk-caps`, `.doc-band-logo` |
| To block | `.doc-to`, `.doc-to-row`, `.doc-to-label` |
| Title block | `.doc-headline` with `.bk-h1`, `.doc-lead` with `.bk-body-lg` |
| Meta row | `.doc-meta`, `.doc-meta-value` |
| Headings | `.doc-h2` with `.bk-h2`, `.doc-h3` with `.bk-h3` |
| Body | `.doc-p` with `.bk-body` |
| Table | `.doc-table-wrap`, `.doc-caption`, `.doc-table`, `.num`, `.doc-status` with `.is-go`, `.is-warn`, `.is-stop` or `.is-info` |
| Callout | `.doc-callout` |
| Actions | `.doc-actions`, `.doc-actions-item`, `.doc-actions-n` |
| Sign-off | `.doc-sign`, `.doc-sign-name`, `.doc-sign-contact` |
| Footer | `.doc-footer` |
| Lockup | `.ce-powered .ce-powered-light`, plus `.doc-lockup` in a report. `.ce-powered` alone on the closing slide |
| Slide | `.slide`, plus `.slide-dark .bk-on-dark` on a dark slide |
| Slide layouts | `.slide-title`, `.slide-divider`, `.slide-statement`, `.slide-text`, `.slide-two-column`, `.slide-chart-slide`, `.slide-table-slide`, `.slide-comparison`, `.slide-timeline`, `.slide-quote`, `.slide-summary`, `.slide-closing` |
| Slide parts | `.slide-headline`, `.slide-body`, `.slide-cols`, `.slide-points`, `.slide-bullets`, `.slide-table`, `.slide-chart`, `.slide-steps`, `.slide-foot` |

| Template | Type |
|---|---|
| [`templates/memo.html`](../templates/memo.html) | memo |
| [`templates/one-pager.html`](../templates/one-pager.html) | one-pager |
| [`templates/document.html`](../templates/document.html) | report and generic |
| [`templates/deck.html`](../templates/deck.html) | deck, all twelve layouts |
| [`snippets/header-band.html`](../snippets/header-band.html) | the band alone |
| [`Examples/royal-one-pager.html`](../Examples/royal-one-pager.html) | A filled one-pager. A reference, not a starting point |
| [`Examples/HPSM_Ordering_Workflow_Manager.html`](../Examples/HPSM_Ordering_Workflow_Manager.html) | A partner document that predates this standard. No lockup, its own layout. Not a model |

---

## 12. Check before delivery

Each line can be measured. A document that fails one is not finished.

1. **Page count.** A one-pager is exactly 1 page. A memo is 1 page, 2 at most. A deck has one message per slide.
2. **Page size and margins.** Letter, portrait, 0.75in margins, or 0.6in on a one-pager. Slides are 13.333 x 7.5in.
3. **Nothing past the margins.** Only the band crosses a margin. No text box, table or picture ends outside the text block or the slide padding.
4. **Fonts.** Every run is Montserrat, at 400, 600, 700 or 800. No italic. No fallback face in the file.
5. **Sizes.** Every size is a step in section 9. Nothing in a document is under 9pt. Nothing on a slide is under 12pt, except the POWERED BY label at 9pt. Slide body text is 15pt.
6. **Budgets.** Every slot is inside its character, line and item limit. No text box has auto-fit or shrink-on-overflow switched on.
7. **Band.** On page 1 only. Fill #2f193b. No rule. Title on one line.
8. **Logo.** Role `horizontal-on-dark` in the band, 1.6in wide, once.
9. **Tables.** Header fill #2f193b, text #FFFFFF. Hairline under every row. No frame, no vertical rules, no zebra. Numbers right-aligned.
10. **Color.** Status colors are the four alert colors and nothing else. Chart colors are the house data set. No brand color stands for a status.
11. **Slides.** Content slides are white. Only title, divider and closing are #2f193b.
12. **Lockup.** Powered by Collective Edge appears exactly once, 2.125in wide, in the place section 3.12 names.
13. **Footer.** On every page. Signature left, Page X of Y right, 9pt, the last line on the bottom margin.
14. **Copy.** No em dash. Curly quotation marks. Headings in sentence case.

---

## 13. Other patterns

| Need | Where |
|---|---|
| Chart colors and chart rules | [`reference/data-color.md`](data-color.md) |
| Diagram and flowchart node colors | `diagramRoles` in [`tokens.json`](../tokens.json) |
| Buttons, inputs and product UI | [`reference/ui.md`](ui.md) |
| The type scale and its rules | [`reference/type-system.md`](type-system.md) |
| Lockup CSS for sites and dashboards | [`snippets/cobrand.css`](../snippets/cobrand.css) |

**Retired at this version.** The sub-banner under the band. The uppercase label above a heading. The row of large stat numerals. Uppercase table headers. The rule under a section heading. Where one of these appears in an existing file, leave it while editing that file and do not carry it into new work.
