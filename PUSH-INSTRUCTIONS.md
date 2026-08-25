# Push this kit

The repo exists at **https://github.com/collective-edge/royal-brand-kit** and is public, which is what jsDelivr requires. `main` is the branch the CDN serves. Work lands on a branch and merges into `main`.

Local path:

```
/Users/jacob.sarasohn/collective-edge/royal-brand-kit
```

## Step 1. Verify before you push

Both scripts must pass. Nothing goes to `main` until they do.

```bash
cd /Users/jacob.sarasohn/collective-edge/royal-brand-kit
python3 scripts/check-sync.py
python3 scripts/validate.py snippets/*.html templates/*.html \
  $(ls Examples/*.html | grep -v '\.before\.html$')
```

`check-sync.py` proves `reference/type-system.md`, `NEW-BRAND.md`, `brands.json`, `snippets/type-system.css`, `snippets/type-tokens.json`, `scripts/validate.py` and `scripts/check-sync.py` are still byte-identical to the Collective Edge kit, and that `palette.css` still defines all 17 contract variables. It exits non-zero the moment one forks.

`validate.py` checks rules 1, 2, 5, 9, 10, 13 and 14 against every shipping HTML file and exits non-zero on a violation. The `grep -v` skips `*.before.html`, the pre-v1.0 originals, which fail by design.

If `check-sync.py` reports a shared file out of sync, fix it in every kit and resync. Never edit a shared file in this repo alone.

## Step 2. Commit and push the branch

```bash
git add .
git commit -m "Describe what changed"
git push -u origin type-system-v1
```

## Step 3. Merge to main

The CDN serves `main`. Open a pull request or fast-forward locally:

```bash
git checkout main
git merge --ff-only type-system-v1
git push origin main
```

## Step 4. Confirm the CDN picked it up

jsDelivr caches for up to 12 hours on `@main`. Hit the file you changed and read the response:

```bash
curl -sI https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/palette.css
```

To force a refresh, purge the path:

```bash
curl -s https://purge.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/snippets/palette.css
```

`type-system.css` is served from the Collective Edge kit, not this one. A type change purges there.

## Step 5. Tag a version

Tag after a change to a value in section 3, 4 or 5 of the type standard, or to a palette value or a mark.

```bash
git tag v1.0
git push --tags
```

Production materials pin by replacing `@main` with `@v1.1` in the CDN URL.

## Step 6. Tell the team

One line. They run it once and Claude applies the brand from then on.

```bash
git clone https://github.com/collective-edge/royal-brand-kit ~/.claude/skills/royal-brand-guidelines
```

To update:

```bash
cd ~/.claude/skills/royal-brand-guidelines && git pull
```
