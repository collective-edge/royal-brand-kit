# Royal Ambulance · layout standard

How to build a working document, a sheet, a deck, a one-pager, a report or a memo for Royal Ambulance. The rules are the same in the Collective Edge, Apex Paramedics and Royal Ambulance kits. Only the values in section 2 differ.

This file is written so a page can be built from it without seeing one. [`documents.json`](../documents.json) holds the same values as data, and the two agree exactly. Type steps come from [`snippets/type-tokens.json`](../snippets/type-tokens.json). Colors come from [`tokens.json`](../tokens.json).

**Units.** Page geometry is in inches. Type and space are in points. On screen, 1pt is 4/3px, so 12pt is 16px and 1in is 96px. Slide positions are measured from the top left corner of the slide.

---

## 1. Choose a type

**Start here.**

1. Is there an existing file? Follow the editing rules. Do not restyle it.
2. Did they point at a document to imitate? Copy it.
3. Otherwise pick a type from the table below. The first row that fits wins.
4. Keep it short. Follow the wording budget.

### Editing rules

Most requests change a file that already exists. These eight rules come before every other rule in this file.

1. **Edit in place.** Asked to edit, update, fix or add to an existing file: keep its layout, styles, fonts, sizes, colors, column order and wording. Change only what was asked. Same file, same link. Do not convert its format, move it or make a copy unless asked.
2. **Match the neighbors.** New content inside an existing file takes the style of the nearest existing content of the same kind. A new row looks like the rows around it. A new slide uses the deck’s own layout.
3. **A named example is the template.** Asked to make it look like another document: copy that document’s structure, styles and order. This kit does not override it.
4. **Restyle only when asked.** “Brand this”, “clean up the formatting”, “make it consistent”. Then apply the working-doc styles to what is there: font, sizes, heading colors, table style, logo, footer. Do not reorder, rewrite or shorten the words. Do not add a band. Where the file has a band, take it out: the logo goes top left and the band’s words go only if they are not already the title.
5. **An accepted format is fixed.** A recurring report or an agenda a person approved is reused exactly next time. Never improve it unprompted.
6. **Leave the words alone.** Shorten or rewrite only when asked. Asked to tighten: cut at least half and keep every fact, name, number and date.
7. **Delete nothing that is not yours.** Never delete someone else’s content, comments, formulas, data validation or tabs. Before a large change, say what will change. After, list what changed in three bullets or fewer.
8. **Never resize to fit.** Never change the spacing, sizes or margins of an existing file to make an edit fit a page. If an edit pushes content onto a new page, leave it there and say so when you hand the work back.

### Types

| Type | Use it when | Section |
|---|---|---|
| sheet | Rows and columns people will sort, filter or fill in, in Google Sheets or Excel. Words: tracker, list, log, roster, budget, workbook, spreadsheet. | 14 |
| deck | Anything presented on a screen, in Google Slides or PowerPoint. One slide and a graphic for a slide count. Words: deck, slides, slide, presentation, pitch. | 8 |
| working-doc | The default. Anything in Google Docs or Word that people will keep editing. Words: agenda, meeting guide, prep packet, status report, plan, charter, brief, notes, job description, scorecard, policy draft, proposal draft. | 7 |
| one-pager | A designed single page for an outside reader, delivered as a PDF. Words: one-pager, fact sheet, flyer, leave-behind, case study, handout. | 5 |
| report | A designed document of three pages or more for an outside reader, delivered as a PDF. Words: report, proposal, review, analysis, white paper. | 6 |
| memo | Only when the request asks for a memo by name. | 4 |

- **Default.** A request that matches nothing is a working-doc. The earlier generic type is now working-doc.
- **The band.** The band is for PDF, print and slides. A document that will live in Google Docs is a working-doc unless the person asks for a designed one-pager.
- **Wording budget.** It applies to every type. The first line states the decision, the ask or the status. In an agenda it states what the meeting is for. No paragraph restates the title. No closing summary. No sentence about the document itself. A sentence runs 20 words at most. Items that share the same fields go in a table. Parallel items go in bullets.

### Page setup

| Type | Page | Orientation | Margins | Text block | Body measure | Columns | Pages |
|---|---|---|---|---|---|---|---|
| memo | US Letter, 8.5 x 11in | portrait | 0.75in on all four sides | 7.0in wide | 5.96in, 70 characters | 1 | 1, 2 at most |
| one-pager | US Letter, 8.5 x 11in | portrait | 0.6in on all four sides | 7.3in wide | 5.96in, 70 characters | 1 | exactly 1 |
| report | US Letter, 8.5 x 11in | portrait | 0.75in on all four sides | 7.0in wide | 5.96in, 70 characters | 1 | 3 or more |
| working-doc | US Letter, 8.5 x 11in | portrait | 0.75in on all four sides | 7.0in wide | 7.0in, the text block | 1 | 1 for an agenda or a status report. Otherwise as short as the content allows |
| deck | 16:9, 13.333 x 7.5in | landscape | 0.67in top, 0.83in left and right, 0.42in bottom | 11.67in wide | 7.45in, 70 characters | 1 or 2 | any |

