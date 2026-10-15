# Royal Ambulance · logo and brand pack

Everything an outside designer needs to put the Royal Ambulance brand on something, in one folder. No install, no build step, no account. Download the folder and open it.

If you only read one line: use the SVG files, set type in Montserrat, and the purple is `#43205b`.

## What is in here

```
for-humans/
├── README.md                     You are reading it
├── Royal-Ambulance-logo-sheet.html   Open in a browser. Every mark, every color, on screen
├── logos/
│   ├── svg/                      Vector. Use these. Scales to any size with no quality loss
│   └── png/                      Raster, transparent background. For software that will not take SVG
└── fonts/
    └── Montserrat-VariableFont_wght.ttf   The brand typeface. Free to install and use
```

## Which logo to use

There are three lockups, each in two colors. Pick by the background you are placing it on.

| Lockup | Use it for | On a white or light background | On a dark purple background |
|---|---|---|---|
| **Horizontal** | The default. Anywhere with room across | `Royal-Ambulance-horizontal-purple` | `Royal-Ambulance-horizontal-white` |
| **Stacked** | Portrait and square formats, tight columns | `Royal-Ambulance-stacked-purple` | `Royal-Ambulance-stacked-white` |
| **Crown** | Icon only. Favicons, badges, social avatars, app tiles | `Royal-Ambulance-crown-purple` | `Royal-Ambulance-crown-white` |

Horizontal is the primary lockup. Reach for stacked or crown only when horizontal does not fit.

The file named `-purple` goes **on** light. The file named `-white` goes **on** dark. The name is the ink color, not the background.

## Sizes and spacing

| Rule | Value |
|---|---|
| Clear space on all four sides | Equal to the height of the crown mark |
| Smallest the horizontal lockup may go | 110 px on screen, 1 inch in print |
| Smallest the crown may go | 32 px on screen |
| Logo width in a letterhead header band | 1.4in to 1.8in |

## Do not

- Stretch, squash, skew or rotate it.
- Recolor it. Pick the file that matches the background instead.
- Change the color to anything but Royal Purple `#43205b` or white.
- Add a drop shadow, glow, outline or gradient.
- Pull the crown apart from the wordmark in the horizontal lockup.
- Put it on a busy photo without a solid backing panel behind it.
- Use it below the minimum sizes above.

## Color

Hex and RGB are the authoritative values. Everything else gets converted from these.

| Name | Hex | RGB | What it is for |
|---|---|---|---|
| Dark Purple | `#2f193b` | 47, 25, 59 | The dominant brand color. Header bands, hero backgrounds, full-width bands |
| Purple | `#572e72` | 87, 46, 114 | The workhorse accent. Buttons, links, rules, callout borders, purple text on white |
| Royal Purple | `#43205b` | 67, 32, 91 | The logo color on light backgrounds |
| Light Purple | `#8260a2` | 130, 96, 162 | Tertiary accents and hover states only |
| Charcoal | `#1E293B` | 30, 41, 59 | Body text |
| Muted grey | `#64748B` | 100, 116, 139 | Captions, secondary text |
| Hairline | `#E2E8F0` | 226, 232, 240 | Table rules, card borders |
| Surface | `#faf5fd` | 250, 245, 253 | Very light purple tint for alternating rows and callout fills |
| White | `#FFFFFF` | 255, 255, 255 | Page background |

Two things that will bite you, both measured:

- **Light Purple `#8260a2` is never body text and never a large background.** It is a tertiary accent and a hover state, nothing more.
- **Never put Light Purple `#8260a2` on Dark Purple `#2f193b`.** It measures 3.13:1 and fails at every size. On a dark background use `#E0D6E8` for body text and `#B0A2BC` for captions.

White text belongs only on Dark Purple, Purple or Royal Purple. Never white on Light Purple.

No CMYK build is specified for this brand. For offset or large-format work, convert from the hex values above and send a proof before the run.

## Type

The brand is set in **Montserrat** throughout. There is no secondary typeface.

The variable font file is in `fonts/`. It is also free from Google Fonts at https://fonts.google.com/specimen/Montserrat, which is the better source if you want the full static family.

Headings are bold. Display statements on a title, band or divider are uppercase and letter-spaced, and never run past four words. Headings inside a document are sentence case.

## Writing, if you are setting copy

- Short declarative sentences. Active verbs. Nothing before the point.
- No em dashes. Use a period, a comma, or `·`.
- A label and a value, nothing between them. No helper text under a field, no caption restating the number above it.
- Name partners and facilities exactly the way they write themselves.

## Questions

Anything this folder does not answer, ask before you guess. The brand owner would rather answer a question than correct a proof.
