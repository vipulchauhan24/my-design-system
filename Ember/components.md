# Components

Specs for the Ember component set. Button, Input, Card, Alert and the Data Grid are fully specified; the rest list variants, states and tokens so they can be expanded the same way.

All components read **component tokens** (`--button-*`, `--grid-*`, …) from `tokens.css`. In Tailwind apps, use the utilities from `tailwind-theme.css`; each spec shows both.

## Rules that apply to every interactive component

| Rule | How it is met |
|---|---|
| Visible focus | `:focus-visible` shows a `--focus-ring-width` (2px) ring in `--color-focus-ring`, offset `--focus-ring-offset`. ≥3:1 on every surface (see `contrast-report.txt`). Tailwind: `focus-ring`. |
| Pointer target ≥ 44px | Controls are 32 / 40 / 48px visually. On `(pointer: coarse)` the `sm` and `md` sizes grow to 44px (`--size-touch-target`). On fine pointers, `sm` is 32px (above the 24px WCAG 2.5.8 minimum) and an invisible `::after` extends its hit area to 44px. Grid rows grow to 44px on touch. |
| Disabled vs loading | Use `aria-disabled="true"` (not the `disabled` attribute) where the element should stay focusable, plus `aria-busy="true"` while loading. Disabled opacity is `--opacity-disabled`. |
| Not color alone | Status always has an icon or a word. Selected rows have an accent bar, not only a tint. Sort state has an arrow and `aria-sort`. |
| Reduced motion | Transitions use `--motion-duration*`, which collapse to 0ms under `prefers-reduced-motion`. |
| Forced colors | The focus outline falls back to `Highlight`. Borders carry meaning, so keep them (do not rely on background alone). |
| Brand fill and label flip together | Light: white on `#D14800`, 4.53:1. Dark: near-black on `#FF671F`, 6.41:1. Always use `--color-on-primary`, never hard-coded white or black. White on `#FF671F` is 2.91:1 and **fails**. |

---

## Button

**Variants**

