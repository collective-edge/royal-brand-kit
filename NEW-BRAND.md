# Adding a brand to the house

This file is identical in every brand kit.

A new brand supplies three things: a palette, a set of logos and its brand facts. Everything else is the house and is shared: type, layout, the neutrals, the alert family, chart color, the UI controls and the co-brand lockup. If you find yourself editing a shared file for the new brand, stop. That change lands on every brand in the house.

Every kit says the same thing in the same order in the same words. Only color, logo and brand facts differ.

---

## What a brand kit contains

Every kit has the same file set. A reader who knows one kit knows all of them.

| Path | Per brand | What it is |
|---|---|---|
| `AGENTS.md` | Yes | Entry point for an agent |
| `README.md`, `CONTRIBUTING.md` | Yes | Entry point for a person, and how to change the kit |
| `SKILL.md` | Brand facts only | The standard in brief. Same sections, same order and same shared wording in every kit |
| `for-agents/README.md` | Brand facts only | The shortest correct path for an agent |
| `for-humans/` | Yes | Logos as SVG and PNG, static fonts, previews. Built from `for-humans/pack.json` |
| `reference/brand.md` | Brand facts only | Full color tables, contrast, logo specifications, co-brand, voice |
| `reference/layout.md` | Brand facts only | The working document, the sheet, the deck, the one-pager, the report and the memo |
| `reference/type-system.md` | No | The type standard |
| `reference/data-color.md` | No | Chart color |
| `reference/ui.md` | No | Buttons, links and form controls |
| `brands.json` | No | Registry of every brand in the house |
| `tokens.json` | Values only | This brand’s colors as data. One key structure in every kit |
| `snippets/palette.css` | Yes | The only stylesheet that differs by brand |
| `snippets/type-system.css`, `snippets/type-tokens.json` | No | The type layer, as CSS and as data |
| `snippets/cobrand.css`, `snippets/ui.css`, `snippets/data-color.css` | No | The co-brand lockup, the controls, the data layer |
| `snippets/header-band.html`, `templates/` | Yes | The band and the document templates, with this brand’s root and logo |
| `Examples/ui-controls.html`, `Examples/data-color.html` | No | Every control and every data color, rendered |
| `scripts/validate.py`, `scripts/validate-palette.py`, `scripts/check-sync.py`, `scripts/ui-audit.py` | No | The checks |
| `scripts/build-handoff.py` | Yes | Renders `for-humans/` from `pack.json` |
| `assets/logos/` | Yes | The marks, as SVG |

Fonts are not copied. Every kit loads Montserrat from the Collective Edge kit, so there is one font file in the house and one place to update it.

---

## Steps

### 1. Create the repo

Name it `<brand>-brand-kit` under the `collective-edge` org. Make it public so jsDelivr can serve it.

```
gh repo create collective-edge/<brand>-brand-kit --public
```

### 2. Copy the shared files, unchanged

Seventeen files, byte for byte, from the Collective Edge kit. Do not edit any of them.

```
reference/type-system.md
reference/ui.md
reference/data-color.md
NEW-BRAND.md
brands.json
documents.json
snippets/type-system.css
snippets/type-tokens.json
snippets/cobrand.css
snippets/ui.css
snippets/data-color.css
Examples/ui-controls.html
Examples/data-color.html
scripts/validate.py
scripts/validate-palette.py
scripts/check-sync.py
scripts/ui-audit.py
```

`scripts/check-sync.py` holds this list as `SHARED_FILES` and fails when one drifts.

### 3. Write the palette

Copy `snippets/palette.css` from the closest existing brand. Keep the structure. Replace the brand values only.

| Block | Change it |
|---|---|
| `--neutral-*` | No. One neutral family sets text, rules and on-dark text in every brand |
| `--<prefix>-*` | Yes. The brand’s own colors |
| `--fg-*`, `--bg-*`, `--border-*` | Point them at the brand colors and the neutrals |
| `--alert-*` | No. Go, warn, stop and info, each with base, text, tint, text on tint and on dark |
| `--status-*`, `--diagram-*` | No. Aliases of the alert and neutral families |
| `--brand-seq-100` to `-700`, `--brand-seq-dark-100` to `-700` | Yes. The sequential ramp in the brand’s hue |
| Radii, shadow, motion | No |

The semantic block is a contract. `type-system.css`, `ui.css` and `data-color.css` style through these names, and `scripts/check-sync.py` fails when one is missing.

