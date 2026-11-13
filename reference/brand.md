# Royal Ambulance · brand reference

The full tables behind `SKILL.md`: color, logo, co-brand and voice. Type is in `reference/type-system.md`. Layout is in `reference/layout.md`. Chart color is in `reference/data-color.md`.

Royal Ambulance is a Bay Area medical transportation company and an operating company under Collective Edge. Its color is purple and its mark is the crown.

Collective Edge, Apex Paramedics and Royal Ambulance share one standard. The sections, the order and the rules in this file are the same in all three kits. Color, logo and brand facts differ.

`snippets/palette.css` is authoritative for color and `tokens.json` mirrors it. If this file disagrees with either, this file is stale.

---

## 1. Color

### 1.1 Palette

Purple is the whole palette. Three purples do three jobs: Dark Purple is the band, Purple is the primary and the accent, Royal Purple is the logo fill. Text and rules come from the shared neutrals in 1.3.

| Name | Token | Hex | RGB | Use |
|---|---|---|---|---|
| Dark Purple | `--royal-dark-purple` | `#2f193b` | 47, 25, 59 | The band, as `--bg-band` and `--bg-inverse`. Hero grounds, section dividers, table header rows |
| Purple | `--royal-purple` | `#572e72` | 87, 46, 114 | Primary. Accent bars, callout borders, buttons, links. Accent text, as `--fg-accent`. A filled block, as `--bg-mid` |
| Royal Purple | `--royal-royal-purple` | `#43205b` | 67, 32, 91 | The logo fill on light. The action node in a flowchart |
| Light Purple | `--royal-light-purple` | `#8260a2` | 130, 96, 162 | Tertiary accents and hover states. Never text. Never a large background |
| Surface | `--royal-surface` | `#faf5fd` | 250, 245, 253 | Callout fill, as `--bg-surface` |
| White | `--royal-white` | `#FFFFFF` | 255, 255, 255 | The page. Text on a dark purple ground |

Three more `--royal-*` names resolve to the shared neutrals in 1.3: `--royal-charcoal` `#23232A`, `--royal-muted` `#6D6D77` and `--royal-hairline` `#E4E4E9`. `--royal-black` is `#000000`.

### 1.2 Grounds

Every brand has the same six grounds, from lightest to darkest. White is the page. The last column lists the only text that sits on each ground.

| Ground | Token | Hex | RGB | Against white | Text on it |
|---|---|---|---|---|---|
| Canvas | `--bg-canvas` | `#FFFFFF` | 255, 255, 255 | | `--fg-1`, `--fg-2`, `--fg-3`, `--fg-accent` |
| Surface | `--bg-surface` | `#faf5fd` | 250, 245, 253 | 1.07:1 | `--fg-1`, `--fg-2`, `--fg-3`, `--fg-accent` |
| Surface 2 | `--bg-surface-2` | `#f0e1fd` | 240, 225, 253 | 1.24:1 | `--fg-1`, `--fg-2`, `--fg-accent`. Never `--fg-3` |
| Mid | `--bg-mid` | `#572e72` | 87, 46, 114 | | `--fg-on-dark-1`, `--fg-on-dark-2`. Never `--fg-on-dark-3` |
| Band | `--bg-band` | `#2f193b` | 47, 25, 59 | | `--fg-on-dark-1`, `--fg-on-dark-2`, `--fg-on-dark-3` |
| Hero | `--bg-inverse` | `#2f193b` | 47, 25, 59 | | `--fg-on-dark-1`, `--fg-on-dark-2`, `--fg-on-dark-3` |

Royal runs Hero and Band on one ground, `#2f193b`. Mid is Purple. Surface 2 `#f0e1fd` is step 100 of the purple ramp.

### 1.3 Neutrals

One neutral family sets text and rules in all three brands. It leans neither blue nor purple, so it sits beside every brand color. Ratios are on `#FFFFFF`.