| Variant | Use | Fill | Label | Edge |
|---|---|---|---|---|
| `primary` | The one main action per view | `--button-primary-bg` (#D14800 light, #FF671F dark) | `--button-primary-text` (white light, near-black dark) | `--button-primary-border` (same as fill) |
| `secondary` | Alternative actions | `--button-secondary-bg` | `--button-secondary-text` | `--button-secondary-border` (3:1) |
| `ghost` | Tertiary, toolbars, dense UI | transparent | `--button-ghost-text` | none |
| `destructive` | Irreversible actions | `--button-destructive-bg` | `--button-destructive-text` | none |
| `link` | Inline navigation-like action | none | `--button-link-text` (ember-700) | underline |

**Sizes**

| Size | Height token | Visual | Padding X | Font |
|---|---|---|---|---|
| `sm` | `--button-height-sm` | 32px (44px on touch) | `--button-padding-x-sm` | `--button-font-size-sm` (13px) |
| `md` | `--button-height-md` | 40px (44px on touch) | `--button-padding-x-md` | `--button-font-size-md` (16px) |
| `lg` | `--button-height-lg` | 48px | `--button-padding-x-lg` | `--button-font-size-lg` (16px) |

**States**

| State | Primary | Notes |
|---|---|---|
| default | light: bg `ember-500` `#D14800`, white label (4.53:1). dark: bg `ember-400` `#FF671F`, near-black label (6.41:1) | |
| hover | light: `ember-600` (darker). dark: `ember-300` (lighter) | Hover moves away from the page background in each theme, and label contrast only improves (5.93:1 light, 9.66:1 dark). |
| active | light: `ember-700`; dark: `ember-200` | Label ≥7.9:1 |
| focus-visible | 2px ring `--color-focus-ring`, 2px offset | |
| disabled | `--button-disabled-opacity`, `cursor: not-allowed`, `aria-disabled="true"` | Contrast is exempt for disabled controls |
| loading | `aria-busy="true"`, spinner replaces or precedes the label, width does not change, clicks ignored | Spinner is `currentColor`; announce completion via a live region |

**Composition.** An icon-only button must have `aria-label` and be square (`width = height`). Put at most one `primary` button in a group. In a button pair, primary goes last in LTR (trailing action) and Cancel is `ghost`.

**Tailwind**

```html
<button class="inline-flex items-center justify-center gap-2 h-control-md px-4 rounded-md
               bg-brand text-on-brand font-semibold hover:bg-brand-hover active:bg-brand-active focus-ring
               aria-disabled:opacity-45 aria-disabled:cursor-not-allowed">
  Save changes
</button>
```

**Do** use `primary` for the single most important action. **Do** pair a destructive action with a confirming label ("Delete project", not "OK").
**Don't** hard-code white or black on `bg-brand` (use `text-on-brand`, which flips with the theme). **Don't** use `ember-400` (#FF671F) as text on a light background: it is 2.91:1.

---

## Input (text, textarea, select)

**Anatomy:** label (always visible, associated with `for`/`id`), control, optional helper text, optional error text.

| Token | Value |
|---|---|
| Height | `--input-height` (40px; 44px on touch) |
| Font size | `--input-font-size` = 1rem (16px; also prevents iOS zoom-on-focus) |
| Padding X / radius | `--input-padding-x` / `--input-radius` |
| Background / text | `--input-bg` / `--input-text` |
| Border | `--input-border` (ash-500, ≥3:1), hover `--input-border-hover`, focus `--input-border-focus` |
| Placeholder | `--input-placeholder` (≥4.5:1, but never a substitute for a label) |

**States**

| State | Behavior |
|---|---|
| default | 1px `--input-border` |
| hover | border → `--input-border-hover` |
| focus-visible | 2px ring in `--input-border-focus`, no offset |
| error | border `--input-border-error` **and** an icon + message below (`--input-error-text`), `aria-invalid="true"`, `aria-describedby` → message id |
| disabled | `--input-bg-disabled`, `--opacity-disabled`, `disabled` attribute (not focusable) |
| read-only | Normal appearance, `readonly`, stays focusable |

**Composition.** Stack label → control → helper with `--space-2xs` gaps. In a form, use `--space-stack-gap` between fields. Error text replaces helper text, it does not sit beside it.

**Tailwind**

```html
<label for="n" class="text-sm font-medium text-fg">Project name</label>
<input id="n" class="h-control-md w-full px-3 rounded-md bg-canvas text-fg border border-line-strong
                     hover:border-fg-muted focus-visible:outline-2 focus-visible:outline-focus
                     aria-invalid:border-critical placeholder:text-fg-subtle disabled:bg-sunken disabled:opacity-45">
<p class="text-sm text-fg-muted">Lowercase, with hyphens.</p>
```

**Do** keep the label visible. **Do** say how to fix the error ("Enter an email like name@site.com").
**Don't** signal an error with a red border only. **Don't** use the brand orange for the error state (it is not distinguishable from focus/brand).

---

## Card

A bordered container that groups related content. Border-first, not shadow-first, so dense layouts stay quiet.

| Token | Default |
|---|---|
| `--card-bg` | `--color-surface-raised` |
| `--card-border` / `--card-border-hover` | `--color-border` / `--color-border-strong` |
| `--card-radius` | `--radius-container` (10px) |
| `--card-padding` / `--card-gap` | 24px / 16px |
| `--card-shadow` / `--card-shadow-hover` | none / `--shadow-raised` |
| `--card-title-text` / `--card-body-text` | primary / secondary text |

**Variants:** `static` (default), `interactive` (whole card is one link or button; hover strengthens the border and adds a shadow), `selected` (uses `--color-surface-selected` and a 2px `--color-primary` border).

**States:** interactive cards need focus-visible (ring on the card, not an inner element), hover, active (no shadow), and disabled.

**Composition.** Title (`h3`/`h4`), body, then actions at the end. An interactive card contains **one** primary link; do not nest buttons inside a clickable card. In dark mode elevation comes from `--color-surface-raised` being lighter than the page, not from shadows.

**Tailwind**

```html
<article class="grid gap-4 p-6 rounded-lg bg-raised border border-line hover:border-line-strong hover:shadow-low">
  <h3 class="text-xl font-semibold text-fg">Grid for Tailwind</h3>
  <p class="text-fg-muted">Sort, filter, pin and resize columns.</p>
</article>
```

**Do** keep one idea per card. **Don't** nest cards more than one level, or stack more than two surface levels.

---

## Alert

Inline, persistent message about the page or a form. For transient messages use a Toast (same tokens, `--shadow-popover`, auto-dismiss ≥6s, never the only place an error is shown).

**Variants:** `info`, `success`, `warning`, `error`. Each has `--alert-{v}-bg`, `--alert-{v}-accent` (2px start border), `--alert-{v}-icon`.

**Anatomy:** status icon (decorative, `aria-hidden`), title (semibold), description, optional action and dismiss button.

| Token | Value |
|---|---|
| `--alert-bg` family | the status `-subtle` color |
| `--alert-text` | `--color-text-primary` (text stays neutral; only the icon and accent carry color) |
| `--alert-radius` / `--alert-padding` / `--alert-gap` | 10px / 16px / 12px |
| `--alert-accent-width` | 2px |

**Accessibility.** `error` uses `role="alert"` (assertive). The others use `role="status"` (polite). The title always names the status in words ("Deploy failed"), and the icon differs per status, so color is never the only signal. Status text/icons use `*-text` tokens (≥4.5:1 on surface and on the tinted bg). Dismiss button ≥44px target with `aria-label="Dismiss"`.

**Why gold and crimson.** Brand orange (hue 41) sits between warning and error on the color wheel. Warning is pushed to yellow-gold (hue 90) and error to a pinkish crimson (hue 15), and the brand is never used for status.

**Tailwind**

```html
<div role="alert" class="flex gap-3 p-4 rounded-lg bg-critical-subtle text-fg border-s-2 border-critical">
  <svg class="size-5 text-critical-fg" aria-hidden="true">…</svg>
  <div><b class="font-semibold">Deploy failed</b> The build exited with code 1.</div>
</div>
```

**Do** write the title as an outcome. **Don't** use an alert for marketing banners, and don't color the body text.

---

## Data Grid

Tokens and rules for the AG Grid-inspired Tailwind table. The grid renders in the page's theme and density scope, so it needs no props for either.

**Structure**

| Part | Tokens |
|---|---|
| Shell | `--grid-bg`, `--grid-border`, `--grid-radius`, `--grid-font-size` (13px) |
| Header | `--grid-header-height`, `--grid-header-bg`, `--grid-header-bg-hover`, `--grid-header-text`, `--grid-header-text-active`, `--grid-header-weight` |
| Row | `--grid-row-height`, `--grid-row-bg`, `--grid-row-bg-alt` (zebra, optional), `--grid-row-bg-hover`, `--grid-row-bg-selected`, `--grid-row-border`, `--grid-row-selected-accent` |
| Cell | `--grid-cell-padding-x`, `--grid-cell-text`, `--grid-cell-text-muted`, `--grid-cell-editing-bg`, `--grid-cell-focus-ring`, `--grid-cell-focus-ring-width` |
| Numeric | `--grid-font-numeric` (JetBrains Mono) with `font-variant-numeric: tabular-nums`, right-aligned |
| Sort | `--grid-sort-icon`, `--grid-sort-icon-active` |
| Resize | `--grid-resize-handle`, `--grid-resize-handle-hover`, `--grid-resize-handle-width`, `--grid-resize-hit-width` (8px grab area around a 2px line) |
| Pinned | `--grid-pinned-bg`, `--grid-pinned-shadow-start`, `--grid-pinned-shadow-end` |
| Layering | `--grid-z-cell` < `--grid-z-pinned` < `--grid-z-header` (pinned header cells sit at header + 1) |
| Footer / status bar | `--grid-footer-bg`, `--grid-footer-text`, `--grid-footer-height` |

**Density.** Set `data-density` on the grid (or any ancestor). The `--grid-*` size tokens are re-declared per `[data-density]` scope in `tokens.css`, so nested grids can differ.

| Density | Row | Header | Cell padding X |
|---|---|---|---|
| `compact` | 28px | 32px | 8px |
| default | 36px | 40px | 12px |
| `comfortable` | 44px | 48px | 16px |

On `(pointer: coarse)` every row is 44px, whatever the density.

**States**

| State | Treatment |
|---|---|
| Row hover | `--grid-row-bg-hover` |
| Row selected | `--grid-row-bg-selected` **plus** a 2px start accent bar `--grid-row-selected-accent`, `aria-selected="true"` |
| Sorted column | arrow in `--grid-sort-icon-active` and `aria-sort="ascending\|descending"` on the `th` |
| Cell focus | 2px inset ring in `--grid-cell-focus-ring` (inset so adjacent cells do not clip it) |
| Editing | cell takes `--grid-cell-editing-bg` and an input-style focus ring |
| Pinned column | opaque `--grid-pinned-bg` and an edge shadow only while content is scrolled beneath it |
| Resizing | handle turns `--grid-resize-handle-hover`; cursor `col-resize` for the entire hit area |
| Loading | skeleton rows at the current row height, `aria-busy="true"` on the grid |
| Empty | centered message and a primary action inside the shell |

**Accessibility.** Use semantic table markup (or the ARIA `grid` role when cells are navigable by arrow keys). Header sort controls are `<button>`s inside `<th scope="col">`. The scroll region is focusable (`tabindex="0"`) with a label. Selection is announced through `aria-selected` and a live count in the footer. Resize handles need a keyboard alternative (e.g. focus the header, then `Alt+←/→`).

**Tailwind**

```html
<div data-density="compact" class="rounded-lg border border-line bg-canvas overflow-hidden text-sm">
  <table class="w-full border-separate border-spacing-0">
    <thead>
      <tr class="h-header-row bg-sunken text-fg-muted font-semibold sticky top-0 z-(--z-grid-header)">
        <th class="px-(--grid-cell-padding-x) text-start" aria-sort="ascending">Project</th>
        <th class="px-(--grid-cell-padding-x) text-end numeric">Stars</th>
      </tr>
    </thead>
    <tbody>
      <tr class="h-row border-b border-line hover:bg-hover aria-selected:bg-selected aria-selected:shadow-[inset_2px_0_0_var(--color-primary)]" aria-selected="true">
        <td class="px-(--grid-cell-padding-x) font-semibold">ember-ui</td>
        <td class="px-(--grid-cell-padding-x) text-end font-mono numeric">2,840</td>
      </tr>
    </tbody>
  </table>
</div>
```

**Do** right-align and tabular-figure numbers. **Do** keep header text `--color-text-secondary` so data outranks chrome.
**Don't** use brand orange for hover or zebra rows (it is reserved for selection, sort and focus signals). **Don't** pin more than two columns.

---

## Remaining components

Each is expressed with the tokens already in `tokens.css`; expand each into a full spec when you build it.

| Component | Variants | States | Tokens | Notes |
|---|---|---|---|---|
| **Select / Combobox** | single, multi, searchable | = Input, plus open, option hover, option selected | `--input-*`, `--color-surface-overlay`, `--shadow-popover`, `--z-dropdown` | Selected option: `--color-surface-selected` + check icon, not color alone |
| **Checkbox / Radio** | default, indeterminate (checkbox) | unchecked, checked, focus-visible, disabled, error | `--check-*` | Checked fill is the brand color with a glyph in `--check-checked-icon` (flips with the theme); 44px label hit area |
| **Switch** | default | off, on, focus-visible, disabled | `--switch-*` | Needs a visible label; track-on is the brand fill (≥4.5:1 light, 6.4:1 dark), so on/off differ by more than color: the thumb moves |
| **Badge** | neutral, brand, secondary, success, warning, error, info | static | `--badge-*` | Status badges include an icon or glyph. 11px text, so keep to ≤2 words |
| **Tabs** | underline | default, hover, selected, focus-visible, disabled | `--tabs-*` | Indicator uses `--color-primary` (≥3:1 on every surface). Arrow-key roving focus |
| **Tooltip** | default | visible on hover **and** focus | `--tooltip-*` | Inverse surface. Dismissible with `Esc`, hoverable, never the only place information lives |
| **Modal / Dialog** | default, destructive confirm | open, closing | `--modal-*`, `--color-scrim` | Focus trap, `Esc` closes, return focus to the trigger, `aria-modal`, scroll lock |
| **Toast** | info, success, warning, error | enter, exit | `--alert-*`, `--shadow-popover`, `--z-toast` | Same variants and icons as Alert. ≥6s, pause on hover/focus |
| **Menu / Dropdown** | default | item hover, item focus, disabled, open | `--color-surface-overlay`, `--shadow-popover`, `--z-dropdown` | Roving tabindex, type-ahead |
| **Pagination** | numbered, compact | current, hover, disabled | button tokens, `--grid-footer-*` | Current page: `aria-current="page"` and weight, not only color |
| **Skeleton** | text, block | pulse | `--color-surface-sunken`, `--motion-duration-slow` | Respect reduced motion (no pulse) |

## Portfolio patterns

Portfolio and marketing pages use the same tokens with more air and a bigger display tier:

- Headings: `--text-display-lg-size` / `--text-display-md-size` (fluid), `--text-display-line`, `--text-display-tracking`.
- Sections: `--space-section-gap` (fluid 64-128px); page gutters: `--space-page-margin` (fluid 16-40px).
- Content width: `--layout-content-max` (72rem); long text: `--layout-prose-max` (65ch) at `--text-prose-line`.
- A highlighted word in a headline can be set as a `bg-brand text-on-brand` mark, as in `preview.html`. That is the safest way to use the brand orange at large sizes.
