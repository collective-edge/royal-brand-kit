# Royal Ambulance · for agents

You are producing something for Royal Ambulance. This page is the shortest correct path. [`SKILL.md`](../SKILL.md) is the full standard, and it wins any disagreement with this page.

Royal Ambulance is an operating company under Collective Edge. Purple palette, the crown wordmark, the house type system.

Working for a person instead? Send them to [`for-humans/`](../for-humans/).

## 1. Load the brand

Every file is public on jsDelivr. No auth, no install.

```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/
```

HTML takes these stylesheets, in this order:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/type-system.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/palette.css">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/snippets/data-color.css">
```

`type-system.css` and `data-color.css` are served from the Collective Edge kit for every brand. `palette.css` is the only file that differs. Load `data-color.css` only when the page has a chart, a dashboard tile or a reported number.

For print or PDF, add the face inline and select it:

```css
@font-face {
  font-family: "Montserrat";
  src: url("https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.woff2") format("woff2-variations"),
       url("https://cdn.jsdelivr.net/gh/collective-edge/collective-edge-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf") format("truetype-variations");
  font-weight: 400 800;
  font-style: normal;
}
html, body { font-family: "Montserrat", "Helvetica Neue", Helvetica, Arial, sans-serif; }
```

Style through the `.bk-*` classes and the `--fg-*`, `--bg-*` and `--border-*` variables. Those names are identical in all three brands. Start from [`templates/`](../templates/) and [`snippets/header-band.html`](../snippets/header-band.html) instead of a blank page.

## 2. Get a logo by role

Ask for a role, never a filename. Filenames differ between brands. `-on-light` is the file you place on a light background.

| Role | URL | Place on |
|---|---|---|
| `horizontal-on-light` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-purple.svg` | A light background |
| `horizontal-on-dark` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg` | A dark background |
| `mark-on-light` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/crown-purple.svg` | A light background |
| `mark-on-dark` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/crown-white.svg` | A dark background |
| `stacked-on-dark` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/stacked-white.svg` | A dark background |

Embed with `<img src="...">`. Do not inline a copied SVG path, because it drifts from the master.

Transparent PNG, for generators that cannot place SVG:

| Role | URL |
|---|---|
| `horizontal-on-light` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/for-humans/logos/png/Royal-Ambulance-horizontal-purple-1200w.png` |
| `horizontal-on-dark` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/for-humans/logos/png/Royal-Ambulance-horizontal-white-1200w.png` |
| `stacked-on-light` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/for-humans/logos/png/Royal-Ambulance-stacked-purple-1200w.png` |
| `stacked-on-dark` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/for-humans/logos/png/Royal-Ambulance-stacked-white-1200w.png` |
| `mark-on-light` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/for-humans/logos/png/Royal-Ambulance-crown-purple-512w.png` |
| `mark-on-dark` | `https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/for-humans/logos/png/Royal-Ambulance-crown-white-512w.png` |

Each PNG also ships at double width. Replace the width in the filename: `1200w` to `2400w`, `512w` to `1024w`.

## 3. Color

| Name | Variable | Hex | Use |
|---|---|---|---|
| Dark Purple | `--royal-dark-purple` | `#2f193b` | Header bands, hero grounds, table header fill |
| Purple | `--royal-purple` | `#572e72` | Accent bars, callout borders, links, brand-colored text |
| Royal Purple | `--royal-royal-purple` | `#43205b` | Logo fill on light, stat numerals |
| Light Purple | `--royal-light-purple` | `#8260a2` | Tertiary accents and hover only |
| Charcoal | `--royal-charcoal` | `#1E293B` | Body text on light |
| Surface | `--royal-surface` | `#faf5fd` | Tinted rows and callout fills |

Every value, including the semantic, status and on-dark sets, as JSON:

```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/tokens.json
```

## 4. The rules that get broken

1. Light Purple `#8260a2` is never text and never a large ground.
2. Light Purple on Dark Purple measures 3.13:1 and fails at every size. On the band use `--fg-on-dark-2` `#E0D6E8` for body and `--fg-on-dark-3` `#B0A2BC` for captions.
3. White text sits only on Dark Purple, Purple or Royal Purple.
4. A partner facility color comes only from [`reference/partner-colors.md`](../reference/partner-colors.md). Never sample a logo, never guess.
5. Chart and dashboard color comes from `data-color.css`, in series order. A brand color is never a chart series.
6. Match the logo file to the background. Never recolor or invert a logo with CSS.
7. Montserrat only, weights 400 to 800. No italic, at any weight.
8. No em dashes in copy. A period, a comma, or `·`.
9. For print or PDF, inline the `@font-face` block. A locally installed font renders right on one machine and wrong everywhere else.

## 5. Not writing HTML

| Output | Read |
|---|---|
| python-pptx, python-docx, matplotlib, reportlab | `tokens.json` for color, [`snippets/type-tokens.json`](../snippets/type-tokens.json) for sizes, weights and tracking |
| A font file to embed | [`for-humans/fonts/static/`](../for-humans/fonts/static/) · Regular 400, SemiBold 600, Bold 700, ExtraBold 800 |
| A raster logo | The PNG table above |
| A chart | [`reference/data-color.md`](../reference/data-color.md). The hex values are in `snippets/data-color.css` |

Twenty photographs with a manifest are in [`for-humans/photos/`](../for-humans/photos/). Use them unfiltered.

## 6. Read next, by task

| Making | Read |
|---|---|
| Anything | [`SKILL.md`](../SKILL.md), start to finish. It ends with the pre-ship check |
| A header band, table, stat callout, flowchart, footer | [`reference/layout.md`](../reference/layout.md) |
| A chart, dashboard or scorecard | [`reference/data-color.md`](../reference/data-color.md) |
| Buttons, inputs, product UI | [`reference/ui.md`](../reference/ui.md) |
| Long-form type decisions | [`reference/type-system.md`](../reference/type-system.md) |
| A contrast or logo question | [`reference/brand.md`](../reference/brand.md) |
| A partner facility is named on the page | [`reference/partner-colors.md`](../reference/partner-colors.md) |

## 7. Verify before you report done

```bash
python3 scripts/validate.py path/to/output.html
python3 scripts/ui-audit.py path/to/output.html
python3 scripts/validate-palette.py --series
```

`validate.py` exits non-zero on a mechanical rule violation. None of the scripts can see overlap, clipping or a fallback font. Render the file and look at it. If you cannot render, say so instead of reporting it clean.

## 8. Install as a skill

Clone the kit into the skills directory your agent reads. The path differs by tool.

```bash
git clone https://github.com/collective-edge/royal-brand-kit ~/skills/royal-brand-guidelines
```

`SKILL.md` at the root carries the frontmatter. `git pull` updates it.

## 9. The other brands

One registry resolves every brand in the house to its CDN root, palette, tokens and logo roles. It is identical in all three kits.

```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/brands.json
```

| Brand | Kit | Entry point |
|---|---|---|
| Apex Paramedics | [`apex-brand-kit`](https://github.com/collective-edge/apex-brand-kit) | [for agents](https://github.com/collective-edge/apex-brand-kit/tree/main/for-agents) |
| Collective Edge | [`collective-edge-brand-kit`](https://github.com/collective-edge/collective-edge-brand-kit) | [for agents](https://github.com/collective-edge/collective-edge-brand-kit/tree/main/for-agents) |