| Name | Token | Hex | RGB | On white | Use |
|---|---|---|---|---|---|
| Ink | `--neutral-ink` | `#23232A` | 35, 35, 42 | 15.61:1 | Body text and headings on light |
| Secondary | `--neutral-secondary` | `#565860` | 86, 88, 96 | 7.09:1 | Secondary text |
| Tertiary | `--neutral-tertiary` | `#6D6D77` | 109, 109, 119 | 5.12:1 | Captions and metadata. The dimmest text |
| Dimmed | `--neutral-dimmed` | `#8A8B93` | 138, 139, 147 | 3.39:1 | Marks only. Never text |
| Border | `--neutral-border` | `#D0D0D6` | 208, 208, 214 | 1.54:1 | Borders and table rules. Never text |
| Hairline | `--neutral-hairline` | `#E4E4E9` | 228, 228, 233 | 1.27:1 | Hairlines and dividers. Never text |
| Tint 2 | `--neutral-tint-2` | `#E5E6EA` | 229, 230, 234 | 1.25:1 | Stronger neutral tint |
| Tint | `--neutral-tint` | `#F0F1F4` | 240, 241, 244 | 1.13:1 | Neutral surface tint |
| Mid | `--neutral-mid` | `#4E4F58` | 78, 79, 88 | 8.13:1 | Mid tone fill. Diagram process nodes and connectors |
| On-dark body | `--neutral-on-dark-body` | `#DDDDE3` | 221, 221, 227 | | Body text on a dark ground |
| On-dark caption | `--neutral-on-dark-caption` | `#A3A4AC` | 163, 164, 172 | | Captions on a dark ground |

### 1.4 Semantic layer

Style through these names. They are identical in every brand, so a component built for one brand renders correctly in another with only `palette.css` swapped. `tokens.json` carries the same names under `foreground`, `background` and `border`.

| Token | Hex | Use |
|---|---|---|
| `--fg-1` | `#23232A` | Primary text on light |
| `--fg-2` | `#565860` | Secondary text |
| `--fg-3` | `#6D6D77` | Tertiary text, metadata, captions. The dimmest text |
| `--fg-4` | `#8A8B93` | Dimmed marks. Never text |
| `--fg-accent` | `#572e72` | Brand-colored text. Purple. 10.30:1 on white |
| `--fg-on-dark-1` | `#FFFFFF` | Headings and primary text on a dark ground |
| `--fg-on-dark-2` | `#DDDDE3` | Body text on a dark ground |
| `--fg-on-dark-3` | `#A3A4AC` | Captions and labels on a dark ground |
| `--bg-canvas` | `#FFFFFF` | The page |
| `--bg-surface` | `#faf5fd` | Callouts |
| `--bg-surface-2` | `#f0e1fd` | The stronger tint |
| `--bg-elevated` | `#FFFFFF` | Raised surface |
| `--bg-mid` | `#572e72` | Filled block |
| `--bg-band` | `#2f193b` | Header band |
| `--bg-inverse` | `#2f193b` | Hero, title slide |
| `--border-1` | `#E4E4E9` | Hairlines and dividers |
| `--border-2` | `#D0D0D6` | Stronger rule |
| `--border-on-dark` | `rgba(255,255,255,0.12)` | Rules on a dark ground |
| `--border-band-rule` | `transparent` | Royal runs no rule under the band |

The focus ring on a control is `#23232A` on light and `#FFFFFF` on dark, 2px wide at a 2px offset.

### 1.5 Alerts

Four meanings, one family, identical in every brand, so a signal never changes meaning between documents. Green means good and nothing else. A brand color is never a status color. A word or an icon always travels with the color.

| Meaning | Base | Text | Tint | Text on tint | On dark |
|---|---|---|---|---|---|
| Go · cleared, on time, in service, favorable | `#1E7A4D` | `#1E7A4D` | `#DAF8DF` | `#1E7A4D` | `#56B580` |
| Warn · at risk, pending, watch, caution | `#B5821A` | `#926603` | `#FFEFDD` | `#926603` | `#E9B457` |
| Stop · failed, out of service, blocked, unfavorable | `#B0322B` | `#B0322B` | `#FDE9E6` | `#B0322B` | `#EB685C` |
| Info · neutral notice | `#2A5A8C` | `#2A5A8C` | `#E3F0FF` | `#2A5A8C` | `#5796D9` |

| Step | CSS name | `tokens.json` | Use |
|---|---|---|---|
| Base | `--alert-<name>` | `alert.<name>.base` | A fill, a rule or a dot on a light ground |
| Text | `--alert-<name>-text` | `alert.<name>.text` | Text on white and on Surface |
| Tint | `--alert-<name>-tint` | `alert.<name>.tint` | A pill or a callout fill |
| Text on tint | `--alert-<name>-on-tint` | `alert.<name>.onTint` | Text on the matching tint |
| On dark | `--alert-<name>-on-dark` | `alert.<name>.onDark` | Text, dots and rules on a dark ground |

Worst measured ratio across white, the three brand surfaces and the three brand bands:

| Step | Go | Warn | Stop | Info |
|---|---|---|---|---|
| Text on white and on Surface | 4.71:1 | 4.51:1 | 5.57:1 | 6.33:1 |
| Text on tint | 4.68:1 | 4.52:1 | 5.39:1 | 6.18:1 |
| On dark, on the bands | 5.76:1 | 7.72:1 | 4.62:1 | 4.69:1 |

**Canonical names and aliases.** `--alert-*` is canonical. It holds one value on every ground. Pick the step for the ground. Three sets are aliases of it and resolve to the same values:

| Alias | Resolves to | Note |
|---|---|---|
| `--status-go`, `--status-warn`, `--status-stop`, `--status-info` | The alert base | Under `.bk-on-dark` they move to the on-dark step |
| `--dir-favorable`, `--dir-unfavorable`, `--dir-caution` | Go text, stop text, warn text | The data layer. `--dir-neutral` is Tertiary `#6D6D77` |
| `--diagram-decision`, `--diagram-warning` | Go base, warn base | Section 1.6 |

**Status on a dark ground.** Status works on a band. Use the on-dark step: `#56B580`, `#E9B457`, `#EB685C`, `#5796D9`. The worst case is stop on the Apex band, 4.62:1.

**Warn.** The base `#B5821A` measures 3.40:1 on white. It is a fill, a rule or a dot, never text. Warn text is `#926603`, 5.09:1 on white. Text on an amber fill is `#23232A`, 4.59:1. White on amber measures 3.40:1 and fails.

**Surface 2.** On Surface 2, go text measures 4.28:1 and warn text 4.10:1. Neither sits bare on that ground. Carry them in a tint pill there. Stop and info hold.

### 1.6 Diagram roles

Identical in every brand, so a diagram reads the same in any document. Every node is a rectangle with a 6px radius. Fill carries the role, never shape. Each role names the one text color that clears contrast on its fill.

| Role | Fill | Border | Text | Contrast | Use |
|---|---|---|---|---|---|
| Decision | `#1E7A4D` | `#036139` | `#FFFFFF` | 5.32:1 | Decision boxes, questions, branch points |
| Warning | `#B5821A` | `#926603` | `#23232A` | 4.59:1 | Warnings, advisories. Ink, never white |
| Process | `#4E4F58` | `#23232A` | `#FFFFFF` | 8.13:1 | Neutral process steps, context boxes |
| Connector | `#4E4F58` stroke | | | | Lines between nodes, 1.8pt, with arrow markers |
| Brand role | `#43205b` | `#2f193b` | `#FFFFFF` | 13.16:1 | Action. The Royal highlight step. Royal only |

A node carries its own ground, so these values do not change on a band.

### 1.7 Charts

Chart colors come from the house data set, never from the brand palette. A brand color is never a chart series. The standard is [data-color.md](data-color.md). The one chart value that follows the brand is the sequential ramp:

| Step | 100 | 200 | 300 | 400 | 500 | 600 | 700 |
|---|---|---|---|---|---|---|---|
| On light | `#f0e1fd` | `#e2c2fb` | `#d29ef8` | `#ba7ce4` | `#9d60c6` | `#7f42a6` | `#572e72` |
| On dark | `#3d1f52` | `#572e72` | `#7f42a6` | `#9d60c6` | `#ba7ce4` | `#d29ef8` | `#e2c2fb` |

The Royal ramp is purple and step 700 is `--fg-accent` `#572e72`. Steps 100 and 200 are for continuous scales only. On a dark ground the lightest step is the largest value.

### 1.8 Contrast

WCAG 2 relative luminance. Body-size text needs 4.5:1. Large text needs 3:1 and starts at 18pt regular or 14pt bold. Use these figures. Do not restate a different one.

