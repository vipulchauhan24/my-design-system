#!/usr/bin/env python3
"""Generate tokens.json (W3C DTCG draft format) from tokens.css.

tokens.css is the single source of truth; run this after editing it:

  python3 -I design-system/scripts/build_tokens_json.py

Rules
  - `--primitive-*` tokens carry values; every other token is an alias such as
    "{color.text.primary}" that resolves through the layers.
  - Semantic tokens that change in the dark theme carry
    $extensions.mode.dark with the dark alias.
  - A name that is both a token and a prefix of other tokens (color-primary and
    color-primary-hover) is stored under `$root`, per the DTCG draft.
  - Colors are converted to hex. Values with no DTCG type (shadows, clamp()
    expressions, em letter-spacing, colors with alpha) are kept as CSS strings
    with no $type.
Density overrides ([data-density]) and media queries are CSS-only and are not
exported; the default density values are.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_contrast import parse_color, parse_tokens, to_hex  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HUES = {"ember", "ash", "tide", "moss", "gold", "crimson", "azure"}
COMPOUND = ["font-size", "font-weight", "line-height", "letter-spacing", "border-width"]
ALIAS = re.compile(r"^var\(\s*(--[\w-]+)\s*\)$")


def split_name(name):
    """'--primitive-font-size-2xl' -> ['primitive', 'font-size', '2xl']"""
    s = name[2:]
    for c in COMPOUND:
        s = s.replace(c, c.replace("-", "\0"))
    parts = [p.replace("\0", "-") for p in s.split("-")]
    merged = []  # 0-5 -> '0-5' (spacing half-steps)
    for p in parts:
        if merged and re.fullmatch(r"\d+", p) and re.fullmatch(r"\d+", merged[-1]):
            merged[-1] += "-" + p
        else:
            merged.append(p)
    return merged


def primitive_type(parts, value):
    cat = parts[1]
    if cat in HUES or cat in ("color", "scrim"):
        return "color"
    if cat == "font" and parts[2] in ("sans", "mono"):
        return "fontFamily"
    if cat == "font-weight":
        return "fontWeight"
    if cat == "duration":
        return "duration"
    if cat == "easing":
        return "cubicBezier"
    if cat in ("line-height", "z", "opacity"):
        return "number"
    if cat in ("space", "size", "container", "radius", "border-width", "font-size"):
        return "dimension" if re.fullmatch(r"-?[\d.]+(rem|px)|0", value) else None
    return None


def convert(ptype, value):
    if ptype == "color":
        if "/" in value:
            return value, None  # has alpha: the hex conversion would drop it
        try:
            rgb, _ = parse_color(value)
            return to_hex(rgb)
        except ValueError:
            return value, None  # alpha / unsupported: keep the CSS string, untyped
    if ptype == "fontFamily":
        return [f.strip().strip('"') for f in value.split(",")]
    if ptype in ("fontWeight", "number"):
        return float(value) if "." in value else int(value)
    if ptype == "cubicBezier":
        return [float(x) for x in re.findall(r"[\d.]+", value)]
    if ptype == "dimension" and value == "0":
        return "0rem"
    return value


def main():
    css = (ROOT / "tokens.css").read_text(encoding="utf-8")
    themes = parse_tokens(css)
    light, dark = themes["light"], themes["dark"]

    resolved_type = {}

    def type_of(name):
        if name in resolved_type:
            return resolved_type[name]
        value = light[name]
        m = ALIAS.match(value)
        if m:
            t = type_of(m.group(1))
        else:
            parts = split_name(name)
            t = primitive_type(parts, value) if parts[0] == "primitive" else None
        resolved_type[name] = t
        return t

    def path_of(name):
        return split_name(name)

    paths = {n: path_of(n) for n in light}
    all_paths = {tuple(p) for p in paths.values()}
    prefixes = {tuple(p[:i]) for p in all_paths for i in range(1, len(p))}

    tree = {}

    def put(parts, node):
        cur = tree
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = node

    def ref(name):
        p = paths[name]
        if tuple(p) in prefixes:
            p = p + ["$root"]
        return "{" + ".".join(p) + "}"

    for name, value in light.items():
        parts = list(paths[name])
        if tuple(parts) in prefixes:
            parts.append("$root")
        node = {}
        m = ALIAS.match(value)
        if m:
            node["$value"] = ref(m.group(1))
            t = type_of(name)
            if t:
                node["$type"] = t
        elif parts[0] == "primitive":
            t = type_of(name)
            if t == "color":
                conv = convert("color", value)
                if isinstance(conv, tuple):
                    node["$value"] = conv[0]
                else:
                    node["$value"] = conv
                    node["$type"] = "color"
            else:
                node["$value"] = convert(t, value) if t else value
                if t:
                    node["$type"] = t
        else:
            node["$value"] = value  # raw value outside the primitive layer
        if dark.get(name) != value:
            dm = ALIAS.match(dark[name])
            if dm:
                node.setdefault("$extensions", {}).setdefault("mode", {})["dark"] = ref(dm.group(1))
        put(parts, node)

    out = {
        "$description": "Ember design system tokens (generated from tokens.css; do not edit by hand).",
        **tree,
    }
    (ROOT / "tokens.json").write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote tokens.json ({len(light)} tokens)")


if __name__ == "__main__":
    main()