Body text never runs wider than the body measure, even where the text block is wider. A working-doc is the exception: its body runs the full text block. A sheet has no page: section 14. Tables, callouts, the meta row and the footer span the full text block.

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
| Working-doc logo | Role `horizontal-on-light`, 1.3in wide. Section 7 |
| Working-doc and sheet table header | Fill `--bg-surface-2` #f0e1fd. Text `--fg-1` #23232A |
| Working-doc footer line | `Royal Ambulance · Page N` |
| Powered by Collective Edge lockup | Once on every PDF, deck and image, small. Never on a working-doc or a sheet. Section 3.12 |

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
- The band is for PDF, print and slides: the memo, the one-pager and the report. A working-doc has no band and carries its logo top left of page 1. Section 7.
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
| Section heading, report only | h2, 24pt | weight 700, `--fg-1` #23232A | 36pt | 12pt | 1 line, 40 characters |
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

**Status cells.** A square, then the word at weight 600, both in the alert text color: good `--alert-go-text` #1E7A4D, caution `--alert-warn-text` #926603, bad `--alert-stop-text` #B0322B, notice `--alert-info-text` #2A5A8C. The word carries the meaning. Green means good only. A brand color is never a status color. A status that is neither good, caution nor bad takes the notice color #2A5A8C. The mark is stated once, here. In HTML and PDF it is a drawn square, 6pt in a document and 9pt on a slide. In Word, PowerPoint and Google files it is the character U+25A0, which Montserrat contains, set at 9pt in a document and 12pt on a slide, followed by one no-break space, in the same color as the word. In a working-doc the mark and the word share one run at 10.5pt, weight 700.

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
| Left | The signature: the brand name, a middle dot, then the classification or the document title: Royal Ambulance · Internal. Use Internal only when every reader is staff. Otherwise the document title, 40 characters at most |
| Right | Page X of Y |
| Text | caption, 9pt, `--fg-3` #6D6D77. One line |
| Space above | At least 12pt between the last body block and the rule |

Nothing sits under the footer. Nothing but the band crosses a margin. A working-doc footer is one left-aligned line with no rule. Section 7.

### 3.12 Powered by Collective Edge

Every Royal Ambulance PDF, deck and image carries “Powered by Collective Edge” exactly once, small and quiet. A working-doc and a sheet never carry it.

| | |
|---|---|
| Carries it | Everything delivered as a PDF, a deck or an image: memo, one-pager, report, proposal, deck, and a chart or data graphic made on its own |
| Never carries it | A working-doc and a sheet, as a lockup or as words. The rule follows the type, not the file format: a working-doc exported to PDF stays as it is. A Collective Edge document. A clinical instruction. A patient-facing consent or safety document |
| Lockup | One line. The words, then the logo to their right, 6pt apart, centered on the line. No rule of its own |
| Words | `Powered by`. caption, 9pt, weight 400, `--fg-3` #6D6D77. On the closing slide: body, 12pt, `--fg-on-dark-3` #A3A4AC |
| Logo | The Collective Edge `horizontal-on-light` logo on white, `horizontal-on-dark` on a dark slide, at its minimum width: 1.25in (120px) wide, 0.208in (20px) tall. Never larger in a document. Never smaller anywhere |
| Memo and one-pager | In the footer row of page 1, at left. The signature and the page number move to the right, joined by a middle dot, on the same line. A second page carries the plain footer |
| Report | The last line of the body on the last page, at left. A 0.75pt `--border-1` #E4E4E9 rule above it, with 18pt above the rule and 9pt under it. It never sits alone on a page |
| Deck | The closing slide, in the footer row, at left. Section 8 |
| Chart or data graphic made on its own | No logo. One line of words, `Powered by Collective Edge`, bottom right: caption, 9pt, weight 400, `--fg-3` #6D6D77. On a 1920 x 1080 graphic for a slide the line is 24px |

- Once. Never twice in one document.
- Never inside or touching the Royal Ambulance logo.
- Never set as type where the logo fits. A chart or data graphic made on its own is the one place the words stand alone.
- The 204px lockup in `cobrand.lockup` in [`brands.json`](../brands.json) is for sites and dashboards. A document, a deck and an image never use that size.
- The files are in `cobrand.lockup` in [`brands.json`](../brands.json). On white: `https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/for-humans/logos/png/Collective-Edge-horizontal-black-1200w.png`. On a dark slide: `https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/for-humans/logos/png/Collective-Edge-horizontal-white-1200w.png`.

---

## 4. Memo

A message from a named sender to named readers. The band title is the word Memo. Use it only when the request asks for a memo by name.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.75in on all four sides |
| Text block | 7.0in wide, one column |
| Body measure | 5.96in, 70 characters |
| Pages | 1. 2 at most |
| Parts, top to bottom | band, to-block, body, table, subhead, actions, sign-off, footer |
| Lockup | Footer row of page 1, left. Signature and page number at right, on the same line |
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
| lockup-label | The words Powered by, before the logo, on one line | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | none | caption 9pt |

- No headline. The Re row is the subject.
- Band, To block, body, sign-off and footer are required. Table, subhead and actions are optional. A closing line is the last body paragraph.
- One table at most, 4 body rows and 4 columns, under the last paragraph, built to section 3.7. A one-page memo with a table holds 1 paragraph of 130 characters, the table and 3 actions. Without a table it holds 4 paragraphs of 520 characters in all and 3 actions. Actions never count as paragraphs. A memo that needs more is a report.
- Past one page, the memo runs to a second page with the same margins and footer and no band. Past two pages it is a report.

