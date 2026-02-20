# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Kintsugi is a library for generating wabi-sabi engineering drawings for woodworking. It provides tools for creating clean, precise technical drawings with a focus on simplicity and elegance — honoring the Japanese aesthetic of finding beauty in imperfection.

> **Note**: This library is part of the Woodcraft CAD ecosystem. It may be integrated with WoodCAD in the future.

## Product Vision

Kintsugi produces clean, minimal engineering drawings that:

- Respect the materials and craft
- Focus on essential information
- Have a quiet, unobtrusive aesthetic
- Work well for both screen and print

### Design Principles

**1. Simplicity Over Completeness**

- Each drawing should show only what's necessary
- Avoid clutter; let the drawing breathe
- Use white space as a design element

**2. Precision Without Sterility**

- Exact measurements and proportions
- Clean lines, intentional strokes
- Technical accuracy with aesthetic warmth

**3. Flexibility Within Constraints**

- Support multiple output formats (SVG initially)
- Allow customization of style while maintaining coherence
- Work at various scales and contexts

## Architecture

### Core Modules (`src/kintsugi/`)

- `__init__.py` — Package exports
- `text.py` — Text rendering utilities (shop fractions, dimension labels)
- `sketch.py` — 2D sketch primitives (lines, arcs, Bézier curves)
- `drawing.py` — Drawing composition and layout
- `engine.py` — Core rendering engine using build123d
- `export/` — Export handlers
  - `__init__.py` — Export base classes
  - `svg.py` — SVG output generation

### Design Tokens

**Dimensions:**

- Default units: inches (imperial)
- Internal storage: float/inches
- Display: shop fractions via `to_shop_fraction()`

**SVG Style Defaults:**

- Stroke colors: `#2d2d2d` (dark charcoal)
- Fill: `none` or `#fafafa` (warm white)
- Stroke widths: `0.5px` (hairline), `1px` (standard), `2px` (emphasis)
- Font: System sans-serif, small and unobtrusive

## Quick Reference

Common commands — see `AGENTS.md` for the full list and style guidelines.

```bash
just dev        # install dependencies
just test       # run tests
just test-fast  # fast tests only (pre-commit subset)
just format     # ruff + taplo + dprint
just lint       # check all linters
```

## Project Structure

```
kintsugi/
├── src/kintsugi/
│   ├── __init__.py              # Package exports
│   ├── text.py                  # Text rendering (fractions, labels)
│   ├── sketch.py                # 2D sketch primitives
│   ├── drawing.py               # Drawing composition
│   ├── engine.py                # Core rendering engine
│   └── export/
│       ├── __init__.py          # Export base classes
│       └── svg.py               # SVG output
├── tests/                       # pytest test suite
├── AGENTS.md                    # Coding guidelines for AI agents
├── CLAUDE.md                    # This file
├── justfile                     # Command runner recipes
└── pyproject.toml               # Python package config
```

## Known Issues

- No rendering/display tests (would require display environment)
- Some LSP errors for build123d and numpy (libraries without full stubs)
