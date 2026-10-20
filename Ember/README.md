# Ember Design System

One set of design tokens and component specs for the portfolio, the Tailwind data grid library and the personal UI library, built around the brand color **`#FF671F`**, adjusted to **`#D14800`** in light mode so it passes AA on white.

> Open `preview.html` in a browser to see everything: palette, type, controls, feedback and a live data grid, in light and dark.

## Contents

| File | What it is |
|---|---|
| `tokens.css` | **Source of truth.** Primitive, semantic and component tokens, light and dark themes, density modes, accessibility media queries. Plain CSS custom properties. |
| `tailwind-theme.css` | Tailwind v4 preset. Imports `tokens.css` and exposes it as utilities (`bg-brand`, `text-fg`, `h-row`, …). |
| `tokens.json` | W3C DTCG-format export for Figma (Tokens Studio) and Style Dictionary. Generated. |
| `components.md` | Component specs: Button, Input, Card, Alert and the Data Grid in full; the rest summarized. |
| [`../contrast-reports/ember.txt`](../contrast-reports/ember.txt) | Verified WCAG contrast output for both themes. |
| `preview.html` | Visual reference page. Reads only from `tokens.css`. |
| `scripts/` | `check-contrast.sh` (verify), `build_tokens_json.py` (regenerate `tokens.json`). |

## Direction

**Ember on charcoal.** Confident, technical and warm. The brand orange is used as a *fill*; everything around it is quiet and warm-tinted so the orange does the talking.

| Area | Choice | Why |
|---|---|---|
| Brand | `ember` scale. **500 = `#D14800`** (light-mode brand, 4.53:1 on white). **400 = `#FF671F`** (the original; dark-mode brand, logos, decorative use). | `#FF671F` alone is 2.91:1 on white. `#D14800` is the lightest orange at the same hue that clears AA, so it stays recognisably the same color. |
| Neutrals (derived) | `ash`: warm grays, hue 55, chroma < 0.014 | Cool grays next to orange look dirty. Warm ones look intentional. |
| Secondary (derived) | `tide`: teal, hue 205 | Complement of orange, for charts, selection and links in dense UIs. |
| Feedback (derived) | `moss` success, `azure` info, `gold` warning (hue 90), `crimson` error (hue 15) | Orange sits between warning and error on the wheel, so both are pushed away from it and never rely on color alone. |
| Type | Inter (UI, prose), JetBrains Mono (code, numbers). Ratio 1.2 from 1rem, plus fluid display tier. | Open-licensed and self-hostable. |
| Spacing | 4px base in `rem`, deliberate gaps, density modes | The data grid needs 28 / 36 / 44px rows. |
| Shape | Radius 4 / 6 / 10 / 16 / pill | Crisp and technical; soft edges only on surfaces. |
| Elevation | Border-first; warm-tinted shadows; dark mode uses surface lightness | Keeps dense UIs like tables quiet. |
| Motion | 100 / 200 / 320ms, ease-out; collapses under reduced motion | Snappy, tool-like. |
| Accessibility | WCAG 2.2 AA, `forced-colors`, visible focus, 44px touch targets | |

### Brand contrast: how the orange passes AA

The original `#FF671F` is **2.91:1 on white**, which fails AA. Rather than work around it, the light-mode brand moves to the nearest orange that passes, **`#D14800`** (ember-500, hue 40, **4.53:1** on white). The original is kept as ember-400 and becomes the brand on dark surfaces, where it is **6.41:1**.

| | Light mode | Dark mode |
|---|---|---|
| `--color-primary` (fill) | ember-500 `#D14800` | ember-400 `#FF671F` |
| `--color-on-primary` (label) | white, 4.53:1 | near-black (ash-950), 6.41:1 |
| Hover / active | darker (ember-600 / 700) | lighter (ember-300 / 200) |
| `--color-text-brand` (orange text) | ember-600, 5.93:1 (also passes on tinted backgrounds) | ember-400, 6.41:1 |

Because the label flips between themes, **always use `bg-brand` with `text-on-brand`**. Never hard-code white or black on the brand fill.

