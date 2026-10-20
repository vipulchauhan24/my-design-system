# My Design Systems

A collection of self-contained design systems. Each one lives in its own folder and ships tokens, component specs and a preview.

| Design system | Folder | Stack | Preview |
|---|---|---|---|
| Ember | [`Ember/`](Ember/) | Tailwind v4 or plain CSS | [`Ember/preview.html`](Ember/preview.html) |

[`index.html`](index.html) is a landing page that links to every preview.

## Contents

- [Using a design system](#using-a-design-system)
- [Folder convention](#folder-convention)
- [Scripts](#scripts)

## Using a design system

These design systems are not published as packages. Clone this repo and copy or reference the folder you need.

To use one with an AI skill, share this repo's URL and the design system's folder name (for example `Ember`) with the skill, and tell it to follow that folder's `README.md` and `components.md`.

## Folder convention

Every design system folder has the same shape, so one skill can work with any of them.

| File | Purpose |
|---|---|
| `README.md` | Direction, color and contrast rules, naming guide, do/don't tables |
| `components.md` | Component specs: variants, sizes, states, tokens, markup |
| `tailwind-theme.css` | Tailwind utilities. Its header comment is a compact cheat sheet of every utility. |
| `tokens.css` | Source of truth for all tokens |
| `tokens.json` | Generated export for Figma and Style Dictionary. Do not edit by hand. |
| `preview.html` | Visual reference page |

Contrast reports are kept at the repo root in [`contrast-reports/`](contrast-reports/), one file per design system (for example `ember.txt`).

## Scripts

Shared tooling in [`scripts/`](scripts/). It requires `python3`. Each script takes one argument: the path to the design system folder to work on. It reads that folder's `tokens.css`.

| File | What it does |
|---|---|
| [`check_contrast.py`](scripts/check_contrast.py) | The contrast engine. Parses a `tokens.css`, resolves `var()` chains for the light and dark themes, converts colors to sRGB and computes WCAG contrast ratios for the foreground/background pairs it is given. It also flags undefined tokens and out-of-gamut colors, and exits non-zero if any pair fails. It does not decide which pairs to check. |
| [`check-contrast.sh`](scripts/check-contrast.sh) | The contrast policy. Holds the list of token pairs that must pass (text on each surface, brand text on tints, status text on its tint, focus ring on surfaces) with their minimum ratios (4.5:1 for text, 3:1 for non-text UI). It passes that list to `check_contrast.py`, prints the result and writes it to `contrast-reports/<name>.txt` (overwriting any existing report). |
| [`build_tokens_json.py`](scripts/build_tokens_json.py) | Generates `tokens.json` (W3C DTCG format) from `tokens.css`. Primitive tokens carry values, every other token is an alias, and dark-theme overrides go under `$extensions.mode.dark`. It reuses the CSS parser from `check_contrast.py`. |

### Examples

Run from the repo root:

```bash
# Check WCAG contrast for both themes, print the result and write contrast-reports/ember.txt
# (exits non-zero on any failure; the report is written either way)
./scripts/check-contrast.sh Ember

# Regenerate Ember/tokens.json after editing Ember/tokens.css
python3 -I scripts/build_tokens_json.py Ember

# Run the contrast engine directly with only its built-in default pairs
python3 -I scripts/check_contrast.py Ember
```

The pair list in `check-contrast.sh` uses Ember's token names. A design system with different semantic color names needs its own list.