```
--fg-1  --fg-2  --fg-3  --fg-4  --fg-accent
--fg-on-dark-1  --fg-on-dark-2  --fg-on-dark-3
--bg-canvas  --bg-surface  --bg-surface-2  --bg-elevated  --bg-mid  --bg-inverse  --bg-band
--border-1  --border-2  --border-on-dark  --border-band-rule
```

Rules for the values:

1. Text and rules are the shared neutrals. `--fg-1` to `--fg-4`, `--fg-on-dark-2`, `--fg-on-dark-3`, `--border-1` and `--border-2` point at `--neutral-*`. A brand does not bring its own gray.
2. `--fg-accent` is the brand-colored text. It clears 4.5:1 on `#FFFFFF` and on `--bg-surface`.
3. Every brand has the same six grounds: `--bg-canvas`, `--bg-surface`, `--bg-surface-2`, `--bg-mid`, `--bg-band` and `--bg-inverse`. `--bg-canvas` is `#FFFFFF`.
4. `--bg-surface` is the brand’s lightest tint. `--fg-3` `#6D6D77` clears 4.5:1 on it.
5. `--bg-surface-2` is the stronger tint. For a brand with a hue it is step 100 of the ramp. `--fg-2` `#565860` clears 4.5:1 on it.
6. `--bg-mid` is a filled block. `#FFFFFF` and `--fg-on-dark-2` `#DDDDE3` clear 4.5:1 on it.
7. `--bg-band` is the header band. `#FFFFFF`, `#DDDDE3` and `--fg-on-dark-3` `#A3A4AC` clear 4.5:1 on it. So do the four alert on-dark steps: `#56B580`, `#E9B457`, `#EB685C` and `#5796D9`. If one fails, change the band, never the alert family.
8. `--border-band-rule` is the rule under the band. Set it to `transparent` when the brand runs none.
9. The ramp runs light to dark in the brand’s hue and lands on `--fg-accent` at step 700. A brand with no hue takes the neutral ramp and lands on `--fg-1`. Check it with `python3 scripts/validate-palette.py --ordinal "<seven hex values, comma separated>"`.
10. A bright brand color usually fails as text on white. Provide a `-deep` step for text and say so in `reference/brand.md`.
11. A brand color is never a status color and never a chart series. Green means good and nothing else.

### 4. Write tokens.json

Copy `tokens.json` from an existing kit and replace the values. The keys do not change. `scripts/check-sync.py` compares the key structure across kits and fails when it drifts.

| Key | Holds |
|---|---|
| `brand`, `name`, `role`, `parent`, `prefix`, `hasColor`, `version`, `typeSystemVersion`, `cdnRoot`, `paletteCss`, `dataColorCss`, `typeTokensJson`, `colorNote` | Identity |
| `raw` | A list of the brand’s own colors, each with `key`, `var`, `hex`, `rgb`, `pantone` and `use` |
| `neutral` | The shared neutral family. Copy unchanged |
| `foreground`, `background`, `border` | The semantic layer, each entry with `var`, `value`, `hex`, `rgb`, `alpha` and `use` |
| `tiers` | The six grounds from darkest to lightest, plus `tableHeader` and `focusRing` |
| `alert`, `status`, `diagramRoles` | The alert family and its aliases. Copy unchanged. `diagramRoles.brandRoles` is an empty list unless the brand adds a role |
| `data` | Chart color. Copy unchanged, then replace `sequential` with the brand ramp |
| `logos` | Every role, `null` where the brand ships no file, then `minWidth`, `minWidthPrint`, `viewBox`, `aspect`, `fill`, `clearSpace`, `source` and `notes` |
| `cobrandMarks` | An empty list outside the Collective Edge kit |
| `type`, `radius`, `shadow`, `motion` | Copy unchanged |

A value the brand does not have is `null`. A list may be empty. An object never drops a key. Every hex mirrors `snippets/palette.css`. If the two disagree, `palette.css` wins.

### 5. Export the logos

Name each file for its role, not for its ink, so an agent can build any path from the brand name alone. `-on-light` is the file placed on a light background. `-on-dark` is the file placed on a dark one.

| Role | Required |
|---|---|
| `horizontal-on-light`, `horizontal-on-dark` | Yes. The primary lockup |
| `mark-on-light`, `mark-on-dark` | Yes. The icon |
| `compact-on-light`, `compact-on-dark` | Only where the brand has a short lockup |
| `stacked-on-light`, `stacked-on-dark` | Only where the brand has a vertical lockup |
| `app-icon` | Only where the brand has one |