| Pair | Ratio | Verdict |
|---|---|---|
| `#23232A` on `#FFFFFF` | 15.61:1 | Any size |
| `#23232A` on `#faf5fd` | 14.53:1 | Any size |
| `#23232A` on `#f0e1fd` | 12.56:1 | Any size |
| `#565860` on `#FFFFFF` | 7.09:1 | Any size |
| `#565860` on `#faf5fd` | 6.60:1 | Any size |
| `#565860` on `#f0e1fd` | 5.71:1 | Any size |
| `#6D6D77` on `#FFFFFF` | 5.12:1 | Any size. The dimmest text |
| `#6D6D77` on `#faf5fd` | 4.76:1 | Any size |
| `#6D6D77` on `#f0e1fd` | 4.12:1 | Fails. Never on Surface 2 |
| `#8A8B93` on `#FFFFFF` | 3.39:1 | Never text |
| `#572e72` on `#FFFFFF` | 10.30:1 | Any size |
| `#572e72` on `#faf5fd` | 9.59:1 | Any size |
| `#572e72` on `#f0e1fd` | 8.29:1 | Any size |
| `#43205b` on `#FFFFFF` | 13.16:1 | Any size |
| `#8260a2` on `#FFFFFF` | 5.07:1 | Never text, by rule |
| `#8260a2` on `#2f193b` | 3.13:1 | Fails. Never on the band |
| `#FFFFFF` on `#2f193b` | 15.87:1 | Any size |
| `#DDDDE3` on `#2f193b` | 11.73:1 | Any size |
| `#A3A4AC` on `#2f193b` | 6.40:1 | Any size |
| `#FFFFFF` on `#572e72` | 10.30:1 | Any size |
| `#DDDDE3` on `#572e72` | 7.61:1 | Any size |
| `#A3A4AC` on `#572e72` | 4.15:1 | Fails. Never on Mid |
| `#FFFFFF` on `#43205b` | 13.16:1 | Any size |

### 1.9 Never

- `#8A8B93`, `#D0D0D6` and `#E4E4E9` are never text.
- A brand color is never a status color and never a chart series.
- A status color is never a theme, a background or a decoration.
- The band is never the reading surface of a document.
- No color enters a document that is not in `tokens.json`.
- `#8260a2` is never text and never a large background.
- `#8260a2` never sits on `#2f193b`.
- White text sits on `#2f193b`, `#572e72` or `#43205b` only. Never on `#8260a2`.
- Background tints are `#faf5fd` and `#f0e1fd` only. Nothing stronger.
- Dark grounds are `#2f193b` and `#572e72` only.
- A partner facility color is never sampled from a logo.

---

## 2. Logo

### 2.1 Roles and files

Ask for a role, never a filename. Filenames differ between brands. `-on-light` is the file placed on a light background. `-on-dark` is the file placed on a dark one. SVG files are in `assets/logos/`. PNG files are in `for-humans/logos/png/`, each at two widths.

| Role | SVG | PNG | The artwork |
|---|---|---|---|
| `horizontal-on-light` | `horizontal-purple.svg` | `Royal-Ambulance-horizontal-purple-1200w.png`, `-2400w.png` | `#43205b` crown and wordmark |
| `horizontal-on-dark` | `horizontal-white.svg` | `Royal-Ambulance-horizontal-white-1200w.png`, `-2400w.png` | White crown and wordmark |
| `compact-on-light` | None | None | Royal ships no compact lockup |
| `compact-on-dark` | None | None | Royal ships no compact lockup |
| `mark-on-light` | `crown-purple.svg` | `Royal-Ambulance-crown-purple-512w.png`, `-1024w.png` | The `#43205b` crown |
| `mark-on-dark` | `crown-white.svg` | `Royal-Ambulance-crown-white-512w.png`, `-1024w.png` | The white crown |
| `stacked-on-light` | `stacked-purple.svg` | `Royal-Ambulance-stacked-purple-1200w.png`, `-2400w.png` | `#43205b` crown over the wordmark |
| `stacked-on-dark` | `stacked-white.svg` | `Royal-Ambulance-stacked-white-1200w.png`, `-2400w.png` | White crown over the wordmark |
| `app-icon` | None | None | Royal ships no app icon |

The horizontal lockup is the primary logo. The crown is the icon-only mark, for favicons, badges, avatars and table corners. The stacked lockup is for portrait and square formats. `tokens.json` maps `stacked-on-light`. `brands.json` does not, so resolve that role from `tokens.json`.

### 2.2 Specifications

| Property | Value |
|---|---|
| Horizontal viewBox | `0 0 735.76 179.54` |
| Compact viewBox | None |
| Mark viewBox | `0 0 692.1 692.1` |
| Stacked viewBox | `0 0 526.66 418.93` |
| App icon viewBox | None |
| Fill on light | `#43205b` in every lockup, the crown included |
| Fill on dark | `#FFFFFF` |
| Minimum, horizontal | 110px on screen, 1in in print |
| Minimum, compact | None |
| Minimum, mark | 32px on screen, 0.33in in print |
| Minimum, app icon | None |
| Clear space | The height of the crown, on all four sides |
| Vector master | The SVG files in `assets/logos/`. No separate vector master ships |
| Embedding | Place the PNG in an office document. Reference the CDN URL with `<img>` in HTML. Never inline a copied SVG path |

