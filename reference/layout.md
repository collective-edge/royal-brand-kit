# Royal Ambulance · house layout patterns

House type system v1.0. These are the Royal patterns, lifted from the MotiveCare flowchart, the UCSF and AHS case studies and the ECH one-pager, and rebuilt on the v1.0 scale. Pattern-match them for new collateral.

Every block below is copy-pasteable. Both stylesheets must be loaded first:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/type-system.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/palette.css">
```

What changed from the pre-v1.0 house style:

| Element | Was | Now |
|---|---|---|
| Band title | 800, 18pt, +1.5px | `.bk-h2` inside `.bk-on-dark` · 600, 24pt, `--tr-caps-h2` plus the dark bonus |
| Uppercase caps label | 800 | 600, `.bk-eyebrow` |
| Table header | 800 caps 9pt | 600 caps 9pt, `.bk-table th` |
| Stat numeral | 800, 36pt to 60pt | 700, `.bk-stat` at 42pt |
| Any dark band | Same weight as light | 0.005em more tracking at every step, one weight lighter at 700 and heavier. 600 is the floor |
| Tracking | px | em, from the tracking tokens |

Style through `--fg-*`, `--bg-*` and `--border-*`. Reach for a raw `--royal-*` value only where the brand color is the point: the band, an accent rule, a stat numeral, a chart series.

---

## Header band

Full-width strip across the top of every Royal document. Dark Purple ground, white horizontal logo on the right, title on the left. `.bk-on-dark` drops the title one weight and opens its tracking.

```html
<header class="bk-on-dark" style="background:var(--bg-band); display:flex; align-items:center; justify-content:space-between; gap:var(--space-6); padding:var(--space-6) 0.5in;">
  <div class="bk-h2 bk-caps" style="margin:0;">
    Document title
  </div>
  <img src="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg"
       alt="Royal Ambulance" style="width:1.6in; height:auto; display:block; flex:none;">
</header>
```

`.bk-caps` resolves the uppercase and the caps tracking at whatever step it sits on, and `.bk-on-dark` adds the 0.005em bonus through `--tr-dark`. Never type either value. Slides and title surfaces swap `.bk-h2` for `.bk-display-md`, which resolves to 42pt at 700 on the dark ground. Nothing else changes. The logo runs 1.4in to 1.8in wide. An optional left-to-right gradient from `--royal-dark-purple` to `--royal-purple` is sanctioned on the band and nowhere else.

---

## Sub-banner

Thin Purple strip directly under the header band. Kicker, partner or category line, never more than four words.

```html
<div class="bk-on-dark" style="background:var(--royal-purple); padding:var(--space-2) 0.5in;">
  <div class="bk-eyebrow" style="color:var(--fg-on-dark-1); margin:0;">Partner · Category</div>
</div>
```

`.bk-eyebrow` is 600 at 9pt. Its 0.080em opens to 0.085em inside `.bk-on-dark`, and 600 is the floor, so the weight holds. The explicit `--fg-on-dark-1` overrides the dimmed eyebrow color, which does not hold contrast on `#572e72`.

---

## Flowchart nodes

Every node is a rectangle at `--radius-md` 6px. Role is communicated by fill, never by shape. Labels are 600 uppercase, not 800.

```html
<!-- Standard process step -->
<div class="bk-on-dark" style="background:var(--diagram-process); border:1px solid var(--diagram-process-border); border-radius:var(--radius-md); padding:var(--space-3) var(--space-4);">
  <div class="bk-eyebrow" style="color:var(--fg-on-dark-1); margin:0;">Dispatch confirms</div>
  <div class="bk-caption" style="margin:var(--space-1) 0 0;">Unit <span class="bk-code">R-114</span> assigned</div>
</div>

<!-- Royal action or highlight step -->
<div class="bk-on-dark" style="background:var(--royal-royal-purple); border:1px solid var(--royal-dark-purple); border-radius:var(--radius-md); padding:var(--space-3) var(--space-4);">
  <div class="bk-eyebrow" style="color:var(--fg-on-dark-1); margin:0;">Royal accepts</div>
</div>

<!-- Decision -->
<div class="bk-on-dark" style="background:var(--diagram-decision); border:1px solid var(--diagram-decision-border); border-radius:var(--radius-pill); padding:var(--space-2) var(--space-5);">
  <div class="bk-eyebrow" style="color:var(--fg-on-dark-1); margin:0;">Bed available</div>
</div>

<!-- Warning -->
<div class="bk-on-dark" style="background:var(--diagram-warning); border:1px solid var(--diagram-warning-border); border-radius:var(--radius-md); padding:var(--space-3) var(--space-4);">
  <div class="bk-eyebrow" style="color:var(--fg-on-dark-1); margin:0;">Coverage expires today</div>
</div>

<!-- Branch label -->
<div style="background:var(--bg-canvas); border:1px solid var(--diagram-decision); border-radius:var(--radius-sm); padding:var(--space-1) var(--space-2);">
  <div class="bk-eyebrow" style="color:var(--fg-1); margin:0;">Yes</div>
</div>
```

