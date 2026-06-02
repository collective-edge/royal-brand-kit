# How to push this to GitHub (one-time, ~3 minutes)

Everything is already prepared in this folder. You just need to push it.

## Step 1. Create the empty repo on GitHub

Go to **https://github.com/organizations/collective-edge/repositories/new** and create:

- **Repository name:** `royal-brand-kit`
- **Visibility:** **Public** (required for the jsDelivr CDN to work)
- **Do NOT** initialize with a README, .gitignore, or license — this folder already has those.

Click **Create repository**.

## Step 2. Push from terminal

Open Terminal, then:

```bash
cd "/Users/jacob/Desktop/Royal Brand Kit/github/royal-brand-kit"
git init
git add .
git commit -m "Initial Royal Ambulance brand kit"
git branch -M main
git remote add origin https://github.com/collective-edge/royal-brand-kit.git
git push -u origin main
```

You may be prompted for GitHub authentication. The easiest path is to install the [GitHub CLI](https://cli.github.com/) and run `gh auth login` once.

## Step 3. Verify the CDN is live

After pushing, hit this URL in a browser (give jsDelivr 30–60 seconds to cache the first time):

```
https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/logos/horizontal-white.svg
```

You should see the white Royal logo. The font, colors.json, and example HTML are all at the same base URL.

## Step 4. Switch your local one-pager to the CDN

The deliverable PDF in `Royal Brand Kit/ECLG-to-ECMV Cath Lab Workflow - One Pager.pdf` already has Montserrat embedded, so it works as-is.

If you want to regenerate it (or any future doc) using the CDN instead of the local font file, in the HTML source replace:

```css
src: url('Montserrat.ttf') format('truetype');
```

with:

```css
src: url('https://cdn.jsdelivr.net/gh/collective-edge/royal-brand-kit@main/assets/fonts/Montserrat-VariableFont_wght.ttf') format('truetype');
```

The fully-CDN version is already saved at `github/royal-brand-kit/examples/eclg-ecmv-one-pager.html` and will work the moment your repo is pushed.

## Step 5. Tell teammates

Share this single line. They run it once and Claude on their machine applies the brand automatically forever:

```bash
git clone https://github.com/collective-edge/royal-brand-kit ~/.claude/skills/royal-brand-guidelines
```

## Updating later

Edit any file in `github/royal-brand-kit/`, then:

```bash
cd "/Users/jacob/Desktop/Royal Brand Kit/github/royal-brand-kit"
git add . && git commit -m "Describe what changed" && git push
```

Changes go live on the CDN within a minute or two. Anyone with the skill installed can pull updates with `git pull`.

## Versioning (optional, for production safety)

Once the kit is stable, tag a release so production materials can pin to a fixed version:

```bash
git tag v1.0
git push --tags
```

Then in CDN URLs, replace `@main` with `@v1.0`. Bump the tag when you ship breaking changes.