## 5. One-pager

One finding on exactly one page. The headline states it. A designed document for an outside reader, delivered as a PDF.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.6in on all four sides |
| Text block | 7.3in wide, one column |
| Body measure | 5.96in, 70 characters |
| Pages | Exactly 1 |
| Parts, top to bottom | band, title-block, meta-row, subhead, body, table, callout, footer |
| Lockup | Footer row of page 1, left. Signature and page number at right, on the same line |
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
| lockup-label | The words Powered by, before the logo, on one line | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | none | caption 9pt |

- Exactly one page. Never a second.
- One table or one chart, never both.
- One callout at most.
- The page holds two subheads. The first sits over one paragraph. The second sits over the table.
- A chart takes the place of the table and its height: 2.2in at most.

## 6. Report

A designed document of three pages or more, in sections, for an outside reader, delivered as a PDF. Page 1 opens with the band, the title block and the meta row. The first section follows on the same page.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.75in on all four sides |
| Text block | 7.0in wide, one column |
| Body measure | 5.96in, 70 characters |
| Pages | 3 or more |
| Parts, top to bottom | band, title-block, meta-row, section-heading, subhead, body, table, callout, actions, lockup, footer |
| Lockup | Last line of the body on the last page, left, under a 0.75pt --border-1 rule with 18pt above the rule and 9pt under it |
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
| lockup-label | The words Powered by, before the logo, on one line | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | none | caption 9pt |

- The band is on page 1 only.
- Every page carries the footer.
- A heading never sits on the last line of a page.
- A table stays whole on one page, with its caption.

## 7. Working document

The default type, `working-doc`. Anything people will keep editing in Google Docs or Word: agenda, meeting guide, prep packet, status report, plan, charter, brief, notes, job description, scorecard, policy draft, proposal draft. It is plain on purpose, so it survives conversion to Google Docs untouched. It replaces the generic branded document. `types.generic` in `documents.json` repeats `types.working-doc`.

| | |
|---|---|
| Page | US Letter, 8.5 x 11in, portrait |
| Margins | 0.75in on all four sides |
| Text block | 7.0in wide, one column. Body text runs the full width |
| Pages | An agenda and a status report fit 1 page. Anything else is as short as the content allows. Budget to 90 percent of a page in a Google file |
| Parts, top to bottom | logo, title, meta-line, heading-1, heading-2, body, bullets, table, footer |
| Weights | 400 and 700 only. Bold off and bold on. `Montserrat SemiBold` is not needed |
| Never | Band, callout box, card, shadow, tinted panel, icon, emoji, uppercase label, sub-banner, stat numeral, justified text, text box, floating image, section break, columns |
| Logo | Role `horizontal-on-light`, PNG, 1.3in wide. Once, top left of page 1, inline, as its own paragraph, 12pt after |
| Footer | The document footer, on every page. One left-aligned line: `Royal Ambulance · Page N`, where N is the page number field. No rule, no logo, no table |
| Lockup | None. A working-doc never carries “Powered by Collective Edge”, as words or as a lockup. The rule follows the type, not the file format: a working-doc exported to PDF stays as it is |
| Template | [`templates/working-doc.html`](../templates/working-doc.html) |

| Slot | Named style | What it holds | Step | Print | Screen | Weight | Color | Line spacing | Space before, after | Limit |
|---|---|---|---|---|---|---|---|---|---|---|
| title | Title | Names the document. Sentence case, no period | h2 | 24pt | 32px | 700 | `--fg-1` #23232A | 1.15 | 0, 3pt | 60 characters |
| meta-line | Normal | Directly under the title. Owner or team · date as 13 November 2026 · audience or status if needed. A 0.75pt `--border-1` #E4E4E9 bottom border on the paragraph, 6pt under the text | body-sm | 10.5pt | 14px | 400 | `--fg-3` #6D6D77 | 1.35 | 0, 12pt | 1 line |
| heading-1 | Heading 1 | A plain label. Sentence case, no colon, no period | h4 | 15pt | 20px | 700 | `--fg-1` #23232A | 1.15 | 18pt, 6pt | 6 words |
| heading-2 | Heading 2 | A plain label. Sentence case, no colon, no period | body | 12pt | 16px | 700 | `--fg-accent` #572e72 | 1.15 | 12pt, 3pt | 6 words |
| body | Normal | Running text. Flush left, never justified | body-sm | 10.5pt | 14px | 400 | `--fg-1` #23232A | 1.35 | 0, 6pt | 20 words a sentence |
| bullet | List Bullet, List Number | The standard bullet list of the application. Hanging indent 0.25in | body-sm | 10.5pt | 14px | 400 | `--fg-1` #23232A | 1.35 | 0, 3pt | 1 line each, 2 at most. 6 in a group. 1 nesting level |
| table-header | Normal | Header row. Fill `--bg-surface-2` #f0e1fd. A 0.75pt `--fg-1` #23232A bottom border | body-sm | 10.5pt | 14px | 700 | `--fg-1` #23232A | 1.35 | 0, 0 | none |
| table-text | Normal | Body cells. A 0.75pt `--border-1` #E4E4E9 bottom border. Numbers right-aligned | body-sm | 10.5pt | 14px | 400 | `--fg-1` #23232A | 1.35 | 0, 0 | none |
| status | Normal | U+25A0, a no-break space, then the word, in one run | body-sm | 10.5pt | 14px | 700 | The alert text color | 1.35 | 0, 0 | 2 words |
| footer | Normal | The footer line | caption | 9pt | 12px | 400 | `--fg-3` #6D6D77 | 1.35 | 0, 0 | 1 line |

