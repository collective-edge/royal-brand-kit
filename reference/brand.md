# Royal Ambulance · brand reference

Everything about this brand that does not fit in `SKILL.md`. Color, logo, voice, sources. Type is not decided here. Read `type-system.md`.

Royal Ambulance is an operating company under Collective Edge. It inherits the house type system unchanged and supplies two things of its own: a purple palette and the crown wordmark.

---

## 1. Full color table

| Name | CSS | Hex | RGB | Usage |
|---|---|---|---|---|
| Dark Purple | `--royal-dark-purple` | `#2f193b` | 47, 25, 59 | Dominant brand color. Header bands, hero backgrounds, section dividers, full-width bands, table header fill. |
| Purple | `--royal-purple` | `#572e72` | 87, 46, 114 | Workhorse accent. Column headers, accent bars, callout borders, contact labels, category badges, label chips, buttons, links, brand-colored text on white. |
| Light Purple | `--royal-light-purple` | `#8260a2` | 130, 96, 162 | Tertiary accents and hover states only. |
| Royal Purple | `--royal-royal-purple` | `#43205b` | 67, 32, 91 | Logo fill on light. Alternate dark accent. Action and highlight nodes in flowcharts. |
| Black | `--royal-black` | `#000000` | 0, 0, 0 | Maximum-contrast headings on white. |
| White | `--royal-white` | `#FFFFFF` | 255, 255, 255 | Page background. Text on any dark purple ground. |

### Neutrals

| Name | CSS | Hex | RGB | Usage |
|---|---|---|---|---|
| Charcoal | `--royal-charcoal` | `#1E293B` | 30, 41, 59 | Primary body text on light. This is `--fg-1`. |
| Muted | `--royal-muted` | `#64748B` | 100, 116, 139 | Secondary and tertiary text, captions, legends, footer left rail, stat unit labels. |
| Hairline | `--royal-hairline` | `#E2E8F0` | 226, 232, 240 | Table rules, card borders, footer top border. |
| Surface | `--royal-surface` | `#faf5fd` | 250, 245, 253 | Very light purple tint. Alternating table rows, callout fills. |

`#f8f4fc` is the one sanctioned alternate tint when a second surface value is genuinely needed. Nothing stronger than these two is a background tint.

### Semantic layer

Style through these names. They are identical in every brand, so a component written for Royal renders correctly for Apex with only `palette.css` swapped.

| Variable | Resolves to | Job |
|---|---|---|
| `--fg-1` | `#1E293B` | Primary text on light |
| `--fg-2` | `#64748B` | Secondary text |
| `--fg-3` | `#64748B` | Tertiary text, metadata, captions, eyebrows |
| `--fg-4` | `#94A3B8` | Dimmed labels |
| `--fg-accent` | `#572e72` | Brand-colored text |
| `--fg-on-dark-1` | `#FFFFFF` | Primary text on dark |
| `--fg-on-dark-2` | `#E0D6E8` | Body text on dark |
| `--fg-on-dark-3` | `#B0A2BC` | Captions and eyebrows on dark |
| `--bg-canvas` | `#FFFFFF` | Page |
| `--bg-surface` | `#faf5fd` | Tinted surface |
| `--bg-elevated` | `#FFFFFF` | Cards |
| `--bg-inverse` | `#2f193b` | Inverted panels |
| `--bg-band` | `#2f193b` | Header and hero bands |
| `--border-1` | `#E2E8F0` | Hairline |
| `--border-2` | `#CBD5E1` | Stronger rule |
| `--border-on-dark` | `rgba(255,255,255,0.12)` | Rule on dark |
| `--border-band-rule` | `transparent` | Royal runs no accent rule under the band |

### Status colors

Identical in every brand so an operational signal never changes meaning between documents. A brand accent is never a status color.