### 2.3 Do not

- Do not stretch, skew or rotate a logo.
- Do not recolor a logo, and do not invert one with a filter. Pick the file for the ground.
- Do not add a shadow, a glow, an outline or a gradient.
- Do not place a logo on a photograph without a solid backing.
- Do not set a logo below its minimum size.
- Do not crop the clear space. Shrink the logo instead, down to the minimum.
- Do not put one brand’s logo twice on a page or slide.
- Do not separate the crown from the wordmark in the horizontal or stacked lockup.
- Do not change the fill to anything but `#43205b` or white.

---

## 3. Co-brand

Apex Paramedics and Royal Ambulance are operating companies under Collective Edge, and the reader should be able to see it. The rules in this section are identical in all three kits.

### 3.1 The lockup

“Powered by Collective Edge” is one lockup in two sizes. On a site or a dashboard it is the label `POWERED BY` over the Collective Edge horizontal lockup, under a hairline. In a PDF, a deck or an image it is small and quiet: the words `Powered by`, then the logo on the same line at its minimum width. The table gives the site lockup, then the document lockup. `cobrand` in `brands.json` carries every value below, and `snippets/cobrand.css` is the HTML implementation.

| Part | Value |
|---|---|
| Label | `POWERED BY`. Weight 600, uppercase, 12px, tracking 0.080em |
| Label color | `#6D6D77` on white, 5.12:1. `#A3A4AC` on a dark ground |
| Lockup on white | The Collective Edge `horizontal-on-light` file, `assets/logos/horizontal-black.svg` in the Collective Edge kit |
| Lockup on a dark ground | The Collective Edge `horizontal-on-dark` file, `assets/logos/horizontal-white.svg` in the Collective Edge kit |
| Width | 204px wide, 34px tall. The artwork is 6:1 |
| Floor | 120px. On a site, a floor and not a target |
| Hairline | 0.75pt (1px) above the label. `#E4E4E9` on white. White at 12 percent on a dark ground |
| Spacing | On a site: 18pt (24px) above the hairline, 18pt (24px) between hairline and label, 9pt (12px) between label and lockup |
| Document lockup | In a PDF, a deck or an image. One line: the words `Powered by`, weight 400, 9pt, `#6D6D77`, then 6pt to the right the Collective Edge horizontal logo, 1.25in (120px) wide, 0.208in (20px) tall. No hairline of its own. On a closing slide the words are 12pt, `#A3A4AC`. Never larger. `reference/layout.md` section 3.12 |
| Figure line | On a chart or data graphic made on its own. No logo. The words `Powered by Collective Edge`, bottom right, weight 400, 9pt, `#6D6D77` |
| Ground | The light lockup sits on white, not on a tint |
| CSS classes | `.ce-powered` on a dark ground. `.ce-powered ce-powered-light` on white. `.ce-powered-text` where no mark fits |

The label measures 6.40:1 on this brand’s band.

### 3.2 Where it goes

1. “Powered by Collective Edge” appears once on everything Apex Paramedics and Royal Ambulance deliver as a PDF, a deck or an image: memo, one-pager, report, proposal, deck, and a chart or data graphic made on its own. A working-doc and a sheet never carry it, as a lockup or as words. The rule follows the type, not the file format: a working-doc exported to PDF stays as it is.
2. A Collective Edge document carries the Collective Edge logo in its band and no lockup.
3. Where the Collective Edge mark shares a surface with another brand, the lockup is on that surface, once.

| Surface | Place |
|---|---|
| Memo, one-pager | The footer row of page 1, at left |
| Report | The last line of the body on the last page |
| Deck | The footer row of the closing slide, at left |
| Chart or data graphic made on its own | One line of words, bottom right. No logo |
| Working-doc, sheet | None |
| Site | The footer |
| Dashboard | The sidebar header |
| Data page or methodology page | Anywhere a number was computed and not typed |

### 3.3 Never

- Never put the lockup on the partner’s own mark or inside its lockup.
- Never merge, nest or recolor either mark to match the other.
- Never use it twice in one document or on one surface.
- Never set the phrase as type where the mark fits. A chart or data graphic made on its own is the one place the words stand alone.
- Never design the lockup down to the 120px floor on a site or a dashboard.
- Never set it larger than 1.25in in a PDF, a deck or an image.
- Never put it on a working-doc or a sheet.
- Never put it on a clinical instruction.
- Never put it on a patient-facing consent or safety document.

