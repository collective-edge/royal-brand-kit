# Contributing to the Royal Ambulance brand kit

This repository is public and live. Shipped documents and sites fetch its files from the CDN at render time, so a change here shows up in work that is already out the door.

## Three rules

1. **Add files. Do not move or rename one.** Paths under `assets/`, `snippets/` and `for-humans/logos/` are public URLs.
2. **Shared files change in all three kits or not at all.** Sixteen files are byte for byte identical across `collective-edge-brand-kit`, `apex-brand-kit` and `royal-brand-kit`. `scripts/check-sync.py` fails when one drifts.
3. **Nothing reaches `main` until the checks pass.** `main` is the branch the CDN serves.

## The shared files

```
reference/type-system.md
reference/ui.md
reference/data-color.md
NEW-BRAND.md
brands.json
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

## Check

```bash
python3 scripts/check-sync.py
python3 scripts/validate.py $(find snippets templates Examples for-humans -name '*.html' ! -name '*.before.html' ! -name 'data-color-sheet.html' ! -name '_audit-fixture.html')
python3 scripts/validate-palette.py --series
```

`check-sync.py` proves the shared files have not forked and that `snippets/palette.css` still defines every variable in the semantic contract. `validate.py` checks generated HTML against the mechanical type rules and fails on retired logo artwork. Neither can see a rendered page. Open the file and look.

A `*.before.html` file in `Examples/` is the pre-v1.0 original kept for comparison. It fails the validator by design. Do not run the validator over it and do not correct it.

## Change a logo or a color

The PNG logos, the previews and the color chips in `for-humans/` are rendered, not hand-exported.

```bash
python3 scripts/build-handoff.py
```

It reads `for-humans/pack.json`. Edit the list, rerun, commit the output. It needs Chrome or Chromium and Pillow.

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

## Version

Production material pins a tag in place of `@main`.

```bash
git tag v1.4
git push --tags
```

Bump the minor version for an additive change. Bump the major version when a palette value or a mark changes.

## Add a brand

[`NEW-BRAND.md`](NEW-BRAND.md) covers standing up a kit for a new operating company.