| Role | CSS | Hex |
|---|---|---|
| Go | `--status-go` | `#1E7A4D` |
| Warn | `--status-warn` | `#B5821A` |
| Stop | `--status-stop` | `#B0322B` |
| Info | `--status-info` | `#2A5A8C` |

`--status-warn` `#B5821A` measures 3.40:1 on `#FFFFFF`. Use it large or bold only. Never set running copy in it. Carry a warning at body size with a `#B5821A` rule, chip border or icon and keep the text at `--fg-1`.

### Diagram roles

Not primary brand colors. Official house conventions for flowcharts, dashboards and process docs where a role is needed beyond purple. Identical across every brand. Never invent a hue for a role.

| Role | Fill | Border | Use |
|---|---|---|---|
| Decision | `#4a8e3a` | `#3a7029` | Decision boxes, questions, branch points |
| Warning | `#f57c00` | `#cc6600` | Warnings, advisories, watch-out pills |
| Process | `#3e3e3e` | `#2a2a2a` | Neutral process steps, context boxes |
| Action | `#43205b` | `#2f193b` | Royal highlight step |

Connector stroke `#3e3e3e`, 1.8pt, arrow markers. Every node is a rectangle at 6px radius. Color does the differentiation work. Role is communicated by fill, never by shape.

Measured contrast on these fills: `#FFFFFF` on `#4a8e3a` is 4.02:1, large or bold only. `#FFFFFF` on `#f57c00` is 2.70:1, which fails at every size. Do not describe either combination as legible at label sizes. Both fills and their white text are inherited from the pre-v1.0 kits and are frozen pending a decision from the brand owner, so do not change them here. Where you need a warning that reads at caption size, carry the role with a `#f57c00` border on `--bg-canvas` and `--fg-1` text instead of a `#f57c00` fill.

---

## 2. Extended color rules

- Dark Purple `#2f193b` carries the top of the page. Every Royal document opens on it.
- Purple `#572e72` does the accent work everywhere else. It is the only purple that may be body-size text on white.
- Light Purple `#8260a2` is **never body text**. It measures 5.07:1 on `#FFFFFF`, which clears AA at text sizes and fails AAA, and against the 14.63:1 of `--fg-1` it reads washed out on the page. It is **never a large background** either. It is a tertiary accent and a hover state.
- Light Purple on Dark Purple is a contrast trap. `#8260a2` on `#2f193b` measures 3.13:1 and fails at every size. Do not put `#8260a2` on `#2f193b`. On a dark ground use `--fg-on-dark-2` `#E0D6E8` or `--fg-on-dark-3` `#B0A2BC`.
- White text belongs only on Dark Purple, Purple or Royal Purple. Never white on Light Purple.
- Black `#000000` is for maximum-contrast headings. Running body text is `--fg-1` `#1E293B`.
- Backgrounds are white first. Tints stop at `#faf5fd` and `#f8f4fc`.
- No off-brand hues for decoration. Functional colors stay in the status and diagram sets above.
- Chart series stay inside the purple ramp: `#2f193b`, `#43205b`, `#572e72`, `#8260a2`. Reach outside it only for a status meaning, and then use the status colors.

---

## 3. Logo

### Roles and files

| Role | File | Placed on |
|---|---|---|
| horizontal-on-light | `assets/logos/horizontal-purple.svg` | White and light grounds |
| horizontal-on-dark | `assets/logos/horizontal-white.svg` | Dark purple grounds |
| mark-on-light | `assets/logos/crown-purple.svg` | White and light grounds |
| mark-on-dark | `assets/logos/crown-white.svg` | Dark purple grounds |
| stacked-on-dark | `assets/logos/stacked-white.svg` | Dark grounds, portrait and square formats |

Ask for a role, never for a filename. `-on-light` is the version you place **on** a light background.

These five roles are the whole contract. `brands.json` maps exactly these five for every brand, so a role name that is not in this table resolves to nothing. `assets/logos/stacked-purple.svg` ships in this repo, viewBox `0 0 526.66 418.93`, but no role points at it. Reference it by path when a portrait lockup on a light ground is unavoidable, and do not ask for it by role.

