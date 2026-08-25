---
name: royal-brand-guidelines
description: Applies Royal Ambulance’s brand standards to any output representing Royal Ambulance: the purple palette, the crown wordmark, and the shared Collective Edge house type system set in Montserrat. Use when producing or reviewing a Royal Ambulance email, slide, deck, one-pager, report, letterhead, flyer, document, web page, table, chart, diagram, flowchart, case study, proposal, or PDF, and when checking existing Royal material for brand compliance. Covers asset CDN URLs, logo role selection, color and contrast rules, the fifteen type rules, the house layout patterns, and the validator to run before shipping.
---

# Royal Ambulance · brand guidelines

House type system v1.0.

Royal Ambulance is a Bay Area medical transportation company and an operating company under Collective Edge. It inherits the house type system unchanged and supplies two things of its own: a purple palette and the crown wordmark.

Reference, read on demand:

- [reference/brand.md](reference/brand.md) · full color table, contrast traps, logo specifications, voice
- [reference/type-system.md](reference/type-system.md) · the type standard and the fifteen rules
- [reference/layout.md](reference/layout.md) · header band, sub-banner, flowchart nodes, stat callout, table, footer, the Collective Edge co-brand lockup
- `tokens.json` · colors for python-pptx, python-docx, matplotlib, reportlab
- `snippets/type-tokens.json` · type values for the same generators

---

## 1. Load the assets

Three stylesheets, in this order. `type-system.css` is identical in every kit and is served from the Collective Edge kit. `palette.css` is the only file that differs. `cobrand.css` is the co-brand lockup, also identical everywhere, and it reads the palette, so it loads last.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/type-system.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/palette.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/cobrand.css">
```

Inline this block at the top of every HTML file you generate, even when Montserrat is installed on the rendering machine. A local copy makes the file render correctly on that one machine and wrong everywhere else, and only the declaration embeds the font in a downstream PDF (weasyprint, wkhtmltopdf, Chrome print). The `font-family` line is not optional: without it nothing selects Montserrat when the CDN stylesheet fails to resolve.

```css
@font-face {
  font-family: "Montserrat";
  src: url("https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.woff2") format("woff2-variations"),
       url("https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf")   format("truetype-variations");
  font-weight: 400 800;
  font-style: normal;
  font-display: swap;
}
html, body { font-family: "Montserrat", "Helvetica Neue", Helvetica, Arial, sans-serif; font-synthesis: none; }
```

The range is `400 800`. 100, 200, 300 and 900 are forbidden at document sizes, so never open the axis to `100 900`.

### Logo roles

Ask for a role, never a filename. `-on-light` is the version you place **on** a light background.

| Role | URL |
|---|---|
| horizontal-on-light | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-purple.svg` |
| horizontal-on-dark | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg` |
| mark-on-light | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/crown-purple.svg` |
| mark-on-dark | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/crown-white.svg` |
| stacked-on-dark | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/stacked-white.svg` |

Horizontal is the default anywhere with horizontal room. Minimum width 110px for horizontal, 32px for the mark. Never recolor a mark with a filter. Pick the file for the ground. Full specifications in [reference/brand.md](reference/brand.md).

---

## 2. Color

| Name | CSS | Hex | Usage |
|---|---|---|---|
| Dark Purple | `--royal-dark-purple` | `#2f193b` | Header bands, hero grounds, section dividers, table header fill |
| Purple | `--royal-purple` | `#572e72` | Accent bars, callout borders, links, buttons, brand-colored text |
| Royal Purple | `--royal-royal-purple` | `#43205b` | Logo fill on light, stat numerals, flowchart action nodes |
| Light Purple | `--royal-light-purple` | `#8260a2` | Tertiary accents and hover only |
| Charcoal | `--royal-charcoal` | `#1E293B` | Body text on light. This is `--fg-1` |
| Surface | `--royal-surface` | `#faf5fd` | Tinted rows and callout fills |

Style through `--fg-*`, `--bg-*` and `--border-*`. Reach for a raw `--royal-*` value only where the brand color is the point.

Three rules that get broken most:

1. **Light Purple `#8260a2` is never body text and never a large background.** It measures 5.07:1 on `#FFFFFF`, so it clears AA at text sizes and fails AAA, and it washes out at scale. It is the tertiary accent, not a text color. Body text is `--fg-1` `#1E293B`, 14.63:1. Brand-colored text is `--fg-accent` `#572e72`, 10.30:1.
2. **Never put `#8260a2` on `#2f193b`.** On a dark ground use `--fg-on-dark-2` `#E0D6E8` or `--fg-on-dark-3` `#B0A2BC`.
3. **A brand purple is never a status color.** Status is `--status-go` `#1E7A4D`, `--status-warn` `#B5821A`, `--status-stop` `#B0322B`, `--status-info` `#2A5A8C`, identical in every brand.

