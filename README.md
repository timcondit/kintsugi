# kintsugi

**Wabi-sabi engineering drawings for woodworking.**

A purpose-built Python CAD drawing engine that creates hand-drawn aesthetic 2D engineering drawings from 3D models while maintaining precision for Japanese joinery.

## Philosophy

Traditional CAD drawings prioritize geometric perfection. Kintsugi embraces **wabi-sabi** — finding beauty in imperfection. Lines have subtle organic wobble. Text has hand-drawn character. Yet dimensions remain precise to 1/16" tolerances.

The name comes from [kintsugi](https://en.wikipedia.org/wiki/Kintsugi), the Japanese art of repairing broken pottery with gold — highlighting rather than hiding the marks of use and time.

## Features

- **Wabi-sabi line rendering** — organic noise-based perturbation baked into geometry
- **Hand-drawn text** — Hershey-style single-stroke fonts with slight wobble
- **Shop fraction dimensions** — 1 3/4", 5/8", etc. (not decimals)
- **Warm aesthetic** — sepia ink palette on cream background
- **Precision** — visual imperfection doesn't affect actual measurements

## Installation

```bash
pip install kintsugi
```

## Quick Start

```python
from build123d import Box, export_svg
from kintsugi import WabiSketch, Drawing
from kintsugi.export import render_to_svg

# Create a simple 3D model
with BuildPart() as part:
    Box(2, 1, 0.75)

# Apply wabi-sabi effect
wabi = WabiSketch()
drawing = Drawing()

# Add sketch paths with wabi-sabi effect
# (simplified - real usage would project 3D → 2D first)
drawing.add_sketch_path(wabi.sketch_line(50, 50, 200, 50))
drawing.add_sketch_path(wabi.sketch_line(200, 50, 200, 150))
drawing.add_sketch_path(wabi.sketch_path(200, 150, 50, 150))
drawing.add_sketch_path(wabi.sketch_line(50, 150, 50, 50))

# Add dimension
drawing.add_dimension(50, 50, 200, 50, label='2"')

# Export to SVG
svg = render_to_svg(drawing)
```

## Project Structure

```
kintsugi/
├── src/kintsugi/
│   ├── __init__.py
│   ├── engine.py          # CAD engine abstraction
│   ├── sketch.py          # Wabi-sabi line generation
│   ├── text.py            # Hand-drawn text rendering
│   ├── drawing.py         # Drawing composition
│   └── export/
│       └── svg.py         # SVG serialization
├── tests/
├── pyproject.toml
└── README.md
```

## License

Apache 2.0