- **Headings.** Two levels at most. No label, number or rule above or under a heading.
- **Lists.** A numbered list only for steps in order or agenda items.
- **Table.** The full text width, the left edge of the table on the left margin. In a Word or Google file that takes a table indent equal to the left cell padding, 6pt, and column widths that sum to the text block less 6pt. Cell padding 4pt top and bottom, 6pt left and right. No vertical rules, no zebra, no frame, no dark header fill. The dark header of section 3.7 is for the one-pager, the report and the deck. One empty paragraph between two adjacent tables.
- **Status.** The alert text colors of section 3.7: good #1E7A4D, caution #926603, bad #B0322B, notice #2A5A8C.
- **Agenda.** A 3-column table: Time or minutes, Topic, Owner. Or a numbered list with the owner and the minutes at the end of each line. Never both.
- **Status report.** One line of overall status. Then a table: Item, Owner, Due, Status. Then bullets under the heading Needs a decision, if any.
- **Line spacing.** A multiple, as Word and Google Docs state it: 1.15 for headings, 1.35 for body. Never an exact point value. In CSS the same lines are a line-height of 1.4 and 1.65, since the natural line of Montserrat is 1.219.
- **Restyling an existing file.** Only when asked. Apply these styles to what is there. Do not reorder, rewrite or shorten the words. Do not add a band. Where the file has a band, take it out: the logo goes top left and the band’s words go only if they are not already the title.
- **Build.** Section 11, Google Docs.

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
- Body text is 15pt. Nothing on a slide is under 12pt.
- Content slides are white. Only title, divider and closing are dark.
- Dark slides are flat `--bg-inverse` #2f193b. No picture background.
- Uppercase is for the title slide title only. Four words at most.
- A headline that takes one line still reserves two. The body zone starts at y 2.53in on every white slide.
- One chart or one table per slide.
- A chart of one quantity is one series, in series color 1. Two series only when comparing two things.
- No stat card and no big-number panel.
- No logo on a dark slide except title and closing.

### Editing a deck

The common case, often one slide. Use that deck’s own layouts, fonts, colors and positions, even where they are not this kit’s. Combine, split or reword slides without restyling the rest. Deliver the change inside the same deck. “Combine these two slides” means one slide that carries the content of both in the layout of the first, then delete the second. If the two say the same thing, say so and ask before deleting one.

### A graphic for a slide

A 1920 x 1080 PNG on a white ground. The same type rules as a slide, no band. Text is 48px or larger, which is 24pt on the slide. An Apex Paramedics or Royal Ambulance graphic or chart made on its own carries one line of words, bottom right: `Powered by Collective Edge`, 24px, weight 400, `--fg-3` #6D6D77. No logo. A Collective Edge graphic carries none.

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
| chart |  | 1 chart, 4 series | 0.83in, 2.53in | 7.5in, 3.78in | One chart. Colors from reference/data-color.md. Caption above, source line under, both in the caption slot. One quantity is one series, in series color 1. Two series only when comparing two things. A bar chart holds four categories |
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
| lockup |  |  | 0.83in, 6.73in | 2.42in, 0.35in | A 0.75pt `--border-on-dark` #483553 rule at y 6.55in, 11.67in wide. On the footer row: the words Powered by in `--fg-on-dark-3` #A3A4AC, 12pt, weight 400, in a box at x 0.83in, 1.1in wide, anchored middle. Then the Collective Edge `horizontal-on-dark` logo at x 2.0in, y 6.80in, 1.25in wide, 0.208in tall. The date at right, 12pt, #A3A4AC, in a box at 7.0in, 6.73in, 5.5in by 0.35in, right-aligned. The lockup takes the place of the brand name. The only place in the deck the lockup appears |

---

## 9. Type by role

One face, Montserrat. Four weights: 400, 600, 700, 800. No italic. Sizes come from the house scale in [`snippets/type-tokens.json`](../snippets/type-tokens.json). Leading is given in points so it can be set exactly. In a file that will become a Google file, set line spacing as a multiple instead: section 11.

| Step | Print | Screen | Leading | Used for in a document | Used for on a slide |
|---|---|---|---|---|---|
| display-lg | 54pt | 72px | 58.3pt |  | Title slide title |
| display-md | 42pt | 56px | 46.2pt |  | Headline, statement, quote, divider title, closing line |
| h1 | 30pt | 40px | 35.4pt | Headline | Floor for display-md |
| h2 | 24pt | 32px | 30pt | Band title, section heading, working-doc title |  |
| h3 | 18pt | 24px | 24.3pt | Subhead | Key points, subtitle, column labels |
| h4 | 15pt | 20px | 21.8pt | Working-doc heading 1 | Floor for h3 |
| body-lg | 15pt | 20px | 23.3pt | Lead | Body, bullets, tables |
| body | 12pt | 16px | 19.2pt | Body, To block, actions, callout, working-doc heading 2 | Caption, source line, footer, page number. The floor |
| body-sm | 10.5pt | 14px | 16.3pt | Table text, meta value, sign-off contact, working-doc body and tables | Not used |
| caption | 9pt | 12px | 13.1pt | Caption, meta label, footer, the words Powered by | Not used |
| eyebrow | 9pt | 12px | 13.1pt | Not used | Not used |

