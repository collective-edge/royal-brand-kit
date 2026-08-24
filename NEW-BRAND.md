# Adding a brand to the house

House type system v1.0. This file is identical in every brand kit.

A new brand inherits the entire type system and supplies two things: a palette and a set of logos. Nothing about type is decided per brand. If you find yourself editing `type-system.css` for a new brand, stop, because that file is shared and the change would land on every other brand in the house.

Budget about ninety minutes, most of it spent exporting logos.

---

## What a brand kit contains

Every kit has the same eleven paths. An agent that has read one kit can navigate any of them.

| Path | Varies per brand | What it is |
|---|---|---|
| `SKILL.md` | thin | Loaded into context. Brand identity, then pointers. |
| `BRAND.md` | yes | This brand’s palette, logos and voice. Read on demand. |
| `TYPE-SYSTEM.md` | no | The type standard. Identical everywhere. |
| `brands.json` | no | Registry of every brand in the house. Identical everywhere. |
| `tokens.json` | yes | This brand’s colors, machine-readable. |
| `snippets/type-system.css` | no | The type layer. Identical everywhere. |
| `snippets/palette.css` | yes | The only stylesheet that differs. |
| `snippets/type-tokens.json` | no | Type values for non-CSS generators. Identical everywhere. |
| `snippets/header-band.html` | yes | Drop-in band, palette swapped. |
| `templates/` | yes | Document and deck, palette swapped. |
| `assets/logos/`, `assets/fonts/` | yes / no | Marks per brand. Fonts shared. |

---

## Steps

### 1. Create the repo

Name it `<brand>-brand-kit` under the `collective-edge` org, public so jsDelivr can serve it.

```
gh repo create collective-edge/<brand>-brand-kit --public
```

### 2. Copy the shared files, unchanged

From any existing kit. Do not edit any of these.

```
TYPE-SYSTEM.md
brands.json
snippets/type-system.css
snippets/type-tokens.json
NEW-BRAND.md
tools/check-sync.py
```

Fonts are not copied. Every kit loads Montserrat from the Collective Edge kit, so there is one font file in the house and one place to update it.

### 3. Write the palette

Copy `snippets/palette.css` from the closest existing brand and replace the values. The structure does not change: raw `--<prefix>-*` names first, then the semantic layer.

The semantic block is a contract. `type-system.css` styles through these names, so every one of them must be defined or text will render without color.

```
--fg-1  --fg-2  --fg-3  --fg-4  --fg-accent
--fg-on-dark-1  --fg-on-dark-2  --fg-on-dark-3
--bg-canvas  --bg-surface  --bg-elevated  --bg-inverse  --bg-band
--border-1  --border-2  --border-on-dark  --border-band-rule
```

Rules for the values:

- `--fg-1` on `--bg-canvas` must clear 4.5:1. `--fg-3` on `--bg-canvas` must clear 4.5:1 at body size.
- `--bg-band` is the dark header strip. It carries `--fg-on-dark-1` at 4.5:1 or better.
- `--border-band-rule` is the accent line under the band. Set it to `transparent` when the brand has no accent rule.
- Status and diagram colors are already in the file and are identical across the house. Leave them alone. A brand accent is never a status color.
- A bright brand color usually fails contrast as text on white. Provide a `-deep` step for text use and say so in `BRAND.md`.

### 4. Export the logos

Five roles. Name the files for the role, not for the color, so an agent can construct any path from the brand name alone.

```
assets/logos/horizontal-on-light.svg
assets/logos/horizontal-on-dark.svg
assets/logos/mark-on-light.svg
assets/logos/mark-on-dark.svg
assets/logos/stacked-on-dark.svg      (omit if the brand has none)
```

`-on-light` is the version you place **on** a light background. `-on-dark` goes on a dark one. This is the opposite of naming a file after its own ink, which is what causes an agent to pick the invisible variant.

Keep the vector master in `assets/logos/source/`.

### 5. Register the brand

Add an entry to `brands.json` under `brands`, then copy that file to every other kit so the registry stays identical everywhere. Use an existing entry as the shape. Required keys:

```
name  role  parent  skill  repo  cdnRoot  paletteCss  tokensJson
prefix  hasColor  color  colorNote  logos  minWidth
```

If Collective Edge will co-brand with this partner, also add `wedgeHue` and produce the two co-brand marks in the Collective Edge kit.

### 6. Write BRAND.md and SKILL.md

Copy both from an existing kit. `SKILL.md` stays short: identity, the two `<link>` tags, and pointers to the deeper files. Everything a reader needs only sometimes belongs in `BRAND.md`.

Do not restate the type system in either file. Point at `TYPE-SYSTEM.md`. A second copy of the rules is a second copy that will drift.

### 7. Verify

```
python3 tools/check-sync.py
```

Then, by hand:

- [ ] Every shared file is byte-identical to the Collective Edge kit.
- [ ] Every semantic variable in the contract above is defined.
- [ ] `--fg-1`, `--fg-3` and `--fg-on-dark-1` clear 4.5:1 against their grounds.
- [ ] All five logo roles resolve, and the `-on-dark` variants are legible on `--bg-band`.
- [ ] `brands.json` is identical in every kit, including the new entry.
- [ ] A rendered test page shows Montserrat, not a fallback.
- [ ] The kit is public and the CDN URLs return 200.

### 8. Tag

```
git tag v1.0 && git push --tags
```

`@main` serves the latest. Tag when the kit is stable so a consumer can pin.

---

## What never varies

Changing any of these forks the house and defeats the system.

- The typeface, the scale, the weight ladder, tracking, leading, measure.
- The fifteen rules in `TYPE-SYSTEM.md`.
- Status colors and diagram role colors.
- The `--fg-*` / `--bg-*` / `--border-*` names.
- The `.bk-*` class grammar.
- The 4px spacing base.

A brand is a palette and a set of marks. Everything else is the house.
