# Royal Ambulance brand kit · agent entry point

This repository is the brand standard for Royal Ambulance. If you were asked to make or review anything that carries this brand, do this:

1. Read [`for-agents/README.md`](for-agents/README.md). Asset URLs, logo roles, colors and the rules that get broken, on one page.
2. Read [`SKILL.md`](SKILL.md). The full standard and the pre-ship check.
3. Run the checks in `scripts/` on what you made, then render it and look.

If you were asked to change this repository itself:

- Sixteen files are shared byte for byte with the other two kits. `scripts/check-sync.py` lists them and fails when one drifts. Change a shared file in all three kits or not at all.
- Paths under `assets/`, `snippets/` and `for-humans/logos/` are fetched live from the CDN by shipped documents and sites. Add files. Do not move or rename one.
- `for-humans/logos/` and `for-humans/previews/` are built by `scripts/build-handoff.py` from `for-humans/pack.json`. Edit the list and rerun. Do not hand-export.
- Run `python3 scripts/check-sync.py` before committing. [`CONTRIBUTING.md`](CONTRIBUTING.md) covers the rest.

A person looking for logos wants [`for-humans/`](for-humans/).