Branch label borders match the outcome they carry: `--diagram-decision` on yes, `--diagram-warning-border` or `--diagram-process-border` on no. Connectors are `--diagram-connector` `#3e3e3e` at 1.8pt with arrow markers.

The white label on the warning node is not legible at caption size. `#FFFFFF` on `#f57c00` measures 2.70:1 and `#FFFFFF` on `#4a8e3a` measures 4.02:1. Both fills and their white text are frozen pending a decision from the brand owner, so the blocks above ship as they are. When the label has to be read rather than scanned, use the branch-label pattern instead: `--bg-canvas` ground, role-colored border, `--fg-1` text. See `brand.md` section 1.

A yes or a no outcome is a status, not a diagram role. Fill those with `--status-go` `#1E7A4D` and `--status-stop` `#B0322B`, which hold white at caption size, and never with a red or green picked for the document.

---

## Stat callout

Kicker, numeral, unit. Nothing between them, no caption restating the number.

```html
<div style="display:flex; flex-direction:column; gap:var(--space-1);">
  <div class="bk-eyebrow" style="color:var(--fg-accent); margin:0;">Median response</div>
  <div class="bk-stat" style="color:var(--royal-royal-purple);">11.4</div>
  <div class="bk-caption" style="margin:0;">minutes, Q2&nbsp;2026</div>
</div>
```

`.bk-stat` is 700 at 42pt with `tabular-nums lining-nums` already applied. Do not raise it to 800. At display sizes ExtraBold reads as a slab, not a number.

---

## Table

Dark Purple header row, white body, hairline rules, `--bg-surface` alternation only where it helps a long table read.

```html
<table class="bk-table" style="width:100%; color:var(--fg-1); font-size:var(--fs-body-sm); line-height:var(--lh-body-sm); letter-spacing:var(--tr-body-sm);">
  <thead class="bk-on-dark" style="background:var(--bg-band);">
    <tr>
      <th style="color:var(--fg-on-dark-1); padding:var(--space-2) var(--space-3);">Facility</th>
      <th style="color:var(--fg-on-dark-1); padding:var(--space-2) var(--space-3);">Level</th>
      <th style="color:var(--fg-on-dark-1); padding:var(--space-2) var(--space-3); text-align:right;">Transports</th>
    </tr>
  </thead>
  <tbody>
    <tr style="border-bottom:1px solid var(--border-1);">
      <td style="padding:var(--space-2) var(--space-3);">UCSF Parnassus</td>
      <td style="padding:var(--space-2) var(--space-3);">BLS</td>
      <td style="padding:var(--space-2) var(--space-3); text-align:right;">1,284</td>
    </tr>
    <tr style="background:var(--bg-surface); border-bottom:1px solid var(--border-1);">
      <td style="padding:var(--space-2) var(--space-3);">Alameda Health System</td>
      <td style="padding:var(--space-2) var(--space-3);">CCT</td>
      <td style="padding:var(--space-2) var(--space-3); text-align:right;">612</td>
    </tr>
  </tbody>
</table>
```

`.bk-table th` is already 600 uppercase at 9pt, carrying `--tr-caps-small` plus the dark bonus, 0.085em on the header row above, one step below the 10.5pt cells it heads. That is deliberate and it is the one place the caps label sits below its body. A column header names a column; it is not a kicker stacked above a block of copy, which is what the never-smaller rule governs. Never restate the header inline and never push it back to 800. Set cell type once on the `<table>`, as above, rather than putting a body class on every cell and then clearing its measure. `.bk-table` cells already carry `tabular-nums lining-nums`, so number columns only need `text-align:right`. Unit IDs and authorization numbers in a cell go in `.bk-code`. A count, a duration and a median are measurements and stay Montserrat.

---

## Footer

Slim full-width rail. Hairline above, muted caption left, revision marker in Purple right.

```html
<footer style="border-top:1px solid var(--border-1); display:flex; justify-content:space-between; align-items:baseline; gap:var(--space-4); padding:var(--space-2) 0.5in;">
  <span class="bk-caption">Royal Ambulance · Document title</span>
  <span class="bk-caption bk-caps" style="color:var(--royal-purple); font-weight:600;">Rev.&nbsp;<span class="bk-code">08.26</span></span>
</footer>
```

The revision marker is a caps label, so it is 600, not 700. 700 belongs to headings, emphasis and stat numerals. `.bk-caps` carries the uppercase and the 0.080em tracking, so never type either one.