- **Horizontal** is the primary lockup and the default anywhere with horizontal room.
- **Crown** is the icon-only mark, for favicons, badges, social avatars and table corners.
- **Stacked** is the vertical lockup for portrait orientations and tight squares.

### Specifications

| Property | Value |
|---|---|
| Horizontal viewBox | `0 0 735.76 179.54` |
| Crown viewBox | `0 0 692.1 692.1` |
| Stacked viewBox | `0 0 526.66 418.93` |
| Fill on light | `#43205b` in every lockup. **`assets/logos/crown-purple.svg` declares `#3c2157` instead. Unresolved: the mark has not been recolored, because that is an owner decision.** |
| Fill on dark | `#FFFFFF` |
| Clear space | Padding on all four sides equal to the height of the crown mark |
| Minimum size, horizontal | 110px on screen, 1 inch in print |
| Minimum size, crown | 32px on screen |
| Band size, horizontal | 1.4in to 1.8in wide in a one-pager header band |
| Embedding | `<img src="{CDN}assets/logos/…">` direct. Public CDN, no auth. |

### Do not

- Stretch, skew or rotate the logo.
- Recolor it with a CSS filter. Pick the file for the ground.
- Change the color to anything but Royal Purple `#43205b` or white.
- Add a drop shadow, glow, outline or gradient.
- Separate the crown from the wordmark in the horizontal lockup.
- Place it on a busy photograph without a solid backing panel.
- Render it below the minimum sizes above.

### Source

The shipping SVGs in `assets/logos/` are the working masters. Any future vector master belongs in `assets/logos/source/`, which Royal has not populated. Royal’s `brands.json` entry carries no `logoSource` key for that reason.

---

## 4. Voice and content

- Write for the reader who is between calls. Short declarative sentences, active verbs, no throat-clearing.
- No em dashes. Use a period, a comma or `·`.
- A label, a value, and nothing between them. No helper text under a field, no caption restating the number above it, no parenthetical after a heading.
- Sentence case for headings inside a document. Uppercase for display statements on a title, band or divider surface, and for labels. Always tracked, never past four words.
- Name partners and facilities exactly as they write themselves.
- Unit IDs, run numbers, authorization numbers, policy numbers and MRNs go in the mono face with `.bk-code`.
- When you hand work back, state which brand choices you applied: logo role, accent, how the font embedded.

---

## 5. Sources and versioning

| What | Path |
|---|---|
| CDN root | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/` |
| Repo | `collective-edge/royal-brand-kit` |
| Palette, authoritative | `snippets/palette.css` |
| Color tokens, machine-readable | `tokens.json` |
| Type values, machine-readable | `snippets/type-tokens.json` |
| Registry of every brand | `brands.json` |

`@main` serves the latest. Pin to a tag for stability: replace `@main` with `@v1.0`. Bump the major version when a palette value or a mark changes.

### Deprecated, still served

`snippets/brand-base.css`, `assets/colors.json` and the Royal-hosted Montserrat TTF predate v1.0. They stay on the CDN because documents already point at them. New work never loads them.

| Deprecated | Address | Replaced by |
|---|---|---|
| Base CSS | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/brand-base.css` | `type-system.css` plus `palette.css` |
| Colors JSON | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/colors.json` | `tokens.json` |
| Montserrat variable TTF | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf` | the Collective Edge copy, woff2 first, TTF second |

The Royal-hosted TTF still ships in `assets/fonts/` and still resolves. Every new `@font-face` points at the Collective Edge kit instead, so one font file serves all three brands:

```
https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.woff2
https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf
```

The drop-in `<link>` a pre-v1.0 document carries is still live:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/brand-base.css">
```

It now forwards to `type-system.css` and `palette.css` and keeps the old `--royal-*` names resolving, so an old document picks up the corrected type without being edited.
