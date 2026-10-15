# House data color · reference

The colors that carry data. Shared, byte-identical in every kit, and never forked for a brand.

`snippets/data-color.css` is authoritative. `tokens.json` carries the same values for generators that cannot parse CSS. This file carries the reasoning and the measured numbers.

Read this before building any chart, table heatmap, dashboard tile, scorecard or comparison slide.

---

## 1. Why this layer exists

The brand palette is purple. For a logo, a band and a letterhead that is correct. For a chart it is a defect.

Measured: the rule this layer withdrew said chart series stay inside the purple ramp, `#2f193b`, `#43205b`, `#572e72`, `#8260a2`. Two of those sit at **ΔE 6.6 under normal vision**. The floor is 15. A reader with no color vision deficiency at all cannot reliably tell them apart. The rule was producing charts nobody could read, including the person who wrote the rule.

So, the governing principle:

> When there is data on the page, the job of color is to separate and to signal. The brand is carried by the band, the mark and the type, not by the bars.

A brand accent is never a series color and a series color is never a brand accent. Slot 1 is the single sanctioned exception: a kit may map it to the brand accent in `palette.css`, and Royal does.

---

## 2. The four jobs

Every color in a chart does exactly one of these. If you cannot say which, the chart is not finished.

| Job | Question it answers | What to use |
|---|---|---|
| **Identity** | which series is this | `--series-1` to `--series-8`, in order |
| **Magnitude** | how much | `--seq-100` to `--seq-700` |
| **Polarity** | which side of a baseline | `--div-neg-3` to `--div-pos-3` |
| **Direction** | is this good news | `--dir-favorable`, `--dir-unfavorable`, `--dir-caution`, `--dir-neutral` |

The commonest mistake in Royal and Apex material is using identity color where the answer was direction, or using two tints of the brand hue where the answer was identity.

---

## 3. Series · identity

Eight slots. Assign in order. Never cycle, never skip, never generate a ninth.

| Slot | Hue | Light | Dark ground | Contrast on white |
|---|---|---|---|---|
| 1 | purple | `#572e72` | `#be6df2` | 10.30:1 |
| 2 | green | `#1a9d4b` | `#1ba04d` | 3.52:1 |
| 3 | amber | `#dca821` | `#f3ba26` | 2.17:1 |
| 4 | red | `#d42320` | `#e6443a` | 5.17:1 |
| 5 | teal | `#1a97a3` | `#22b6c4` | 3.50:1 |
| 6 | orange | `#e6811c` | `#f78b1f` | 2.79:1 |
| 7 | blue | `#116dce` | `#519dfa` | 5.12:1 |
| 8 | pink | `#e53975` | `#fb608e` | 4.06:1 |

The **order is the safety mechanism**, not a preference. It was chosen by enumerating orderings and keeping only those where every neighboring pair stays separable under simulated red-green color blindness. Reordering the slots to suit a deck undoes the work.

Measured on the neighboring pairs:

| | Simulated red-green | Normal vision | Floor |
|---|---|---|---|
| Light | ΔE 9.8 | ΔE 22.3 | 8 / 15 |
| Dark ground | ΔE 14.5 | ΔE 26.4 | 8 / 15 |

**Caps that are not negotiable.**

- **Three series** on scatter, bubble, map and small-multiple charts. In those forms any two marks can end up adjacent, which is a harder test than bars and lines. Slots 1 to 3 clear it; slot 4 does not.
- **Eight series** everywhere else. Past eight, fold the tail into "Other" or split into several charts. A ninth color does not exist.
- **Amber `#dca821` and orange `#e6811c` sit below 3:1 on white.** Legal, but only with direct labels or a table view beside the chart. They are never the only way to read a value.

---

## 4. Sequential · magnitude

One hue, light to dark, for a single continuous quantity. Volume by month, density by region, minutes by hour.

| Step | Light | Dark ground |
|---|---|---|
| 100 | `#f0e1fd` | `#3d1f52` |
| 200 | `#e2c2fb` | `#572e72` |
| 300 | `#d29ef8` | `#7f42a6` |
| 400 | `#ba7ce4` | `#9d60c6` |
| 500 | `#9d60c6` | `#ba7ce4` |
| 600 | `#7f42a6` | `#d29ef8` |
| 700 | `#572e72` | `#e2c2fb` |

The ramp lands on Royal Purple `#572e72` at step 700. The brand color is the darkest step of the magnitude scale, which is why this layer could be added without moving a single brand value.