- **Weights.** 400 for running text. 600 for subheads, table headers, labels and key points. 700 for headlines, section headings and emphasis. 800 for a slide headline on white only. Three weights at most in a document. A deck is the one piece that uses all four. A working-doc uses 400 and 700.
- **On a dark ground.** A step at 700 or 800 drops one weight: the band title is 600, a dark slide title is 700. Every step gains 0.005em of tracking. In Word and PowerPoint, skip that gain under 24pt.
- **Tracking.** Band title 0.045em. Title slide title 0.025em. Document headline -0.012em. Slide headline -0.015em. Subhead -0.004em. No other slot is tracked. Section 11 gives each in points.
- **Color.** Text is `--fg-1` #23232A. `--fg-accent` #572e72 is for subheads, slide headlines, action numbers and bullets. `--fg-3` #6D6D77 is the lightest text color.
- **Uppercase.** The band title and the title slide title. Nowhere else. Always tracked, never past four words.
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
- A working-doc never tightens. It shortens.

---

## 11. Tools

The same page in each tool. A value not listed here comes from the section named.

### Word, with python-docx

| Rule | How |
|---|---|
| Page and margins | `section.page_width = Inches(8.5)`, `section.page_height = Inches(11)`. All four margins `Inches(0.75)`, or `Inches(0.6)` for a one-pager |
| Body | Style `Normal`: Montserrat, 12pt, color #23232A, line spacing exactly 19.2pt, space after 0, no indent, left-aligned. Body paragraphs add space after 12pt and right indent 1.04in, or 1.34in on a one-pager, so a line is 5.96in wide. Every paragraph in a table cell, the band, the To block, the meta row, the callout and the footer sets right indent 0, space before 0, space after 0, and line spacing exactly at its own step from section 9. Exact line spacing is for a file that stays in Word or becomes a PDF. A file that becomes a Google Doc takes multiples: see Google Docs below |
| Fonts in XML | On every style and run, replace `w:rFonts` with one element carrying `w:ascii`, `w:hAnsi`, `w:cs` and `w:eastAsia`, all set to the font name. Remove every `w:asciiTheme`, `w:hAnsiTheme`, `w:cstheme` and `w:eastAsiaTheme`. Remove `w:pBdr` from `Title`. Set the color on every style |
| Tracking | Tracking in points is em times the size. `w:spacing w:val` on the run, in twentieths of a point. Band title 1.08pt, `w:val="22"`. Headline -0.36pt, `w:val="-7"`. Subhead -0.07pt, `w:val="-1"`. Set no other tracking. Type the capitals of the band title. Do not use the all-caps attribute |
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
| Lockup | Memo and one-pager: a 1-row, 2-column table in the first-page footer, in place of the footer paragraph, the width of the text block, table indent 0, columns 2.6in and the rest. Top border 0.75pt #E4E4E9 on both cells, top cell margin 9pt, other margins 0. Left cell: one 9pt paragraph in #6D6D77, the run `Powered by`, two no-break spaces, then the logo inline, `add_picture(path, width=Inches(1.25))`. Right cell: vertical alignment center, one right-aligned 9pt paragraph: brand, middle dot, Page X of Y. Set the paragraph Word leaves after the table to line spacing exactly 1pt. The footer of later pages is the plain footer paragraph. Report: the last body paragraph, kept with the block before, with a 0.75pt #E4E4E9 top border 9pt above the text and space before 18pt: the run `Powered by`, two no-break spaces, then the inline logo at `Inches(1.25)` |
| Logo | `add_picture(path, width=Inches(1.6))`. PNG from `for-humans/logos/png/`, by role, from `logosPng` in `brands.json`, since Word does not place SVG through python-docx |

### PowerPoint, with python-pptx

| Rule | How |
|---|---|
| Slide size | `prs.slide_width = Emu(12192000)`, `prs.slide_height = Emu(6858000)` |
| Layout | Start every slide from the blank layout. Place each slot as a text box at the x, y, width and height in section 8 |
| Text boxes | `word_wrap = True`, `auto_size = MSO_AUTO_SIZE.NONE`, all four insets 0. Set font name, size and color on every run, bullets included. Set `a:latin`, `a:ea` and `a:cs` on every run |
| Tracking | Tracking in points is em times the size. `spc` on `a:rPr`, in hundredths of a point. Title slide title 1.35pt, `spc="135"`. Slide headline -0.63pt, `spc="-63"`. Set no other tracking. Type the capitals of the title slide title. Do not use the all-caps attribute |
| Ground | White slides: background #FFFFFF. Dark slides: background #2f193b |
| Headline | Text box at 0.83in, 0.67in, 10.0in by 1.28in. `Montserrat ExtraBold`, 42pt, #572e72, line spacing 46.2pt, anchored top |
| Body | `Montserrat`, 15pt, #23232A, line spacing 23.3pt |
| Bullets | `a:buChar` U+2022, `a:buClr` #572e72, `marL` 0.33in, `indent` -0.33in, space before 9pt |
| Rules | A line shape, 0.75pt, #E4E4E9 on white or #483553 on dark |
| Table | `shapes.add_table` in the body zone. Set `a:tableStyleId` to `{2D5ABB26-0587-4C30-8999-92F81FD0307C}` and `firstRow` and `bandRow` to 0. On every cell write `a:lnL`, `a:lnR`, `a:lnT` and `a:lnB` in `a:tcPr`: `a:noFill` for no border, or `w` in EMU with a solid fill. 0.75pt is 9525. 1.5pt is 19050. Header cells: fill #2f193b, text #FFFFFF, no border. Body cells no fill, bottom border 0.75pt #E4E4E9, no other border. Header row height 0.49in, body rows 0.57in. Columns in proportion to content, summing to 11.67in |
| Chart | In the chart box of the chart layout. Series colors from `reference/data-color.md`, in order. One quantity is one series, in series color 1. `chart.value_axis.visible = False`. `plot.has_data_labels = True`, `plot.data_labels.number_format = '#,##0'`, `plot.data_labels.number_format_is_linked = False` |
| Footer | Logo picture at x 0.83in, 1.43in wide, centered on the 0.35in row at y 6.73in. Page number text box at 10.5in, 6.73in, 2.0in by 0.35in, right-aligned, anchored middle. Static text, the bare slide number |

