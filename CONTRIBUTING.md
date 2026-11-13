# Contributing to the Royal Ambulance brand kit

This repository is public and live. `main` is what readers see, what the CDN serves and what the agent fetches on every document request. A change on `main` shows up in work that is already out the door, so changes land whole.

## Three rules

1. **Add files. Do not move or rename one.** Paths under `assets/`, `snippets/`, `for-humans/logos/` and `for-humans/fonts/` are public URLs. So are `brands.json`, `documents.json`, `tokens.json`, `SKILL.md`, `for-agents/README.md`, `reference/layout.md` and `reference/data-color.md`, which the agent fetches by path.
2. **Shared files change in all three kits or not at all.** Seventeen files are byte for byte identical across `collective-edge-brand-kit`, `apex-brand-kit` and `royal-brand-kit`. `scripts/check-sync.py` fails when one drifts.
3. **Nothing reaches `main` until the checks pass.** `main` is the branch the CDN serves.

## The shared files

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

Edit a shared file in the Collective Edge kit, copy it into the other two, then run `check-sync.py` in all three.

`guidelines/build.py` and `guidelines/manual.css` are also identical in the three kits. `check-sync.py` does not check them yet. Copy them the same way.

The files that are not shared carry the same sections, in the same order, with the same wording. Only color, logo and brand facts differ. When a shared rule changes in `README.md`, `SKILL.md`, `for-agents/README.md`, `for-humans/README.md`, `reference/brand.md` or `reference/layout.md`, change it in all three kits and diff them. Brand facts stay in their own kit: the background texture and the hero treatment are in the Collective Edge kit only, the partner facility colors and the photographs in the Royal Ambulance kit only.

## Land a change whole

The agent reads `brands.json`, `for-agents/README.md`, `SKILL.md`, `reference/layout.md`, `reference/data-color.md`, `documents.json`, `tokens.json`, `snippets/type-tokens.json` and the logo files, live from `main`. It builds what they say.

- A value lives in more than one file. A color is in `snippets/palette.css`, `tokens.json`, the guides and the color chips. A layout value is in `reference/layout.md`, `documents.json` and the templates. Change every copy in one merge.
- Rebuild what is built: the guidelines page and the human pack. Both are below.
- Merge the three kits together when the change touches a shared file or a shared rule.

## Check

```bash
python3 scripts/check-sync.py
python3 scripts/validate.py index.html $(find snippets templates Examples for-humans -name '*.html' ! -name '*.before.html' ! -name 'data-color-sheet.html' ! -name '_audit-fixture.html')
python3 scripts/validate-palette.py --series
python3 guidelines/build.py --check
```

`check-sync.py` proves the shared files have not forked, that `snippets/palette.css` still defines every variable in the semantic contract, that the type tokens match the type stylesheet and that `tokens.json` has the same keys in every kit. `validate.py` checks generated HTML against type rules 1, 2, 5, 9, 10, 13 and 14 and check L1, retired logo artwork. `build.py --check` builds the guidelines page without writing it and fails on a value the kit does not ship. None of them can see a rendered page. Open the file and look.

A `*.before.html` file in `Examples/` is the pre-v1.0 original kept for comparison. It fails the validator by design. Do not run the validator over it and do not correct it.

## Rebuild the guidelines page

`index.html` at the repository root is the brand guidelines page. It is built, not hand-edited.

```bash
python3 guidelines/build.py
python3 guidelines/build.py --og
```

It reads `brands.json`, `tokens.json`, `snippets/type-tokens.json`, the snippet stylesheets, `for-humans/pack.json` and `guidelines/page.json`, and writes `index.html`. Brand copy is in `guidelines/page.json`. Every hex, token name, size and URL comes from the kit's data files. The page marks every code, hex and size with the class `bk-code` and sets it in Montserrat, so `validate.py` passes rule 13 on the class, not on the face. `--og` also renders `guidelines/og.png`, the 1200 x 630 preview image, and needs Chrome or Chromium. Run it after any change to a color, a logo, the type tokens or the brand copy.

## Rebuild the human pack

The PNG logos, the previews and the color chips in `for-humans/` are rendered, not hand-exported.

```bash
python3 scripts/build-handoff.py
python3 scripts/build-handoff.py --only swatches
```

It reads `for-humans/pack.json`. Edit the list, rerun, commit the output. `--only` takes `logos`, `swatches`, `data` or `fonts`. It needs Chrome or Chromium and Pillow. The prose in `for-humans/README.md` is written by hand and follows the same outline in all three kits.

## Publish

Work lands on a branch and merges to `main`.

```bash
git checkout -b describe-the-change
git commit -am "Describe what changed"
git push -u origin HEAD
```

Open a pull request, or fast-forward `main` once the checks pass.

jsDelivr caches an `@main` path for up to twelve hours. To serve a change at once, purge the path:

```
https://purge.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/palette.css
```

The guidelines page is served by GitHub Pages from `main` at the repository root: https://collective-edge.github.io/royal-brand-kit/

## Version

Production material pins a tag in place of `@main`.

```bash
git tag vX.Y
git push --tags
```

Bump the minor version for an additive change. Bump the major version when a palette value or a mark changes.

## Add a brand

[`NEW-BRAND.md`](NEW-BRAND.md) covers standing up a kit for a new operating company.
