# House UI standard · v1.0

Byte-identical in every kit. `snippets/ui.css` owns interactive control structure and nothing
else. Load it third, after `snippets/type-system.css` and `snippets/palette.css`, from
`cdn.jsdelivr.net/gh/collective-edge/<kit>@main/snippets/ui.css`.

**Shared, because inconsistency here reads as carelessness.** Buttons, links, form controls,
status badges, focus, disabled, loading.
**Not shared, because this is where a site earns its character.** Page layout, heroes, cards,
marketing sections, dashboard shells, tables, stat tiles, navigation, empty and loading screens.
A project needing one of those builds it on these tokens. A floor, not a ceiling: every `--ui-*`
token is overridable on `:root`.

## Tokens

| Token | Value | For |
|---|---|---|
| `--ui-target-min` | `44px` | the floor. Nothing a person taps is smaller |
| `--ui-h-sm` `--ui-h-md` `--ui-h-lg` | `44px` `48px` `56px` | control height |
| `--ui-pad-sm` `--ui-pad-md` `--ui-pad-lg` | `12px` `16px` `24px` | horizontal padding |
| `--ui-gap` `--ui-radius` | `8px` `6px` | dot or icon to label, control corner |
| `--ui-border` `--ui-border-color` | `1px` `var(--fg-3)` | the control edge, 5.12:1 in every brand |
| `--ui-focus-width` `--ui-focus-offset` `--ui-focus-ring` | `2px` `2px` `var(--focus-ring, var(--fg-1))` | the ring. Black on Collective Edge, ink on Apex and Royal |
| `--ui-accent` `--ui-accent-deep` `--ui-on-accent` | palette names | filled button |
| `--ui-danger` `--ui-danger-deep` | `var(--status-stop)`, mixed 85% toward the band | destructive |
| `--ui-ink` `--ui-ink-help` `--ui-tint` | palette names | label, help, hover tint |
| `--ui-disabled-fill` `--ui-disabled-ink` | `var(--border-1)` `var(--fg-3)` | disabled |
| `--ui-motion` | `120ms` with `--ease-standard` | every transition |

## Buttons

`.ui-btn` plus one of `.ui-btn--primary`, `.ui-btn--secondary`, `.ui-btn--danger`.
Sizes `.ui-btn--sm` and `.ui-btn--lg`, default md. Shapes `.ui-btn--icon`, `.ui-btn--full`.
Labels are sentence case at 600 in every brand. Only the filled variants carry color, so a
screen holds exactly one loud action.

| State | What changes | Measured |
|---|---|---|
| rest | accent fill, white label | 21.00:1 Collective Edge, 10.71:1 Apex, 10.30:1 Royal |
| hover | fill deepens to `--bg-inverse` | 21.00:1, 14.56:1, 15.87:1 |
| active | the hover fill plus `--shadow-1` inset | unchanged |
| focus | `:focus-visible`, 2px ring, 2px offset | ring on ground 21.00:1 Collective Edge, 15.61:1 Apex and Royal |
| disabled | `--border-1` fill, `--fg-3` ink, box unchanged | 4.04:1 in every brand |
| loading | `aria-busy="true"`, label stays, ring spins | unchanged |

Destructive rests at 6.29:1 and hovers at 7.91:1, 7.38:1, 7.34:1. Fill it only inside a
confirmation; in a settings row it is `.ui-btn--secondary` carrying the danger ink.

**There is no text-only button.** With no fill and no border it has no boundary reaching the 3:1
SC 1.4.11 asks, and `scripts/ui-audit.py` says so at every width. The quiet action is a link.

## Links

`.ui-link` in running copy: the accent, a real underline, thickening on hover. On Collective Edge
the accent is the ink the copy is already set in, so the underline is the whole signal.
`.ui-link-action` standing alone: 600, 44px tall, underlined. It is a page’s quiet action.

## Fields

`.ui-field` wraps `.ui-label`, one control, and one of `.ui-help` or `.ui-error`. `.ui-form`
stacks fields at 24px against the 8px inside a field, the same three-to-one attachment the type
standard gives a heading.

Controls: `.ui-input`, `.ui-select`, `.ui-textarea`. All 48px tall, 16px type, `--fg-3` edge.
Sixteen, not fourteen: below 16px iOS Safari zooms on focus and does not zoom back out.

Error: set `aria-invalid="true"` on the control and point `aria-describedby` at the message. The
border turns, one message appears, the label stays neutral. Mark the optional field with
`.ui-optional`, never the required one with a red asterisk: `--status-stop` keeps one meaning,
which is that something is wrong right now.

## Checkbox and radio

`.ui-check` is the label; it wraps `.ui-checkbox` or `.ui-radio` and the words. The box is 20px
and the label is 44px tall, which is what gives the control its target and lets a person hit the
words. Checked mark on fill: 21.00:1, 10.71:1, 10.30:1.

## Status badges

`.ui-badge` plus `.ui-badge--go`, `--warn`, `--stop` or `--info`. One tint under all four and the
status color on the dot, because the warn base measures 3.40:1 on white and cannot legally set
12px text. The lowest dot value across the three brands is the Collective Edge warn dot at 3.01:1.
The dot reads `--alert-go`, `--alert-warn`, `--alert-stop` and `--alert-info`, the alert base that
`--status-*` aliases, because the chip under it is light on every ground.

A brand may switch the shape off. Royal does, and prefers a dot and a sentence. That is a
position, not drift.

## On a dark band

Put `.ui-on-dark` on the band. The ring flips to white, the filled button inverts to a white fill
with dark ink, the secondary edge flips to `--fg-on-dark-3`. An ink ring on a dark ground measures
1.00:1, 1.07:1 and 1.02:1 and is invisible, which is why two ring colors exist. `.ui-btn--danger`
has no dark form: the stop fill against the three bands measures 2.48:1, 2.31:1 and 2.52:1, so a
destructive action belongs in a dialog on the page surface. A field keeps its light surface on a
band; its label and help text flip, the field does not.

## The three things an agent gets wrong most often

1. **Rebuilding the tokens.** Four web projects define 382 local CSS variables where about 95
   would do, and one file in the whole estate loads anything from a kit. Load the three
   stylesheets and style through `--ui-*`. Override a token; never redeclare a control.

2. **Removing the focus ring.** `outline: none` with no replacement appears twice in one dashboard
   today. The ring is declared once here, on `:focus-visible`, at zero specificity so a component
   extends it. Never suppress it, and never bind it to `:focus`, which paints on a mouse click too
   and is what leads teams to delete it.

3. **Reaching for `--fg-4`.** It is the obvious name for disabled or helper text and it is not
   legible: 3.39:1 on white in every brand, failing the 4.5:1 text owes. Help text is `--fg-3`.
   On `--bg-surface` it holds at 4.53:1 or better. On `--bg-surface-2` it falls to 4.10:1, so a
   field on that panel overrides `--ui-ink-help` to `--fg-2`.

## Verify before shipping

```
python3 scripts/ui-audit.py <url-or-file> --width 375 --width 768 --width 1440
python3 scripts/validate.py <file.html>
```

`Examples/ui-controls.html` renders every control in every state and is clean on both.