# field_guide.zip (Field Medic Ledger — DIY Commune)

Open `index.html` to start.

## Modular / Plug & Play
- `data-include="path/to/partial.html"` injects components at runtime.
- Swap content without touching shells:
  - `components/chapters/chNN_left.html`
  - `components/chapters/chNN_right.html`
  - `components/drawers/chNN_drawer.html`
- Concept sections are standalone:
  - `components/sections/*.html`

## Pages
- `index.html` map (pan/zoom + hotspots built from manifest)
- `concept.html` concept docs hub
- `chapter-1.html` ... `chapter-10.html`

## Keys
- Map: drag pan, scroll zoom, `R` reset
- Chapters: `D` drawer toggle

## Build-time precompiler (bake includes → standalone HTML)
Authoring uses runtime `data-include` for plug & play modules.
For GitHub Pages and file:// reliability, bake includes into `dist/`:

```bash
python tools/build.py
python -m http.server 8000 --directory dist
```

Or:

```bash
npm run build
npm run serve:dist
```

Deploy the `dist/` folder (no fetch required).