```
assets/logos/horizontal-on-light.svg
assets/logos/horizontal-on-dark.svg
assets/logos/mark-on-light.svg
assets/logos/mark-on-dark.svg
```

Keep the vector master in `assets/logos/source/`. A mark is a whole mark: no fragment of a logo ships as a file of its own.

List every logo in `for-humans/pack.json`, then render the PNG files and the previews. Lockups render at 1200 and 2400 pixels wide, marks at 512 and 1024.

```
python3 scripts/build-handoff.py
```

State three facts for the logo and put them in `tokens.json`, `brands.json` and `reference/brand.md`: the minimum width of each lockup on screen in pixels, the minimum width in print in inches, and the unit of clear space.

### 6. Register the brand

Add an entry to `brands.json` under `brands`, then copy the file to every kit so the registry stays identical. Use an existing entry as the shape.

```
name  role  parent  skill  repo  cdnRoot  paletteCss  tokensJson
prefix  hasColor  color  colorNote  logos  minWidth
```

Add the new kit’s folder name to `SISTER_KITS` in `scripts/check-sync.py`, and copy that file to every kit too.

Every operating company carries “Powered by Collective Edge” once, small, on every PDF, deck and image, and never on a working document or a sheet. The Edge wedge takes its color. So also:

1. Add `wedgeHue` to the brand’s entry.
2. Draw the two co-brand marks in the Collective Edge kit: `assets/logos/mark-black-<brand>.svg` and `assets/logos/mark-white-<brand>.svg`.
3. Add them to `cobrandMarks` in the Collective Edge entry of `brands.json` and in the Collective Edge `tokens.json`.
4. Add `--wedge-<brand>` to the Collective Edge `snippets/palette.css`.

### 7. Write the brand files

Copy these from an existing operating-company kit:

```
SKILL.md
reference/brand.md
reference/layout.md
for-agents/README.md
AGENTS.md
README.md
CONTRIBUTING.md
snippets/header-band.html
templates/
```

Keep every heading, the order, the numbering and every shared sentence. Change only the brand rows and the brand facts: names, hex values, logo files, minimum sizes, the clear-space unit and the voice. Then diff each file against the kit you copied from. Every differing line must be a brand fact.

Do not restate the type system in a brand file beyond what the source kit states. Point at `reference/type-system.md`. A second copy of a rule is a second copy that drifts.

### 8. Verify

```
python3 scripts/check-sync.py
python3 scripts/validate.py $(find snippets templates Examples for-humans -name '*.html' ! -name 'data-color-sheet.html' ! -name '_audit-fixture.html')
python3 scripts/validate-palette.py --series
```

Then, by hand:

- [ ] Every shared file is byte-identical to the Collective Edge kit.
- [ ] Every name in the semantic contract is defined in `snippets/palette.css`.
- [ ] `tokens.json` has the same key structure as the other kits, and every hex matches `palette.css`.
- [ ] The contrast rules in step 3 hold, measured.
- [ ] Every logo role in `tokens.json` resolves to a file or is `null`, and each `-on-dark` file is legible on `--bg-band`.
- [ ] `brands.json` is identical in every kit, including the new entry.
- [ ] `SKILL.md`, `reference/brand.md`, `reference/layout.md` and `for-agents/README.md` differ from the source kit only in brand facts.
- [ ] A rendered working document, one-pager and deck show Montserrat, not a fallback.
- [ ] The kit is public and the CDN URLs return 200.

### 9. Tag

```
git tag v1.0 && git push --tags
```

`@main` serves the latest. Tag when the kit is stable so a consumer can pin.

---

## What never varies

Changing any of these forks the house.

- The typeface, the scale, the weight ladder, tracking, leading and measure.
- The fifteen rules in `reference/type-system.md`.
- The layout of the working document, the sheet, the deck, the one-pager, the report and the memo: margins, sizes and what goes where.
- The neutral family, the alert family and the diagram roles.
- The chart colors. The sequential ramp is the one value that follows the brand.
- The `--fg-*`, `--bg-*` and `--border-*` names, and the six grounds.
- The `.bk-*` class grammar and the 4px spacing base.
- The key structure of `tokens.json`.
- The “Powered by Collective Edge” lockup.

A brand is a palette, a set of marks and its facts. Everything else is the house.
