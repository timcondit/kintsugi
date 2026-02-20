"""
Drawing composition.

Handles composition of 2D drawings including dimensions,
hatching, and annotation layers.
"""

from dataclasses import dataclass, field
from decimal import Decimal
from fractions import Fraction
from typing import Literal


PALETTE = {
    "ink": "#3a2a1a",
    "brown": "#6b3a1f",
    "amber": "#b5651d",
    "tan": "#c8934a",
    "cream": "#f5f0e8",
    "parchment": "#ede5d4",
    "linen": "#e8dcc8",
    "hatch": "#8b5a2b",
}

STROKE_HEAVY = "1.8"
STROKE_MEDIUM = "1.2"
STROKE_LIGHT = "0.75"


def to_shop_fraction(value: float, precision: int = 16) -> str:
    """
    Format a decimal inch value as a shop fraction string.

    Examples:
        0.625  → 5/8"
        1.75   → 1 3/4"
        3.0    → 3"
    """
    if value < 0:
        return f"-{to_shop_fraction(-value, precision)}"
    d = Decimal(str(round(value, 6)))
    whole = int(d)
    frac_val = d - whole
    if frac_val == 0:
        return f'{whole}"'
    frac = Fraction(frac_val).limit_denominator(precision)
    if frac.numerator == frac.denominator:
        return f'{whole + 1}"'
    if whole == 0:
        return f'{frac.numerator}/{frac.denominator}"'
    return f'{whole} {frac.numerator}/{frac.denominator}"'


@dataclass
class Dimension:
    """A linear dimension with arrows and label."""

    x1: float
    y1: float
    x2: float
    y2: float
    label: str = ""
    offset: float = 12.0
    side: Literal["left", "right", "above", "below"] = "above"


@dataclass
class Callout:
    """A numbered callout bubble."""

    x: float
    y: float
    number: int
    radius: float = 10.0


@dataclass
class HatchRegion:
    """A rectangular hatching region."""

    x: float
    y: float
    width: float
    height: float
    angle_deg: float = 45.0
    spacing: float = 6.0


@dataclass
class CenterLine:
    """A dash-dot center line."""

    x1: float
    y1: float
    x2: float
    y2: float


@dataclass
class Drawing:
    """A complete 2D drawing composition."""

    width: float = 500
    height: float = 380
    background: str = PALETTE["cream"]

    dimensions: list[Dimension] = field(default_factory=list)
    callouts: list[Callout] = field(default_factory=list)
    hatches: list[HatchRegion] = field(default_factory=list)
    centerlines: list[CenterLine] = field(default_factory=list)

    sketch_paths: list[list[tuple[float, float]]] = field(default_factory=list)
    text_paths: list[list[tuple[float, float]]] = field(default_factory=list)
    labels: list[tuple[str, float, float, str]] = field(default_factory=list)

    def add_dimension(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        label: str = "",
    ) -> "Drawing":
        """Add a dimension line."""
        self.dimensions.append(Dimension(x1, y1, x2, y2, label))
        return self

    def add_callout(
        self,
        x: float,
        y: float,
        number: int,
    ) -> "Drawing":
        """Add a callout bubble."""
        self.callouts.append(Callout(x, y, number))
        return self

    def add_hatch(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
    ) -> "Drawing":
        """Add a hatch region."""
        self.hatches.append(HatchRegion(x, y, width, height))
        return self

    def add_centerline(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> "Drawing":
        """Add a center line."""
        self.centerlines.append(CenterLine(x1, y1, x2, y2))
        return self

    def add_sketch_path(
        self,
        path: list[tuple[float, float]],
    ) -> "Drawing":
        """Add a wabi-sabi sketch path."""
        self.sketch_paths.append(path)
        return self

    def add_text_path(
        self,
        path: list[tuple[float, float]],
    ) -> "Drawing":
        """Add a text stroke path."""
        self.text_paths.append(path)
        return self

    def add_label(
        self,
        text: str,
        x: float,
        y: float,
        style: str = "dimension",
    ) -> "Drawing":
        """Add a text label."""
        self.labels.append((text, x, y, style))
        return self