The last two, the working-doc and the sheet are the only documents that carry no lockup.

### 3.4 Who leads

Ask whose name is on the door.

| | Partner led | Collective Edge led |
|---|---|---|
| When | The surface belongs to Apex Paramedics, Royal Ambulance or another partner. The default | A Collective Edge product delivered to a partner or its customer |
| Logo | The partner’s logo heads the surface | The Collective Edge logo heads the surface |
| Palette | The partner’s palette runs the band and the accents | White canvas and the Collective Edge tiers |
| Collective Edge adds | Type, hairlines and whitespace. No hue. The lockup, once | The partner’s color as the one hue, on live and active states only. Never a chart series |

When in doubt, the partner leads. Hold one mode on a surface. Never stack more than three marks in one lockup. Take a partner’s hex from `brands.json` or from that partner’s kit, never from a copy. `unreconciled` in `brands.json` lists placeholder colors for brands with no kit. Confirm those with the owner before use.

### 3.5 The wedge

The Edge wedge is the one part of the Collective Edge block mark that takes color, and that color is the partner’s. Every combination ships as a file in the Collective Edge kit, under `assets/logos/`. Never recolor a mark by hand.

| Wedge | Hex | On light | On dark |
|---|---|---|---|
| Alone | `#C8C8C8` | `mark-black.svg` | `mark-white.svg` |
| With Royal Ambulance | `#572E72` | `mark-black-royal.svg` | `mark-white-royal.svg` |
| With Apex Paramedics | `#FDB61C` | `mark-black-apex.svg` | `mark-white-apex.svg` |

The wedge color never leaves the wedge. The block and the letters stay black or white on every surface. On a Royal surface the wedge is Purple `#572E72`.

---

## 4. Voice

### 4.1 Character

Royal writes for the reader who is between calls. Short declarative sentences.

### 4.2 Rules

- Short declarative sentences. Active verbs. No filler and no throat-clearing.
- No em dashes. Use a period, a comma or `·`. An en dash only in a date or number range, per rule 14 of the type system.
- Exact values. The real number, never a rounded one. The hex, never a description of the color.
- A label, a value, and nothing between them. No helper text under a field, no caption restating the thing above it, no parenthetical after a heading.
- Write a caption only when it carries information the thing above it does not.
- Sentence case for every heading. Uppercase for the band title, the title slide title and the site lockup label only. Always tracked, never past four words.
- No emoji, no exclamation points, no rhetorical questions.
- Clinical and operational terms stay precise. Never soften a protocol term.
- Name people, partners and facilities exactly as they write themselves.
- When you hand work back, state the brand, the document type, the logo role and how the font embedded.
- The reader is between calls. Keep it short.

---

## 5. Only in this kit

### 5.1 Partner facility colors

A chart that compares partner facilities may give each facility its own color. It is opt-in and gated. Read [partner-colors.md](partner-colors.md) first. Never sample a color from a logo.

### 5.2 The action node

Royal adds one diagram role. Action: fill `#43205b`, border `#2f193b`, text `#FFFFFF`, 13.16:1. It marks the Royal highlight step. It is in `tokens.json` under `diagramRoles.brandRoles` and in no other kit.

### 5.3 Photography

Royal ships photography in `for-humans/photos/`. No other kit does.

---

## 6. Files and versions

| What | Path |
|---|---|
| CDN root | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/` |
| Repository | `collective-edge/royal-brand-kit` |
| Palette, authoritative | `snippets/palette.css` |
| Colors as data | `tokens.json`, version 2.0 |
| Type as data | `snippets/type-tokens.json` |
| Registry of every brand | `brands.json` |
| Logos | `assets/logos/` as SVG, `for-humans/logos/png/` as PNG |
| Fonts | `for-humans/fonts/static/` as static files. The variable font is served from the Collective Edge kit |
| Templates | `templates/` |

`@main` serves the latest. Production pins a tag in place of `@main`. Bump the minor version for an additive change. Bump the major version when a palette value or a mark changes.

These files predate the house type system. They stay on the CDN because documents already point at them. New work never loads them.

| Deprecated | Replaced by |
|---|---|
| `snippets/brand-base.css` | `snippets/type-system.css` and `snippets/palette.css` |
| `assets/colors.json` | `tokens.json` |
| `assets/fonts/Montserrat-VariableFont_wght.ttf` in this kit | The Collective Edge copy, woff2 first, TTF second |