The code span needs no size of its own. `.bk-code` sets no font size, so it takes the size of the step it sits in and a revision marker inside a 9pt caption sets at 9pt, on the floor. The old 0.94em reduction landed it at 8.46pt and had to be cleared by hand at every call site.

---

## Powered by Collective Edge

Royal Ambulance is an operating company under Collective Edge. Where a Royal surface is doing something a reader might wonder about, the lockup says who built it. It is a signal, not a legal footnote.

The rule, and it is the whole rule: **the CE lockup rides beside the Royal brand, never inside it, so a hairline keeps the two marks distinct.** The two read as two brands rather than one combined mark. Nothing is merged, nested or recolored to match the other side.

The CSS is shared and identical in every kit: [`snippets/cobrand.css`](../snippets/cobrand.css). Load it after the palette.

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/cobrand.css">
```

**Dark ground.** The Royal band `--bg-band` `#2f193b`.

```html
<div class="bk-on-dark" style="background:var(--bg-band); padding:32px 0.5in;">
  <img src="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg"
       alt="Royal Ambulance" style="width:158px; height:auto; display:block;">
  <div class="ce-powered">
    <span>Powered by</span>
    <img src="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/logos/horizontal-white.svg"
         alt="CE · Collective Edge" width="204" height="34">
  </div>
</div>
```

**Light ground.** The white canvas `--bg-canvas` `#FFFFFF`, for a one-pager or report footer. Same geometry, black lockup, hairline in `--border-1`.

```html
<div class="ce-powered ce-powered-light">
  <span>Powered by</span>
  <img src="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/logos/horizontal-black.svg"
       alt="CE · Collective Edge" width="204" height="34">
</div>
```

**Text only.** Where no lockup fits, `.ce-powered-text` sets the phrase at `.bk-eyebrow` values, 12px web and 9pt print at weight 600 with 0.080em tracking. The Apex customer dashboard ships it at 9px and 700, which is under the 9pt floor and heavier than the caps-label step. Use the class.

```html
<p class="ce-powered-text">Powered by Collective Edge</p>
```

| Part | Value |
|---|---|
| Lockup width | 204px, rendering 34px tall on the 450 x 75 artwork |
| Label | `--fs-caption` 12px web and 9pt print, weight 600, `--tr-caps-small` 0.080em, uppercase |
| Label on dark | `--fg-on-dark-3` `#B0A2BC` on `#2f193b`, 6.61:1 |
| Label on light | `--fg-3` `#64748B` on `#FFFFFF`, 4.76:1 |
| Hairline on dark | 1px `--border-on-dark` `rgba(255,255,255,0.12)` |
| Hairline on light | 1px `--border-1` `#E2E8F0` |
| Spacing | 24px above the hairline and 24px below it, 12px between label and lockup |

204px is deliberate. It runs wider than the partner mark above it because it is sized to read at a glance rather than sit quietly in a corner. The 110px logo minimum in this kit is a floor, not a target.

The light lockup goes on `--bg-canvas`, not on `--royal-surface` `#faf5fd`. The same grey measures 4.43:1 on the tint, under the 4.5:1 small-text threshold.

**Where it belongs.** The footer of any Royal site or printed document. The sidebar header of any Royal dashboard. The closing slide of a deck. The foot of a report. A data page or a methodology page. Anywhere a number was computed rather than typed.

**Where it does not.** On the Royal mark itself or inside the Royal lockup. On a clinical instruction. On a patient-facing consent or safety document. Twice on one surface. Set as type where the mark fits.

---

## Assembly rules

- Space above a heading is three times the space below it. `--space-above-heading` is 48px, `--space-below-heading` is 16px.
- Every vertical value is a multiple of 4. Use the `--space-*` tokens.
- Body copy keeps its `54ch` measure. Never let it run the full width of a wide container, and never clear `max-width` on a `.bk-body*` or `.bk-caption` element to make a cell or a rail fit. Set the type on the container instead, as the table above does.
- The mono face is a whitelist of four: colour values, paths and filenames, code shown as code, and record identifiers a person dictates, the revision marker among them. Measurements, ratios, counts, ordinals, weight numbers, verdict words and labels are Montserrat.
- `.bk-code` sets no font size. It takes the size of the step it sits in, so every code string lands on the ladder and none needs a size cleared by hand.
- `.bk-code` resolves to `--font-mono`, a system stack. No kit embeds a mono face, so a `.bk-code` string falls back to whatever monospace the render host carries and does not embed in a PDF. Keep those strings short, and read them in the rendered file before you ship.
- Maximum three weights and three sizes above body in one piece.
- Content order in a one-pager: header band, optional sub-banner, body, footer. The band is not optional.
