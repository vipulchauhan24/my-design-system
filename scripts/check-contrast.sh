#!/usr/bin/env bash
# Verifies WCAG contrast (text 4.5:1, non-text UI 3:1) for both themes.
# Run from anywhere:  ./scripts/check-contrast.sh [--hex]
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
css="$here/../tokens.css"

pairs=()
add() { pairs+=(--pair "--color-$1" "--color-$2" "$3"); }

# Text on every surface it can sit on
for fg in text-primary text-secondary text-muted; do
  for bg in surface-sunken surface-hover surface-selected; do add "$fg" "$bg" 4.5; done
done
for bg in surface surface-raised surface-selected primary-subtle; do add text-brand "$bg" 4.5; done
add text-inverse surface-inverse 4.5

# Secondary
add on-secondary secondary 4.5
add on-secondary secondary-hover 4.5
add on-secondary secondary-active 4.5
for bg in surface secondary-subtle; do add secondary-text "$bg" 4.5; done

# Feedback: accessible text on surface and on its own tint; label on hover fill
for s in success warning error info; do
  for bg in surface "$s-subtle"; do add "$s-text" "$bg" 4.5; done
done
add on-error error-hover 4.5

# Non-text UI: the brand fill itself must pass as text (4.5) on white and as UI (3) on raised
# surfaces; input error border; focus ring on every surface
add primary surface 4.5
add primary surface-raised 3.0
add error surface 3.0
add focus-ring surface-raised 3.0
add focus-ring surface-selected 3.0
add border-strong surface-raised 3.0

exec python3 -I "$here/check_contrast.py" "$css" "${pairs[@]}" "$@"
