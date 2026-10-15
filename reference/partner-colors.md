# Partner facility colors

Royal only. Not shared, not in `brands.json`, and not part of the house data layer.

A chart comparing partner facilities may give each facility its own brand color. It reads as informed and it helps a reader who already knows the logos. It is opt-in, decided per chart, and it has a gate.

Read `reference/data-color.md` first. This file is the lookup table and the sourcing record.

---

## 1. The gate

Partner brands were never chosen to be distinguishable from each other. Measured on a realistic five-facility set:

| Pair | Measured | Floor | Result |
|---|---|---|---|
| UCSF navy against El Camino blue, raw brand hexes | ΔE 9.0 normal vision | 15 | Fails |
| UCSF navy against Kaiser blue, both restepped to be chart-legible | ΔE 0.5 simulated protanopia | 8 | Collapses |

Half of Bay Area healthcare is blue. Two of those logos in one chart is two series the reader cannot separate.

So, four steps, in order, every time:

1. **Look the value up here.** Never sample a logo, never eyedropper a PDF, never guess from memory.
2. **Restep the hue into the chart band.** A brand hex is a logo color. It is usually too dark or too weak to work as a fill. Hold the hue, move the lightness.
3. **Run the validator on the exact set in that chart.**
   ```bash
   python3 scripts/validate-palette.py "#...,#...,#..." --pairs all
   ```
   Use `--pairs all` whenever marks can end up side by side, which on a facility comparison they can.
4. **On a failure, fall back to the house series order for the whole chart.** Never for part of it. A chart where three facilities wear their own colors and two wear house slots is worse than either option taken cleanly.

---

## 2. The table

`Confidence` is the only column that decides whether you may use a value.

- **Verified** · taken from the organization's own published identity guidance. Usable.
- **Reported** · consistent across independent third-party sources, not confirmed against the owner's own guidance. Usable with the gate, and worth confirming before anything goes to the partner.
- **Unknown** · no reliable value found. **Use the house series order.** Do not approximate.

| Facility | Color | Hex | Confidence | Source |
|---|---|---|---|---|
| Stanford · Stanford Medicine | Cardinal Red | `#8C1515` | Verified | Stanford identity guidance, Pantone 201 C, RGB 140/21/21 |
| Stanford, interactive accent only | Digital Red | `#B1040E` | Verified | Stanford identity toolkit. Explicitly not a replacement for Cardinal |
| UCSF · UCSF Health | Navy | `#052049` | Verified | UCSF brand identity, color palette page |
| UCSF, links and digital | UCSF Blue | `#0071AD` | Verified | UCSF websites standard, replaced Pantone Process Blue C |
| El Camino Health | Cinnabar | `#E03E1A` | Reported | Third-party brand index. Consistent with the 2009 rebrand to orange and blue |
| El Camino Health | Bahama Blue | `#006E90` | Reported | Same source |
| Sutter Health | Teal | `#00A499` | Reported | Third-party sources disagree in the range `#00A499` to `#00A9A0` |
| Kaiser Permanente | Blue | `#0075C9` | Reported | Widely published, not confirmed against Kaiser's own guidance |
| Alameda Health System | — | — | Unknown | No published value found. Use the house series order |
| John George Psychiatric Hospital | — | — | Unknown | Operates under Alameda Health System. Use the house series order |

UCSF publishes a six-range palette (blue, teal, green, purple, violet, magenta). Only navy and the link blue above were confirmed. For anything beyond those two, ask UCSF or use the house order.

---

## 3. Restepping

A logo color is rarely a legible fill. Both Stanford Cardinal `#8C1515` and UCSF Navy `#052049` sit below the chart lightness band, so as bars they read as near-black and lose their identity entirely.

Hold the hue angle, move the lightness until the mark clears 3:1 on the ground, then validate the set. Worked, on the three facilities with distinct hues:

| Facility | Brand hex | Chart step | On white |
|---|---|---|---|
| Stanford | `#8C1515` | `#d23934` | 4.80:1 |
| UCSF | `#052049` | `#2876ea` | 4.31:1 |
| Sutter | `#00A499` | `#1ea69b` | 3.01:1 |

```bash
python3 scripts/validate-palette.py "#d23934,#2876ea,#1ea69b" --pairs all
```

That set passes: worst pair ΔE 13.5 simulated red-green, 20.3 normal vision, everything clear of 3:1.

Two things that restepping will not fix, both met while deriving the set above:

- **Sutter's teal barely holds.** At `#1ea69b` it measures 3.01:1 on white and sits just over the chroma floor. A darker step clears contrast but drops below the floor and starts reading as gray. It works, with a direct label, and it has no headroom.
- **Kaiser cannot join this set.** Kaiser blue and UCSF navy are the same hue, so whatever lightness they are given they collapse. Three distinct hues is the practical ceiling.

---

## 4. When not to do this at all

- **Any chart where two facilities share a hue family.** Two blues is the common case. Use the house order.
- **Anything going to one of those partners.** A UCSF deck using Stanford's cardinal for a comparison line is a bad look in a room where both are present.
- **Clinical or instructional material.** Color there carries safety meaning. It is not for identity.
- **More than four facilities.** Fold the tail into "Other", or split into small multiples.

The house series order is never the lesser option. It is the one that was measured.

---

## 5. Maintaining this file

Values move when a partner rebrands. Before using one in anything going outside Royal, confirm it against the partner's own identity page. Promote a Reported value to Verified only when you have seen it in the owner's published guidance, and record where.

Never record a value taken by eyedropper from a logo, a screenshot or a PDF. Color management, image compression and screen profiles all shift it, and the result is a color the partner does not recognize as theirs.