| Do | Don't |
|---|---|
| `bg-brand text-on-brand` | `bg-brand text-white` (breaks in dark mode) |
| `text-brand-fg` for orange links and icons | Orange body text at `ember-400` on a light page (2.91:1) |
| `ember-400` for logos and decorative accents | Treating `ember-400` as a light-mode text color |

## Using it

### Tailwind v4 apps (the intended path)

```css
/* app.css */
@import "tailwindcss";
@import "ember-design-system/tailwind-theme.css";
```

Load the fonts yourself (self-host or `@fontsource-variable/inter` and `@fontsource-variable/jetbrains-mono`).

```html
<html data-theme="dark">            <!-- optional: omit to follow the OS -->
<body class="bg-canvas text-fg font-sans">
  <button class="bg-brand text-on-brand rounded-md h-control-md px-4 focus-ring">Save</button>
  <div data-density="compact"> …grid… </div>
```

`tailwind-theme.css` **removes Tailwind's default palette** (`--color-*: initial`) so only system colors exist. Delete that one line if you want the stock colors too.

Because every utility reads a CSS variable, light/dark switching needs no `dark:` prefixes. A `dark:` variant is provided anyway; it follows both `[data-theme]` and the OS preference.

### Utility cheat sheet

| Token role | Utility |
|---|---|
| `--color-surface`, `-raised`, `-overlay`, `-sunken`, `-hover`, `-selected`, `-inverse` | `bg-canvas`, `bg-raised`, `bg-overlay`, `bg-sunken`, `bg-hover`, `bg-selected`, `bg-inverse` |
| `--color-text-primary / secondary / muted / disabled / inverse` | `text-fg`, `text-fg-muted`, `text-fg-subtle`, `text-fg-disabled`, `text-fg-inverse` |
| `--color-border`, `-strong` | `border-line`, `border-line-strong` |
| `--color-primary` (+ `-hover`, `-active`, `-subtle`), `--color-on-primary`, `--color-text-brand` | `bg-brand` (+ `-hover`, `-active`, `-subtle`), `text-on-brand`, `text-brand-fg` |
| `--color-secondary` family | `bg-tide`, `bg-tide-subtle`, `text-on-tide`, `text-tide-fg` |
| success / warning / error / info | `positive` / `caution` / `critical` / `notice`, each with `bg-{s}`, `bg-{s}-subtle`, `text-{s}-fg`, `text-on-{s}` |
| `--radius-tight / control / container / surface` | `rounded-sm / md / lg / xl` |
| `--shadow-raised / popover / overlay` | `shadow-low / mid / high` |
| `--size-control-*`, `--size-touch-target` | `h-control-sm/md/lg`, `min-h-touch` |
| `--grid-row-height`, `--grid-header-height` | `h-row`, `h-header-row` |
| `--space-page-margin`, `--space-section-gap` | `px-gutter`, `py-section` |
| z-index | `z-(--z-modal)`, `z-(--z-dropdown)`, … (not a Tailwind theme namespace) |

Utility names deliberately differ from the CSS variable names (`bg-canvas`, not `bg-surface`) so a theme entry never shadows the variable it reads from.

### Plain CSS or other frameworks

```css
@import "ember-design-system/tokens.css";
.card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: var(--card-radius); }
```

### Distributing it across your projects

`package.json` exposes the three entry points (`tokens.css`, `tailwind-theme.css`, `tokens.json`). Publish it to npm (rename the package to your scope first), install it from the git repo (`npm i github:<you>/<repo>#v0.1.0`), or use it as a git submodule. Pin versions per project and read the changelog before bumping a major.

## Token architecture

```
primitive  --primitive-ember-500        raw values. Never used in product code.
   ↓
semantic   --color-primary              purpose-based. What apps and Tailwind use.
   ↓
component  --button-primary-bg          per-component decisions. Reference semantic tokens only.
```

**Rules:** no raw values above the primitive layer; every fill that carries text has an `on-*` partner; both themes override *every* color/shadow token that should change; sizes are in `rem`.

### Naming guide

`--{category}-{role}[-{variant}][-{state}]`, kebab-case, same word order everywhere.

