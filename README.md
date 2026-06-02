# Royal Ambulance Brand Kit

Cloud-hosted brand assets and Claude skill for Royal Ambulance — purple-centric color palette, Montserrat typography, crown + wordmark logos, plus a `SKILL.md` that teaches Claude to apply the brand consistently to any document, slide, flowchart, or one-pager.

Anyone with this repo URL or the CDN links below can produce on-brand Royal materials from any machine, with no local setup beyond a working Claude session.

## What's in here

```
royal-brand-kit/
├── SKILL.md                 # The brand skill Claude reads
├── assets/
│   ├── colors.json          # Source of truth for hex codes
│   ├── fonts/
│   │   └── Montserrat-VariableFont_wght.ttf
│   └── logos/
│       ├── horizontal-purple.svg
│       ├── horizontal-white.svg
│       ├── crown-purple.svg
│       ├── crown-white.svg
│       ├── stacked-purple.svg
│       └── stacked-white.svg
├── snippets/
│   ├── brand-base.css       # Drop-in CSS with @font-face + variables
│   └── header-band.html     # Drop-in header markup
└── examples/
    └── eclg-ecmv-one-pager.html  # Working example using only CDN URLs
```

## CDN base URL

All assets are served via [jsDelivr](https://www.jsdelivr.com/) from the `main` branch — fast, free, and globally cached:

```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/
```

Append the path inside this repo to fetch any file. Example for the white horizontal logo:

```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg
```

## Quick start — using the brand in any HTML

Add this to the top of any HTML document and you have Montserrat plus all the brand color variables:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/brand-base.css">
```

For embedding Montserrat into a printed PDF (weasyprint, wkhtmltopdf, Chrome print-to-PDF), include the `@font-face` declaration inline so the font travels with the file. See `SKILL.md` for the snippet.

## Quick start — installing the Claude skill

So Claude automatically applies the brand whenever you ask for Royal materials, install the skill into your local Claude skills folder:

```bash
git clone https://github.com/collective-edge/royal-brand-kit ~/.claude/skills/royal-brand-guidelines
```

That's it. Claude will pick up `SKILL.md` and apply the brand standards automatically. To update, run:

```bash
cd ~/.claude/skills/royal-brand-guidelines && git pull
```

## Sharing with teammates

Send them this repo URL or paste the install command above. The CDN means generated documents (HTML, PDFs with embedded fonts) work for recipients who don't have the skill installed — the assets are fetched at render time.

## Color reference

See `assets/colors.json` for the machine-readable source of truth, or `SKILL.md` for human-readable usage rules.

| Name | Hex | Use |
|---|---|---|
| Dark Purple | `#2f193b` | Hero headers, dominant brand color |
| Purple | `#572e72` | Workhorse accent — sub-banners, callouts, buttons |
| Royal Purple | `#43205b` | Logo fill, action highlights in flowcharts |
| Light Purple | `#8260a2` | Tertiary accents only |
| Surface | `#faf5fd` | Very light background tint |

## Versioning

`@main` always serves the latest version. To pin to a stable release in production HTML, use a tag instead: `@v1.0`.

## License

Brand assets are property of Royal Ambulance. Use only for Royal Ambulance and partner-related materials.
