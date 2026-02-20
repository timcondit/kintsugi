# kintsugi Specification

**Version:** 0.1.0\
**Status:** Draft

## Overview

kintsugi is a purpose-built Python CAD drawing engine that creates hand-drawn aesthetic 2D engineering drawings from 3D models while maintaining precision for Japanese joinery.

## Design Principles

1. **Wabi-sabi aesthetics** — Lines have subtle organic wobble, text has hand-drawn character
2. **Precision preserved** — Visual imperfection doesn't affect actual measurements
3. **Shop-friendly output** — Dimensions in fractions (1 3/4"), not decimals
4. **Pythonic** — Clean, functional code following modern Python patterns

## Core Components

### 1. CAD Engine Abstraction (`engine.py`)

**Purpose:** Abstract the underlying CAD library (build123d) behind a unified interface.

```python
class CADEngine(ABC):
    def project_3d_to_2d(part, view="front") -> Sketch: ...
    def get_edges(part) -> list: ...
    def get_faces(part) -> list: ...

class Build123dEngine(CADEngine):
    """build123d implementation."""
```

**Status:** Basic implementation exists.

### 2. Wabi-Sabi Sketch Generation (`sketch.py`)

**Purpose:** Apply organic noise-based perturbation to create hand-drawn aesthetic.

```python
@dataclass
class SketchConfig:
    noise_scale: float = 0.02      # Spatial frequency of noise
    noise_amplitude: float = 1.5   # Maximum displacement in pixels
    seed: int | None = None        # Reproducibility

class WabiSketch:
    def sketch_line(x1, y1, x2, y2) -> list[Point]: ...
    def sketch_circle(cx, cy, radius) -> list[Point]: ...
    def sketch_arc(...) -> list[Point]: ...
```

**Implementation:**

- Uses simplex noise for organic variation
- Perturbs points perpendicular to line direction
- Bakes effect into geometry (not render-time)

**Status:** Basic implementation exists.

### 3. Hand-Drawn Text (`text.py`)

**Purpose:** Render text with hand-drawn aesthetic using single-stroke fonts.

```python
class HersheyFont(Enum):
    ROMAN = "roman"           # Classic architectural
    SCRIPT_SIMPLEX = "scriptsx"  # Casual handwritten

@dataclass  
class TextConfig:
    font: HersheyFont = HersheyFont.ROMAN
    size: float = 12.0
    letter_spacing: float = 1.0
    wobble: float = 0.3

class HandTextRenderer:
    def render_character(char, x, y) -> list[Stroke]: ...
    def render_text(text, x, y) -> list[Stroke]: ...
```

**Implementation:**

- Bundled Hershey font stroke data (subset of Roman)
- Applies small random wobble to vertices
- Single-stroke rendering (no fill)

**Status:** Basic implementation with limited character set.

### 4. Drawing Composition (`drawing.py`)

**Purpose:** Compose complete drawings with dimensions, hatching, annotations.

```python
@dataclass
class Drawing:
    width: float = 500
    height: float = 380
    background: str = "#f5f0e8"  # cream
    
    dimensions: list[Dimension] = []
    callouts: list[Callout] = []
    hatches: list[HatchRegion] = []
    centerlines: list[CenterLine] = []
    sketch_paths: list[Path] = []
    text_paths: list[Path] = []
    labels: list[Label] = []
```

**Components:**

- `Dimension` — Linear dimensions with arrows and shop-fraction labels
- `Callout` — Numbered bubbles (①, ②, ③) for feature callouts
- `HatchRegion` — Diagonal hatching for cut/waste surfaces
- `CenterLine` — Dash-dot center lines

**Status:** Full implementation exists.

### 5. SVG Export (`export/svg.py`)

**Purpose:** Serialize Drawing to SVG format.

```python
def render_to_svg(drawing: Drawing) -> str: ...
```

**Output:**

- SVG 1.1 compliant
- Warm color palette (sepia/cream)
- Configurable stroke widths
- Stroke-linecap: round for organic feel

**Status:** Full implementation exists.

## Color Palette

| Name      | Hex     | Usage                     |
| --------- | ------- | ------------------------- |
| ink       | #3a2a1a | Primary strokes (darkest) |
| brown     | #6b3a1f | Secondary strokes         |
| amber     | #b5651d | Dimensions, callouts      |
| tan       | #c8934a | Highlights                |
| cream     | #f5f0e8 | Background                |
| parchment | #ede5d4 | Hatch fill                |
| hatch     | #8b5a2b | Hatch strokes             |

## Stroke Weights

| Name          | Width  | Usage                 |
| ------------- | ------ | --------------------- |
| STROKE_HEAVY  | 1.8px  | Main outlines         |
| STROKE_MEDIUM | 1.2px  | Secondary, dimensions |
| STROKE_LIGHT  | 0.75px | Hatching, dashes      |

## Future Considerations

### Phase 2

- DXF export (for CAM/CNC)
- PDF export (for documentation)
- More Hershey fonts
- Dimension tolerances (1/16" precision)

### Phase 3

- 3D viewing/integration
- More projection views
- Automatic dimension detection

## Dependencies

- `build123d >= 0.10.0` — CAD kernel
- `numpy >= 1.26` — Noise generation

## Testing

Test structure mirrors source:

- `tests/test_sketch.py` → `kintsugi/sketch.py`
- `tests/test_text.py` → `kintsugi/text.py`
- etc.

Run tests with:

```bash
pytest
```

## License

Apache 2.0