On a dark ground the anchor flips: the **lightest** step means the largest value.

- **Continuous scales** use the full range. Step 100 is allowed to recede into the page because it means "near zero".
- **Discrete ordered marks** (funnel stages, tiers, age bands) start at **step 300**. That is the lightest step that still separates from white, at 2.10:1.
- Never use a sequential ramp for things that merely have names. Facilities, payers and crews are identity, not magnitude.

**This is not the ramp for a two-bar before-and-after.** See section 7.

---

## 5. Diverging · polarity

Two hues away from a neutral middle, for distance above or below a baseline. Budget variance, days against target, percentage points against plan.

| Token | Light | Meaning |
|---|---|---|
| `--div-neg-3` | `#d05045` | furthest below |
| `--div-neg-2` | `#f67a6d` | |
| `--div-neg-1` | `#f9b8af` | just below |
| `--div-mid` | `#EDEBEF` | no difference |
| `--div-pos-1` | `#49e3eb` | just above |
| `--div-pos-2` | `#3ab9bf` | |
| `--div-pos-3` | `#2b9095` | furthest above |

**The poles are red and teal, not red and green.** Red against green measures **ΔE 5.5 under simulated deuteranopia**, which is a collapse: for a large minority of readers the two ends of the scale are the same color. Red against teal measures 12.8 and holds.

Green still carries good news. It does it through the direction tokens in the next section, where an icon and a word always travel with it, so the meaning never rests on hue alone.

The middle is gray on purpose. A hue in the middle of a diverging scale reads as a value rather than as "no difference".

---

## 6. Direction · how to feel about a number

This is the section that fixes the complaint "I cannot tell how to feel about this."

| Token | Light | On tint | Dark ground |
|---|---|---|---|
| `--dir-favorable` | `#158840` | ink `#127e3b` on `#daf8df` | `#1ca550` |
| `--dir-unfavorable` | `#db3931` | ink `#c5372f` on `#fde9e6` | `#f16154` |
| `--dir-caution` | `#a36912` | ink `#95600f` on `#fdebd7` | `#c68119` |
| `--dir-neutral` | `#64748B` | ink `#51607A` on `#F1F5F9` | `#B0A2BC` |

All of them clear 4.5:1 where they are used, including the ink steps on their own tints. `--dir-caution` replaces `--status-warn` `#B5821A` for anything that has to be read as text: `#B5821A` measures 3.40:1 on white and was never legal at body size.

### Direction is not the sign of the number

The rule that matters, and the one that gets broken:

> Color follows **favorable against unfavorable**. It never follows the arithmetic sign of the delta, and it never follows the direction of the arrow.

The worked example, from a real Royal report. Transports rose 6.3 percent. Hospital invoice cost fell 38.8 percent. One went up, one went down, **both are good news**. Both wear `--dir-favorable`. The arrow carries the direction, the word carries the meaning, and the color carries the verdict:

```html
<span class="bk-caption" style="background:var(--dir-favorable-tint); color:var(--dir-favorable-ink);
      padding:4px 11px; border-radius:999px; font-weight:700;">▲ 6.3% more</span>

<span class="bk-caption" style="background:var(--dir-favorable-tint); color:var(--dir-favorable-ink);
      padding:4px 11px; border-radius:999px; font-weight:700;">▼ 38.8% lower</span>
```

Two different arrows, one color, because there is one verdict.

Getting this wrong is worse than leaving it uncolored. A red "−38.8%" on a cost saving tells the reader Royal made things worse.

### Never color alone

Every direction value ships with an arrow or icon **and** a word. Reasons, in order of how often they bite:

1. The deck gets printed in grayscale.
2. The reader has a color vision deficiency. About one man in twelve does.
3. The slide is projected on a washed-out screen in a hospital conference room.

---

## 7. The comparison chart

A before-and-after against a baseline is the most common chart in Royal and Apex material, and it has its own recipe because the obvious approach is wrong.

**Wrong: two tints of the brand hue.** Light purple baseline, dark purple result. This is the defect this layer exists to fix. The two bars are close in hue and lightness, so the reader has to stop and read the labels to work out which is which. It also spends the brand color on a distinction the brand has no opinion about.

**Right, and the default:**

| Element | Token | Why |
|---|---|---|
| Baseline bar | `--data-baseline` `#CBD5E1` | The world before. Inert, and nothing to feel about it. |
| Result bar | `--series-1` | What the programme did. Carries the brand accent in Royal. |
| Delta pill | `--dir-*` with arrow and word | The verdict. |
| Headline figure | `--dir-favorable` | Stated once, in the unit that matters. Dollars, not percent. |

