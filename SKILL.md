---
name: royal-brand-guidelines
description: Applies Royal Ambulance's brand standards — purple-centric color palette, Montserrat typography, and logo usage — to ANY output representing Royal Ambulance. Use whenever generating Royal Ambulance materials of any kind: emails, social posts, slides, documents, web content, marketing collateral, internal comms, training materials, flyers, letters, one-pagers, tables, or any visual artifact. Also use when reviewing existing materials for brand compliance.
---

# Royal Ambulance — Brand Guidelines

**When to apply:** Whenever creating or reviewing any material that represents Royal Ambulance, in any medium (digital or print, formal or casual). This skill defines the look-and-feel; specific layouts and templates are intentionally not prescribed here so the brand can apply across many formats.

## CRITICAL: Asset loading

**This brand kit is cloud-hosted.** All fonts and logos live on a public CDN (jsDelivr, backed by GitHub) so any Claude session anywhere can pull them down. **Do not look for local files.** Use the URLs below directly in generated HTML, CSS, or markdown.

**Base CDN URL:**
```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/
```

**Specific asset URLs (copy these into outputs):**

| Asset | URL |
|---|---|
| Montserrat (variable TTF) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf` |
| Horizontal logo (purple) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-purple.svg` |
| Horizontal logo (white) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg` |
| Crown only (purple) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/crown-purple.svg` |
| Crown only (white) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/crown-white.svg` |
| Stacked logo (purple) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/stacked-purple.svg` |
| Stacked logo (white) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/stacked-white.svg` |
| Brand colors (JSON) | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/colors.json` |

**Drop-in base CSS** (includes @font-face for Montserrat + brand CSS variables):
```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/brand-base.css">
```

**For PDF rendering (weasyprint, wkhtmltopdf, Chrome print):** always include the @font-face declaration so the font is embedded in the output PDF. Use this minimal block at the top of any HTML you intend to print:

```css
@font-face {
  font-family: 'Montserrat';
  src: url('https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf') format('truetype');
  font-weight: normal;
}
@font-face {
  font-family: 'Montserrat';
  src: url('https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf') format('truetype');
  font-weight: bold;
}
body { font-family: 'Montserrat', Calibri, Arial, sans-serif; }
```

---

## 1. Brand Colors

Royal Ambulance uses a purple-centric palette. Every piece of collateral should draw from these colors exclusively — never introduce off-brand hues.

| Name          | Hex       | RGB              | Usage                                                        |
|---------------|-----------|------------------|--------------------------------------------------------------|
| Dark Purple   | `#2f193b` | 47, 25, 59       | Primary headers, hero backgrounds, section dividers          |
| Purple        | `#572e72` | 87, 46, 114      | Column headers, accent bars, contact labels, category badges |
| Light Purple  | `#8260a2` | 130, 96, 162     | Tertiary accents, hover states, lighter highlights           |
| Royal Purple  | `#43205b` | 67, 32, 91       | Logo fill color, alternate dark accent                       |
| Black         | `#000000` | 0, 0, 0          | Body text, high-contrast headings on light backgrounds       |
| White         | `#FFFFFF` | 255, 255, 255    | Text on dark backgrounds, page background                    |

### Color usage rules