### Google Docs

Build the `.docx` with python-docx, then upload with conversion. Conversion was tested on a live file. Each row is what it does and the rule that follows.

| What conversion does | Rule |
|---|---|
| Exact line spacing in points lands about three times too far apart. Google Docs has proportional line spacing only | Line spacing is a multiple. `paragraph_format.line_spacing = 1.35`, a float, with `line_spacing_rule = WD_LINE_SPACING.MULTIPLE`. Never `EXACTLY`, never a point value |
| A full-bleed band is impossible. A header table with a negative indent loses its cell padding | A band is a table at text-block width with indent 0, and only on a designed document the person asked for. A working-doc has no band |
| Right tab stops are lost | A left and right footer is a two-cell borderless table. A working-doc footer is one left-aligned line |
| Two tables with nothing between them merge, and the second loses its column widths | One empty paragraph between adjacent tables |
| A table pokes about 9pt into the left margin | Table indent equal to the left cell padding, set explicitly: `w:tblInd` with `w:w="120"` and `w:type="dxa"` in `w:tblPr` |
| Line heights run taller than in Word, so a page that fits in Word can spill onto a second | Budget to 90 percent of a page |
| `Montserrat SemiBold` and `Montserrat ExtraBold` survive as real faces | Name the family, bold off. A working-doc needs neither |
| Text boxes, floating images, section breaks and columns do not convert cleanly | Use none. Place the logo inline |

**Working-doc.** Section 7 holds the values.

| Rule | How |
|---|---|
| Page | Letter, portrait, all four margins `Inches(0.75)`. One section |
| Styles | Set `Title`, `Heading 1`, `Heading 2` and `Normal` to the section 7 values and use them. Set the color on every style. Remove `w:pBdr` from `Title`. `Heading 1` and `Heading 2` keep with next |
| Fonts | `Montserrat` on every style and every run, in `w:ascii`, `w:hAnsi`, `w:eastAsia` and `w:cs`. Remove every theme font attribute. Weight 700 is bold on. Do not name `Montserrat SemiBold` |
| Line spacing | `Title`, `Heading 1`, `Heading 2`: 1.15. `Normal` and the list styles: 1.35. Always a float with the rule `MULTIPLE` |
| Logo | The first paragraph. `run.add_picture(path, width=Inches(1.3))`, inline, space after 12pt |
| Meta line | A `Normal` paragraph, 10.5pt, #6D6D77, space after 12pt, with `w:pBdr` holding `w:bottom w:val="single" w:sz="6" w:space="6" w:color="E4E4E9"` |
| Bullets | Styles `List Bullet` and `List Number`: left indent 0.25in, first line indent -0.25in, space after 3pt |
| Table | `doc.add_table` with no table style, autofit off, column widths that sum to 6.92in. `w:tblInd w:w="120"`, so the left edge of the table sits on the left margin and the cell padding sits inside it. Cell margins 80 twentieths of a point top and bottom, 120 left and right. Header cells: shading F0E1FD, bold, bottom border `w:sz="6"` in 23232A. Body cells: bottom border `w:sz="6"` in E4E4E9, no other border. Cell paragraphs: space after 0. Number cells right-aligned |
| Status cell | One bold run in the alert text color: U+25A0, U+00A0, then the word |
| Between tables | One empty `Normal` paragraph |
| Footer | `section.footer.paragraphs[0]`, left-aligned, 9pt, #6D6D77: the text, then a `PAGE` field. No table, no tab stop, no border. Same footer on every page |

**A designed document in Google Docs.** Only when the person asks for a designed one-pager, report or memo as a Google Doc. Follow the Word rows above with these changes.

| Named style | Role | Line spacing |
|---|---|---|
| Title | Headline, 30pt, bold | 1.0 |
| Subtitle | Lead, 15pt | 1.27 |
| Heading 1 | Section heading, 24pt, bold | 1.0 |
| Heading 2 | Subhead, 18pt, Montserrat SemiBold, #572e72 | 1.1 |
| Normal text | Body, 12pt, 12pt after a paragraph | 1.31 |
| Table text, 10.5pt | Cells | 1.27 |
| Caption and footer, 9pt | Caption, footer | 1.2 |

