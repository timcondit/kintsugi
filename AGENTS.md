# AGENTS.md

Guidelines for agentic coding agents working with the Kintsugi codebase.

> **New developers**: Start with README.md for overview and setup.

## Build Commands

**Package Manager**: `uv` (modern Python package manager)

```bash
# Install dependencies and editable package
just dev

# Run all tests
just test
# or
uv run pytest

# Run fast tests only (pre-commit subset)
just test-fast

# Run tests with coverage report
just coverage

# Run mypy type checking
just typecheck

# Format code
just format

# Run all linters
just lint

# Check conventional commits
just check-commits

# Bump version and generate changelog
just release

# Clean Python cache
just clean
```

**Note**: Code formatting is automatically applied by the [pre-commit](https://pre-commit.com/) hook. Manual formatting via `just format` also runs TOML (taplo) and Markdown (dprint) formatters.

## Code Style Guidelines

### Imports

- Standard library first, then third-party, then local imports
- Use absolute imports from `kintsugi.*`
- Import specific items when possible
- For large import groups from single modules: `from build123d import *` (acceptable for CAD modules)

### Python Standards

- **Python Version**: 3.12+ (see pyproject.toml)
- **Type Hints**: Use extensively with `from typing import Optional, Dict, List, Any`
- **String Formatting**: Prefer f-strings over .format() or %
- **Line Length**: 88 characters (ruff default)

### Naming Conventions

- **Classes**: PascalCase (`Drawing`, `SVGExporter`)
- **Functions/Methods**: snake_case (`generate_svg`, `render_sketch`)
- **Variables**: snake_case (`stroke_width`, `line_color`)
- **Constants**: SCREAMING_SNAKE_CASE (`DEFAULT_DPI`, `MM_PER_INCH`)
- **Private**: Leading underscore (`_cached_path`, `_render_element`)

### Functional Programming (Preferred for New Code)

For new drawing and calculation code, prefer functional style to improve testability and correctness.

**When to use functional style:**

- SVG generation and rendering
- Dimension calculations
- Pure calculation logic (input → output, no side effects)
- Utility functions and helpers

**When to use OOP:**

- Complex rendering pipelines with lifecycle
- Configuration objects
- Export format handlers

**Functional patterns to prefer:**

```python
# ✓ GOOD: Pure function with explicit inputs/outputs
def calculate_dimension(
    measurement: float,
    scale: float,
    units: str = "in"
) -> float:
    """Calculate scaled dimension in specified units."""
    return measurement * scale

# ✓ GOOD: Frozen dataclass for immutable data
from dataclasses import dataclass

@dataclass(frozen=True)
class BoundingBox:
    """Immutable bounding box for 2D drawings."""
    x: float
    y: float
    width: float
    height: float
    
    def scale(self, factor: float) -> "BoundingBox":
        """Returns new instance scaled by factor."""
        return BoundingBox(
            x=self.x * factor,
            y=self.y * factor,
            width=self.width * factor,
            height=self.height * factor,
        )
```

**Guidelines:**

- **No mutation**: Avoid modifying inputs or shared state; return new values
- **Explicit dependencies**: Pass all required data as parameters, no hidden globals
- **Type hints**: Always annotate inputs, outputs, and return types
- **Composition**: Build complex operations from small, tested functions
- **Referential transparency**: Same inputs always produce same outputs (no randomness, no I/O)

### Error Handling

```python
# Prefer specific exceptions
try:
    drawing = Drawing.from_file(path)
except ValueError as e:
    logger.error(f"Invalid drawing file: {e}")
    raise

# Use Optional types instead of None checking
def get_layer(name: str) -> Optional[Layer]:
    return self.layers.get(name)
```

### Documentation

- Use docstrings for all public methods and classes
- Follow Google/NumPy docstring format
- Include type information and examples for complex rendering operations
- Document coordinate system conventions

### Geometry Code (build123d)

- Use context managers for CAD operations: `with BuildPart() as obj:`
- Cache expensive geometry calculations as properties
- Prefer imperial units (inches) throughout the system
- Document coordinate system assumptions in comments

### Testing

- Test files mirror source structure: `tests/test_sketch.py` for `core/sketch.py`
- Use descriptive test names: `test_bounding_box_scaling`
- Use pytest fixtures for complex setup (see `tests/conftest.py`)
- Test both "dumb" (data structures) and "smart" (rendering) behavior
- Use `pytest.approx()` for floating-point comparisons

#### Test Markers

Use pytest markers to categorize tests for selective execution:

```python
import pytest

@pytest.mark.slow
def test_complex_svg_generation():
    """Tests that take > 1s should be marked slow."""
    pass
```

**Available markers:**

- `slow` - Tests taking > 1 second (complex rendering, large datasets)

**Test commands:**

```bash
just test              # All tests
just test-fast         # Fast tests only (pre-commit subset)
uv run pytest -m slow  # Slow tests only
```

**Pre-commit behavior:** Runs `just test-fast` automatically (excludes slow)

## Git Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

**Format:** `<type>[optional scope]: <description>`

**Common types:**

- `feat:` - New feature (correlates with MINOR in semver)
- `fix:` - Bug fix (correlates with PATCH in semver)
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic changes)
- `refactor:` - Code restructuring (no behavior changes)
- `test:` - Adding or updating tests
- `build:` - Build system or dependency changes
- `chore:` - Maintenance tasks

**Examples:**

- `feat: Add SVG export for 2D drawings`
- `fix(sketch): Handle None values in layer rendering`
- `docs: Update AGENTS.md with git conventions`
- `refactor: Extract dimension calculation into separate module`

**Commit body guidelines:**

- Focus on "why" rather than "what" (code shows "what")
- Keep first line under 72 characters
- Use present tense ("Add feature" not "Added feature")
- Reference issues when relevant: `Fixes #123`

**Enforcement:**

- Git hooks managed via [pre-commit](https://pre-commit.com/)
- Commit messages validated automatically using [cocogitto](https://docs.cocogitto.io/)
- Manual validation: `just check-commits` or `cog check HEAD~10..HEAD`
- Manual hook execution: `pre-commit run --all-files`

## Maintaining These Files

`AGENTS.md` and `CLAUDE.md` serve different tools and must stay non-overlapping:

- **`AGENTS.md`** — read by Codex and Claude Code. Contains working rules: commands,
  style, conventions, patterns. Update when workflows or tooling change.
- **`CLAUDE.md`** — read by Claude Code only (Codex does not read it). Contains project
  understanding: vision, architecture, design decisions, terminology. Update when the
  system itself changes.

A pre-commit hook (`check-doc-scope`) enforces this boundary by detecting forbidden
section headings in each file. If your commit is blocked, move the offending section
to the correct file — do not rename the heading to bypass the check.