| Category | Examples |
|---|---|
| `color-*` | `color-text-primary`, `color-surface-raised`, `color-primary-hover`, `color-on-primary`, `color-success-subtle`, `color-success-text` |
| `space-*`, `size-*` | `space-md`, `space-section-gap`, `size-control-md`, `size-touch-target` |
| `text-*`, `font-*` | `text-h2-size`, `text-body-line`, `font-weight-emphasis`, `font-code` |
| `radius-*`, `shadow-*`, `border-width*` | `radius-control`, `shadow-popover` |
| `motion-*`, `z-*`, `opacity-*`, `focus-ring-*` | `motion-duration`, `z-modal`, `opacity-disabled` |
| `density-*` | `density-row-height` |
| `{component}-{part}-{property}[-{state}]` | `button-primary-bg-hover`, `grid-row-bg-selected`, `input-border-error` |

**Color roles.** For each status (`success`, `warning`, `error`, `info`) and for `primary` / `secondary`: `{role}` is the solid fill, `on-{role}` its label, `{role}-subtle` a tinted background, and `{role}-text` the AA-safe text/icon color on surfaces.

**Scales.** Color: OKLCH, 50-950 per hue, lightness steps tuned per hue, chroma kept inside sRGB. Type: ratio 1.2. Spacing and sizes: 4px base. Breakpoints (documented in `tokens.css`; CSS variables cannot be used in `@media`): sm 640, md 768, lg 1024, xl 1280, 2xl 1536.

### Themes and density

- **Theme:** light by default. Dark applies from `prefers-color-scheme: dark` or `<html data-theme="dark">`. `data-theme="light"` forces light. Set `data-theme` on `<html>`.
- **Density:** `data-density="compact"` or `"comfortable"` on any element. Default is the unmarked middle setting. Touch devices (`pointer: coarse`) always get 44px targets.
- **Motion:** `prefers-reduced-motion` collapses durations to 0.
- **Browser support:** colors use `oklch()`, which matches Tailwind v4's own baseline (Safari 16.4+, Chrome 111+, Firefox 128+). `tokens.json` carries hex values for tools that need them.

## Figma naming map

Figma variables map by replacing `-` with `/` at role boundaries. `tokens.json` already follows this structure, so Tokens Studio imports it directly.

| CSS variable | Figma variable | `tokens.json` path |
|---|---|---|
| `--color-text-primary` | `color/text/primary` | `color.text.primary` |
| `--color-primary` | `color/primary` | `color.primary.$root` |
| `--color-primary-hover` | `color/primary/hover` | `color.primary.hover` |
| `--primitive-ember-500` | `primitive/ember/500` | `primitive.ember.500` |
| `--space-md` | `space/md` | `space.md` |
| `--button-primary-bg-hover` | `button/primary/bg/hover` | `button.primary.bg.hover` |

Compound names stay hyphenated (`font-size`, `font-weight`, `line-height`, `border-width`, `letter-spacing`). Light/dark are Figma **modes** of the same variable; the dark alias lives in `$extensions.mode.dark`. A token that is also a group (`color.primary` and `color.primary.hover`) puts its own value in `$root`.

## Working on the system

```bash
./scripts/check-contrast.sh          # verify WCAG contrast, both themes (needs python3)
python3 scripts/build_tokens_json.py # regenerate tokens.json after editing tokens.css
```

Edit `tokens.css` only; regenerate `tokens.json`, re-run the contrast check and commit `contrast-reports/ember.txt` with the change. The checker resolves `var()` chains, flags undefined tokens and out-of-gamut colors, and exits non-zero on any contrast failure.

## Versioning

Semantic versioning for the token set (`0.1.0`).

- **Major:** renaming or removing a token, or changing a token's meaning.
- **Minor:** adding tokens, components or variants.
- **Patch:** value tweaks that keep every contrast pair passing.
- **Deprecating:** keep the old token for one minor release as an alias to the new one, with a comment, then remove it in the next major.
- **Brand colors:** `#D14800` (`--primitive-ember-500`) and `#FF671F` (`--primitive-ember-400`) never change in a minor or patch release.

## What is derived vs given

Given: the brand color `#FF671F`, adjusted to `#D14800` for AA on white. **Derived** (approved in the direction summary): ash neutrals, tide secondary, moss / gold / crimson / azure feedback hues, the type pairing, spacing, radius, elevation and motion values. Change any of these freely; the contrast check will tell you what you broke.
