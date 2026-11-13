# Royal Ambulance brand kit · agent entry point

This repository is the brand standard for Royal Ambulance. It is public. Shipped documents and sites fetch its files live from `main`.

## Making or reviewing something that carries this brand

1. Read [`for-agents/README.md`](for-agents/README.md). Fonts, logos by role, color, and the memo, one-pager and deck specifications in inches, points and hex, on one page.
2. Read [`SKILL.md`](SKILL.md). The full standard and the pre-ship check.
3. For a report, a slide layout, or a Word, PowerPoint or Google build, read [`reference/layout.md`](reference/layout.md). [`documents.json`](documents.json) holds the same values as data.
4. Run the check in `for-agents/README.md` section 7 on the finished file. If you could not render it, say so.

## Changing this repository

1. **Shared files.** Seventeen files are identical byte for byte in the three kits. `scripts/check-sync.py` lists them and fails when one drifts. Edit a shared file in `collective-edge-brand-kit`, copy it to the other two, and run `python3 scripts/check-sync.py` in all three.
2. **Live paths.** `brands.json`, `tokens.json`, `documents.json`, `SKILL.md`, `for-agents/README.md`, `reference/layout.md`, `reference/data-color.md` and everything under `assets/`, `snippets/`, `for-humans/logos/` and `for-humans/fonts/` are fetched by URL. Add files. Never move, rename or delete one.
3. **Generated files.** `for-humans/logos/` and `for-humans/previews/` are built by `scripts/build-handoff.py` from `for-humans/pack.json`. `index.html` is built by `guidelines/build.py` from the kit's data files and `guidelines/page.json`. Edit the source and rerun. Never edit the output by hand.

The rules, the sections and the wording are the same in all three kits. Only color, logo and brand facts differ. [`CONTRIBUTING.md`](CONTRIBUTING.md) covers the rest. Do not push to `main` until the checks pass.

## People

A person who wants a logo, a font or a color goes to [`for-humans/`](for-humans/). The guidelines page is [`index.html`](index.html), served at `https://collective-edge.github.io/royal-brand-kit/`.