Diagram roles come from `brands.json` and are identical across the house: decision `#4a8e3a`, warning `#f57c00`, process `#3e3e3e`. Everything else is in [reference/brand.md](reference/brand.md).

---

## 3. Type

Type is shared with Apex Paramedics and Collective Edge and is never forked for Royal. Read [reference/type-system.md](reference/type-system.md) for the scale, the measure, the micro-typography and the fifteen rules. Style through the `.bk-*` classes. Do not restate the scale from memory.

Three things to never do:

1. **No italic**, at any weight, in any brand. Never synthesize an oblique.
2. **No weight outside 400, 600, 700, 800.** 400 body, 600 subheads and caps labels, 700 headings and emphasis and stat numerals, 800 hero only.
3. **No tracking in px or pt.** Tracking is always em, from the tracking tokens.

On any dark ground put `.bk-on-dark` on the container. It adds 0.005em tracking at every step and drops one weight where the step is 700 or heavier. 600 is the floor, so `.bk-h3`, `.bk-h4`, `.bk-eyebrow` and `.bk-table th` hold 600 and gain the tracking alone. Every Royal document opens on a dark band, so every Royal document needs it.

---

## 4. Layout

Header band, sub-banner, flowchart nodes, stat callout, table and footer are in [reference/layout.md](reference/layout.md) as copy-pasteable blocks. Start every one-pager, report and letterhead with the band:

```html
<header class="bk-on-dark" style="background:var(--bg-band); display:flex; align-items:center; justify-content:space-between; gap:var(--space-6); padding:var(--space-6) 0.5in;">
  <div class="bk-h2 bk-caps" style="margin:0;">
    Document title
  </div>
  <img src="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg"
       alt="Royal Ambulance" style="width:1.6in; height:auto; display:block; flex:none;">
</header>
```

`.bk-caps` resolves the uppercase and the caps tracking at whatever step it sits on, and `.bk-on-dark` adds the 0.005em bonus. Never type either value. Slides swap `.bk-h2` for `.bk-display-md`.

**Powered by Collective Edge.** Royal is an operating company under Collective Edge, and the reader should be able to see it. The lockup rides beside the Royal mark, never inside it, with a hairline between them, at 204px, which is wider than the Royal mark above it on purpose. `.ce-powered` on a dark band, `.ce-powered ce-powered-light` on white, `.ce-powered-text` where no mark fits. It belongs on footers, dashboard sidebars, closing slides, data pages, anywhere a number was computed rather than typed. Never on the Royal mark itself, never on a clinical instruction or a patient-facing consent, never twice on one surface. Both grounds, the measured contrast and copy-pasteable blocks are in [reference/layout.md](reference/layout.md).

**UI controls.** Buttons, links, form controls, status badges and the focus ring are shared and identical in all three brands: [`snippets/ui.css`](snippets/ui.css), loaded third after `palette.css`, with the standard in [reference/ui.md](reference/ui.md). Cards, tables, dashboard shells, navigation and heroes are not shared; each site builds its own on those tokens. `Examples/ui-controls.html` renders every control in every state.

---

## 5. Verify before shipping

```bash
python3 scripts/validate.py path/to/output.html
python3 scripts/ui-audit.py path/to/page.html --width 375 --width 768 --width 1440
```

It checks rules 1, 2, 5, 9, 10, 13 and 14 mechanically and exits non-zero on a violation. It cannot see the rest, so also look:

- [ ] Rendered, not just written. Open it. Overlap, clipping and overflow are invisible in source. If your environment cannot render, say so plainly instead of claiming it looks clean.
- [ ] No collisions. Nothing overlapping, clipped or overflowing. No text running past its container, off the page, or into the logo.
- [ ] Montserrat actually rendered, not a fallback. For PDF, actually embedded.
- [ ] No italic anywhere.
- [ ] The dark band is one weight lighter than the light-surface equivalent.
- [ ] Correct logo role for the ground, clear space respected, never stretched or recolored.
- [ ] Body text holds its 54ch measure and does not run the full container width.
- [ ] “Powered by Collective Edge” on the footer, the sidebar or the closing slide. Once, beside the Royal mark and never inside it.
- [ ] Every color comes from the palette. No off-brand hue.
- [ ] Margins and alignment consistent across every page and every rail.
- [ ] Page breaks clean for print. No table, card or stat block split across a page.
- [ ] No helper text, no caption restating the thing above it, no parenthetical after a heading, no em dash.
- [ ] Nothing under 9pt on paper. A `.bk-code` span inside a 9pt caption or eyebrow needs `font-size:1em`, because 0.94em of 9pt is 8.46pt.

State which brand choices you applied when you hand the work back: logo role, accent, how the font embedded.