- **Dark Purple (#2f193b)** is the dominant brand color. Use for page headers, hero/title bars, section dividers, full-width bands.
- **Purple (#572e72)** is the workhorse accent. Use for column headers, accent bars, callout borders, label chips, buttons, links.
- **Light Purple (#8260a2)** is used sparingly for tertiary accents only. Never as a background for large areas — too washed out at scale.
- **Backgrounds:** White is primary. For subtle alternating rows, callouts, or backgrounds, use a very light purple tint such as `#faf5fd` or `#f8f4fc` — never anything stronger.
- **Text contrast:** White text on Dark Purple. Black text on white. Never light purple text on dark purple — insufficient contrast.
- **No off-brand colors for decorative purposes.** Functional/data colors (e.g., chart series, status indicators) should stay within or harmonize with the purple palette wherever possible.

### Extended palette (functional roles in diagrams, status, dashboards)

These are NOT primary brand colors but are official conventions for diagrams (flowcharts, dashboards, process docs) where additional roles are needed beyond the purple palette. Apply consistently — do not invent new hues for these roles.

| Role             | Hex       | Border    | Use                                                 |
|------------------|-----------|-----------|-----------------------------------------------------|
| Decision / query | `#4a8e3a` | `#3a7029` | Decision boxes, questions, branch points            |
| Warning / callout| `#f57c00` | `#cc6600` | Warning boxes, advisories, "watch out" pills        |
| Info / process   | `#3e3e3e` | `#2a2a2a` | Neutral process steps, context boxes                |

Color does the differentiation work — all diagram shapes should be **rectangles with small rounded corners (radius ~6px)**. Role is communicated by fill color, not by shape.

---

## 2. Logo

### Logo files (CDN URLs above)

- **Horizontal logo** — primary lockup, default for most contexts with horizontal room
- **Crown** — icon-only mark, for compact contexts (favicons, badges, social avatars, table corners)
- **Stacked** — square-ish lockup for portrait orientations or tight squares

Each comes in `purple` (for white/light backgrounds) and `white` (for dark backgrounds).

### Logo specifications

- **Horizontal viewBox:** `0 0 735.76 179.54`
- **Crown viewBox:** `0 0 179.54 179.54`
- **Default fill:** `#43205b` (Royal Purple) on light, `#FFFFFF` on dark.

### Usage rules

1. **Default to the horizontal logo** for any context with horizontal room. Use the crown-only mark only where space requires it (small icons, badges).
2. **Minimum clear space:** Maintain padding around the logo equal to at least the height of the crown icon on all sides.
3. **On dark backgrounds:** Use the `*-white.svg` variant. Do not apply CSS filters to recolor — use the correct file.
4. **On white/light backgrounds:** Use the `*-purple.svg` variant.
5. **Minimum size:** Never render the horizontal logo smaller than ~100px wide on screen or 1 inch in print. The crown-only mark can go down to ~32px.
6. **Do NOT:**
   - Stretch, skew, or rotate the logo
   - Place the logo on busy photographic backgrounds without a solid backing
   - Change the logo colors to anything other than Royal Purple or white
   - Add drop shadows, glows, outlines, or gradients to the logo
   - Separate the crown icon from the wordmark in the horizontal lockup
7. **Embedding:** Reference the logo SVG URL directly with `<img src="...">` — it's a public CDN, no auth needed.

---

## 3. Typography

**Montserrat is the brand font for every output.** No exceptions.

- Title bands / hero headlines: **800 weight, ALL CAPS, +1.5 letter-spacing**
- Section headers: **700 weight**, normal case or all caps
- Body: **500 weight** (Medium) on light backgrounds, **400** (Regular) for long-form
- Tiny labels / kickers: **800 weight, ALL CAPS, +2 letter-spacing**, often in muted purple

**Always include the @font-face declaration** at the top of any generated HTML, even if Montserrat is installed on the rendering machine. This guarantees consistent rendering and embeds the font in any downstream PDF. See the asset-loading section above for the snippet.

---

## 4. Layout conventions (Royal house style)

These patterns are lifted from the Royal house style (MotiveCare flowchart, UCSF/AHS case studies, ECH one-pager). Pattern-match these visually for new collateral.

### Header band
- Full-width strip across the very top of the page.
- Background: Dark Purple `#2f193b`. Optional gradient to Purple `#572e72` on the right side.
- White Royal horizontal logo top-right (~1.4–1.8in wide).
- Title text top-left: white, Montserrat 800, ALL CAPS, 18–22pt for one-pagers / 32–44pt for slides.

### Sub-banner (optional)
- Thin Purple `#572e72` strip just below the header band.
- White Montserrat 600, 8–9pt, ALL CAPS, +2.5 letter-spacing.
- Used for kicker / partner / category line.

### Flowchart nodes
- All node shapes are rounded rectangles (radius 6px).
- **Standard step:** Dark gray `#3e3e3e`, white ALL-CAPS Montserrat 800, optional muted subtitle below.
- **Action / highlight step:** Royal Purple `#43205b`, same text treatment.
- **Decision:** Green `#4a8e3a` pill (border-radius 999px), white ALL-CAPS Montserrat 800.
- **Warning / critical:** Orange `#f57c00`, white ALL-CAPS Montserrat 800.
- **Branch labels (YES / NO):** White box with colored border matching the branch outcome.
- Connector lines: `#3e3e3e`, 1.8pt stroke, with arrow markers.

### Stat / metric callouts
- Big number: Montserrat 800, 36–60pt, Royal Purple.
- Unit label: Montserrat 500, 10pt, Muted.
- Kicker above: Montserrat 800, 8pt, ALL CAPS, Purple, +2 letter-spacing.

### Tables
- Header row: `#2f193b` (Dark Purple) fill, white Montserrat 800 ALL CAPS 9pt.
- Body rows: white, alternating with `#faf5fd` if alternation helps readability.
- Hairline borders: `#E2E8F0`.

### Footer
- Slim full-width footer.
- Top border: `#E2E8F0` hairline.
- Left: "Royal Ambulance | {Document Title}" in `#64748B` Muted.
- Right: revision marker (e.g., "Rev. 06.26") in Purple `#572e72`, Montserrat 700.

---

## 5. Quick-reference snippets

**Header band (drop-in HTML):**
```html
<header style="background:#2f193b; color:#FFFFFF; padding:0.32in 0.5in; display:flex; align-items:center; justify-content:space-between; font-family:'Montserrat',sans-serif;">
  <div style="font-weight:800; font-size:18pt; letter-spacing:1.5px; text-transform:uppercase;">YOUR TITLE</div>
  <img src="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg" style="width:1.6in;" alt="Royal Ambulance">
</header>
```

**Sub-banner:**
```html
<div style="background:#572e72; color:#FFFFFF; padding:6px 0.5in; font:600 8.5pt 'Montserrat'; letter-spacing:2.5px; text-transform:uppercase;">
  KICKER / PARTNER / CATEGORY
</div>
```

**Footer:**
```html
<footer style="border-top:1px solid #E2E8F0; padding:6px 0.5in; font:400 8pt 'Montserrat'; color:#64748B; display:flex; justify-content:space-between;">
  <span>Royal Ambulance &nbsp;|&nbsp; Document Title</span>
  <span style="font-weight:700; letter-spacing:1.5px; color:#572e72;">Rev. MM.YY</span>
</footer>
```

---

## 6. Versioning

Pinning to `@main` always serves the latest version. To pin to a stable release, replace `@main` with a tag, e.g. `@v1.0`. Bump tags when you make breaking changes (logo redesign, color shifts).

---

## 7. Verify before you ship

A brand deliverable fails on details a spell-check can't catch — overlapping text, a clipped logo, an accent you can't read, a font that quietly fell back to Arial. Before you call any Royal deliverable done, verify the **rendered** result, not the source:

1. **Render it and look.** Render the output to an image or PDF (or open the HTML in a browser) and visually inspect what actually renders — text overlap, clipping, and overflow are invisible in the source and only show up in pixels. If your environment can't render, say so plainly instead of claiming it looks clean.
2. **No collisions.** Nothing overlapping, colliding, clipped, or overflowing — no text running past its container, off the page, or into the logo.
3. **Legibility.** Contrast holds — light purple `#8260a2` is never body text (too washed out at text sizes); body copy stays black or purple `#572e72`. Light text only on dark backgrounds.
4. **Logo integrity.** Correct variant for the background (the white variant on dark), never stretched, skewed, or recolored; clear space respected; never on a busy area without a solid backing.
5. **Type.** Montserrat actually rendered, not a system fallback — and for PDFs, actually *embedded* in the file. Confirm it before you call the job done.
6. **On-brand.** Every color is drawn from the palette above, no off-brand hues; margins and alignment consistent; page breaks clean for print.
7. **State what you applied.** When you hand it back, name the brand choices you made (which logo variant, which accent, how the font embedded) so the user can verify at a glance.