Each multiple is the leading in section 9 divided by the size and by 1.219, the natural line of Montserrat. The band is a two-cell table at the top of page 1, at text-block width, indent 0, cell fill #2f193b, no borders. It cannot reach the page edge. The footer is a two-cell borderless table, never a tab stop.

### Google Slides

Build the `.pptx` with python-pptx as above, then upload with conversion. Page size 13.333 x 7.5in. The twelve layout names of section 8, each box at its x, y, width and height. Autofit off on every box.

| What conversion does | Rule |
|---|---|
| Inherited bullet sizes shrink | Set the size on every run. Never rely on a placeholder or a list level for a size |
| A chart gains a visible value axis | Delete it: `chart.value_axis.visible = False` |
| Data labels lose their thousands separators | `plot.has_data_labels = True`, `plot.data_labels.number_format = '#,##0'`, `plot.data_labels.number_format_is_linked = False` |
| A second series adds a legend and a second color to decode | One quantity is one series, in series color 1. Two series only when comparing two things |
| `Montserrat SemiBold` and `Montserrat ExtraBold` survive as real faces | Name the family, bold off |

Editing an existing Google Slides deck: use its own layouts, fonts, colors and positions. Section 8.

### Google Sheets and Excel

Section 14 holds the values. With openpyxl, then upload with conversion, or the same properties set in the sheet.

| Rule | How |
|---|---|
| Font | `Font(name='Montserrat', size=10)` on every cell. Header, status and totals: `bold=True`. Never `Montserrat SemiBold`, never size 10.5 |
| Header row | Row 1. `PatternFill('solid', fgColor='F0E1FD')`, `Border(bottom=Side(style='thin', color='23232A'))` |
| Freeze and filter | `ws.freeze_panes = 'A2'`, or `'B2'` when column A is the name or ID of the row. `ws.auto_filter.ref = ws.dimensions` |
| Columns | `ws.column_dimensions[letter].width` in characters: short code 11, date 15, name 25, notes 45, which is 80px, 110px, 180px and 320px. Text cells `Alignment(wrap_text=True, vertical='top')`. Number cells `Alignment(horizontal='right')` |
| Formats | `cell.number_format`: `'d mmm yyyy'`, `'#,##0'`, `'$#,##0'`, `'0%'` |
| Status | `DataValidation(type='list', formula1='"■ Not started,■ On track,■ At risk,■ Blocked,■ Done"')` on the column. One conditional format per value sets the fill to the alert tint and the font to the alert text on tint, bold |
| Due dates | One conditional format on the date column: the date is before `TODAY()` and the status of the row is not `■ Done`. Font color B0322B |
| Logo and tabs | No picture, no `=IMAGE()`, no tab that was not asked for |
| Totals row | The last row. Bold, `Border(top=Side(style='thin', color='23232A'))`. Every value a formula such as `=SUM(D2:D40)` |
| Editing | Load the file, change only the cells asked for, save to the same file. Never rebuild the sheet from its values |

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
| Lockup | `.ce-powered .ce-powered-light`, plus `.doc-lockup` in a report. `.ce-powered` alone on the closing slide. Each template sets the small document lockup over `cobrand.css` |
| Working-doc | `.wdoc-logo`, `.wdoc-title`, `.wdoc-meta`, `.wdoc-h1`, `.wdoc-h2`, `.wdoc-p`, `.wdoc-list`, `.wdoc-li`, `.wdoc-table`, `.doc-status`, `.wdoc-footer`, `.wdoc-foot` |
| Slide | `.slide`, plus `.slide-dark .bk-on-dark` on a dark slide |
| Slide layouts | `.slide-title`, `.slide-divider`, `.slide-statement`, `.slide-text`, `.slide-two-column`, `.slide-chart-slide`, `.slide-table-slide`, `.slide-comparison`, `.slide-timeline`, `.slide-quote`, `.slide-summary`, `.slide-closing` |
| Slide parts | `.slide-headline`, `.slide-body`, `.slide-cols`, `.slide-points`, `.slide-bullets`, `.slide-table`, `.slide-chart`, `.slide-steps`, `.slide-foot` |

| Template | Type |
|---|---|
| [`templates/working-doc.html`](../templates/working-doc.html) | working-doc |
| [`templates/memo.html`](../templates/memo.html) | memo |
| [`templates/one-pager.html`](../templates/one-pager.html) | one-pager |
| [`templates/document.html`](../templates/document.html) | report |
| [`templates/deck.html`](../templates/deck.html) | deck, all twelve layouts |
| [`snippets/header-band.html`](../snippets/header-band.html) | the band alone |
| [`Examples/royal-one-pager.html`](../Examples/royal-one-pager.html) | A filled one-pager. A reference, not a starting point |
| [`Examples/HPSM_Ordering_Workflow_Manager.html`](../Examples/HPSM_Ordering_Workflow_Manager.html) | A partner document that predates this standard. No lockup, its own layout. Not a model |

---

## 12. Check before delivery

Each line can be measured. A document that fails one is not finished.