Gray against the accent separates instantly. That is the whole fix.

**The sanctioned variant.** On a single-metric hero slide, the result bar may take the direction color instead of the accent, so the bar itself carries the verdict. It reads from the back of a room. The cost is that on a report where everything went well, every bar is green and green stops carrying information. Use it for one slide, not for a deck.

**Do not** color a baseline red to make a result look better. The baseline is not a failure, it is a measurement.

---

## 8. Partner facility colors

Charts that compare partner facilities may use each facility's own brand color, which reads as informed and helps a reader who knows the logos. It is opt-in, it is per-chart, and it has a gate.

The gate exists because partner brands were never chosen to be distinguishable from each other. Measured on a realistic five-facility set: UCSF navy against El Camino's blue sits at **ΔE 9.0 under normal vision**, below the 15 floor. Once both are re-stepped to be chart-legible, UCSF navy against Kaiser blue collapses to **ΔE 0.5 under simulated protanopia**. They are the same blue.

The rule:

1. Use a partner color only from a sourced table. Where a kit ships `reference/partner-colors.md`, that file is the only sanctioned source and it carries each value with its confidence. Royal ships one. A kit without one has no sanctioned partner colors, so use the house series order. Never sample a logo, never guess.
2. Re-step the hue into the chart band. A partner's raw brand hex is usually a logo color and is often too dark or too weak to be a legible fill.
3. **Run `scripts/validate-palette.py` on the exact set in that chart.** Every chart, because the set changes.
4. On a failure, fall back to the house series order for the whole chart. Never part of it. A chart where three facilities wear their own colors and two wear house slots is worse than either.

---

## 9. Verify before shipping

```bash
python3 scripts/validate-palette.py --series                       # the house set, both grounds
python3 scripts/validate-palette.py "#572e72,#1a9d4b,#dca821"      # an ad-hoc set
python3 scripts/validate-palette.py "#...,#..." --pairs all        # scatter, bubble, map
python3 scripts/validate-palette.py "#...,#..." --ordinal          # a one-hue ramp
```

It reports the lightness band, the chroma floor, color-blind separation, the normal-vision floor and contrast against the ground, and exits non-zero on a real failure.

It cannot see a chart. Render it and look:

- [ ] Every color does exactly one of the four jobs, and you can say which.
- [ ] Series assigned in slot order, starting at 1.
- [ ] No two tints of the brand hue standing in for two different things.
- [ ] Direction follows favorable against unfavorable, not the sign of the number.
- [ ] Every direction color carries an arrow or icon and a word.
- [ ] Legend present for two or more series. Four or fewer are also directly labelled.
- [ ] Amber and orange series carry direct labels or a table.
- [ ] One y-axis. Two measures of different scale means two charts.
- [ ] Grayscale print still readable.
- [ ] On a dark band, `.bk-on-dark` is on the container.

---

## 10. What goes wrong

| Pattern | Why it fails |
|---|---|
| Two tints of brand purple for baseline and result | ΔE too low to separate. The original defect. |
| Red and green as the ends of a scale | ΔE 5.5 simulated deuteranopia. Collapses. |
| Red for a negative number that is good news | Tells the reader a cost saving was a loss. |
| A sequential ramp across facility names | Magnitude encoding on identity data. Implies a ranking that is not there. |
| A ninth series color | There is no ninth slot. Fold into "Other". |
| Series color on a value that means good or bad | Use direction tokens. Never both in one chart. |
| Brand accent on every bar | Spends the brand on a distinction it has no opinion about. |
| Color with no label | Fails on print, on projectors, and for one man in twelve. |

---

## 11. Sources

The method, the gates and the simulation model come from the house data visualisation standard: eight fixed hues in a validated order, OKLab ΔE ×100, Machado-Oliveira-Fernandes 2009 at severity 1.0.

The hue angles follow Apple's system colors, which is why the set reads as familiar rather than invented. Apple does not publish fixed hex values and advises against hard-coding them, so the hues were taken as angles and re-stepped against our own grounds. One useful coincidence made the whole thing fit: Apple's `systemPurple` sits at OKLCH hue 312.4 degrees and Royal Purple `#572e72` sits at 309.8 degrees. The brand hue was already the right hue. Only its lightness needed company.

Partner values and their confidence are recorded in a kit's own `reference/partner-colors.md` where one ships. Royal's is the worked example.