Lines 7, 8, 9, 12 and 13 describe a memo, a one-pager and a report. For a working-doc or a sheet, check its own section instead, 7 or 14, and these seven things: no band, the logo once at top left, a light table header, the one-line footer, no Powered by Collective Edge, no exact line spacing, and no two tables without a paragraph between them. For an edited file, check that nothing changed but what was asked.

1. **Page count.** A one-pager is exactly 1 page. A memo is 1 page, 2 at most. An agenda and a status report are 1 page. A deck has one message per slide.
2. **Page size and margins.** Letter, portrait, 0.75in margins, or 0.6in on a one-pager. Slides are 13.333 x 7.5in.
3. **Nothing past the margins.** Only the band crosses a margin. No text box, table or picture ends outside the text block or the slide padding.
4. **Fonts.** Every run is Montserrat, at 400, 600, 700 or 800. No italic. No fallback face in the file.
5. **Sizes.** Every size is a step in section 9. Nothing in a document is under 9pt. Nothing on a slide is under 12pt. Slide body text is 15pt.
6. **Budgets.** Every slot is inside its character, line and item limit. No text box has auto-fit or shrink-on-overflow switched on.
7. **Band.** On page 1 only. Fill #2f193b. No rule. Title on one line.
8. **Logo.** Role `horizontal-on-dark` in the band, 1.6in wide, once.
9. **Tables.** Header fill #2f193b, text #FFFFFF. Hairline under every row. No frame, no vertical rules, no zebra. Numbers right-aligned.
10. **Color.** Status colors are the four alert colors and nothing else. Chart colors are the house data set. No brand color stands for a status.
11. **Slides.** Content slides are white. Only title, divider and closing are #2f193b.
12. **Lockup.** On a PDF, a deck or an image, Powered by Collective Edge appears exactly once, the logo 1.25in wide, in the place section 3.12 names. A working-doc and a sheet carry none.
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

**Retired at this version.** The sub-banner under the band. The uppercase label above a heading. The row of large stat numerals. Uppercase table headers. The rule under a section heading. Where one of these appears in an existing file, leave it while editing that file and do not carry it into new work. Also retired: the generic branded document, which is now the working-doc. The band on a document that lives in Google Docs. Exact line spacing in a file that becomes a Google file. The stacked POWERED BY lockup at 2.125in in a document: the document lockup is one line at 1.25in. Powered by Collective Edge on a working-doc or a sheet.

---

## 14. Sheet

A tracker, list or workbook in Google Sheets or Excel. Type `sheet`. A sheet carries no logo and no lockup.

| | |
|---|---|
| Layout | One table per tab, starting at A1. The header is row 1. No title row above it, no spacer row or column, no merged cells, no decorative color |
| Tabs | Only the tabs that were asked for. No cover tab, no “How to use” tab |
| Logo | None, and no lockup. A growing table has no stable place for one. Never use `=IMAGE()`: it returns `#REF!` |
| Font | Family `Montserrat`, 10pt, in every cell. Google Sheets sets whole point sizes only, so 10pt is the one size outside the scale of section 9. Never 10.5pt. Bold off or bold on, weights 400 and 700. Never name a weight family such as `Montserrat SemiBold` in a sheet: it falls back to Times New Roman |
| Alignment | Text left. Numbers right |
| Header row | Row 1. Weight 700, `--fg-1` #23232A, fill `--bg-surface-2` #f0e1fd, a 1pt `--fg-1` #23232A bottom border. Frozen, filter on |
| First column | Frozen when it is the name or ID of the row |
| Columns | Wrap text columns and set their widths: short code 80px, date 110px, name 180px, notes 320px. Clip nothing. Row height automatic |
| Dates | `d mmm yyyy` |
| Numbers | Whole numbers `#,##0`. Money `$#,##0`, two decimals only when cents matter. Percent `0%` |
| Status column | A dropdown: data validation from a fixed list. Each value is U+25A0, a space, then one or two words. No free text. Weight 700. Conditional formatting sets the color by value, never a hand fill |
| Due dates | Conditional formatting turns a date in the past `--alert-stop-text` #B0322B, unless the status of the row is Done |
| Notes | 120 characters at most. Longer context goes in a linked doc |
| Totals row | At the bottom. Weight 700, a 1pt `--fg-1` #23232A top border. Formulas, never typed values |
| Tab names | 20 characters at most, Title Case. No date unless the tab is a period |

**Status colors.** The cell fill is the alert tint. The text is the alert text on tint. From `alert` in [`tokens.json`](../tokens.json).

| Meaning | Fill | Text | Default word |
|---|---|---|---|
| Go | `--alert-go-tint` #DAF8DF | `--alert-go-on-tint` #1E7A4D | On track, Done |
| Warn | `--alert-warn-tint` #FFEFDD | `--alert-warn-on-tint` #926603 | At risk |
| Stop | `--alert-stop-tint` #FDE9E6 | `--alert-stop-on-tint` #B0322B | Blocked |
| Info | `--alert-info-tint` #E3F0FF | `--alert-info-on-tint` #2A5A8C | Not started |

Use the default words when the request names no statuses.

**Editing an existing sheet.**

- Never reorder or rename columns.
- Never overwrite a formula with a value.
- Keep validations, conditional formats, frozen panes and column widths.
- New columns go at the right. New rows go at the bottom or where the sort order puts them.
- Match the surrounding cell format.
- A sheet that already has its own colors and layout keeps them.

The build is in section 11, Google Sheets and Excel.
