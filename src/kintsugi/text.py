"""
Hand-drawn text rendering.

Supports rendering text with a wabi-sabi aesthetic using
bundled Hershey fonts (single-stroke, plottable fonts).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any

import numpy as np


class HersheyFont(Enum):
    """Hershey font variants with different styles."""

    ROMAN = "roman"
    SCRIPT_SIMPLEX = "scriptsx"
    SCRIPT_COMPLEX = "scriptc"
    GOTHIC_ENGLISH = "gothiceng"
    GOTHIC_GERMAN = "gothicger"
    GOTHIC_ITALIAN = "gothicit"


HERSHEY_FONTS: dict[HersheyFont, dict[str, Any]] = {
    HersheyFont.ROMAN: {
        "name": "Hershey Roman",
        "description": "Classic architectural lettering",
    },
    HersheyFont.SCRIPT_SIMPLEX: {
        "name": "Hershey Script Simplex",
        "description": "Casual hand-written style",
    },
    HersheyFont.SCRIPT_COMPLEX: {
        "name": "Hershey Script Complex",
        "description": "More elaborate script",
    },
}


@dataclass
class TextConfig:
    """Configuration for hand-drawn text rendering."""

    font: HersheyFont = HersheyFont.ROMAN
    size: float = 12.0
    letter_spacing: float = 1.0
    word_spacing: float = 2.0
    baseline_offset: float = 0.0
    wobble: float = 0.3


ROMAN_LETTERS: dict[str, list[list[tuple[float, float]]]] = {
    "A": [
        [(0, 0), (0.5, 1), (1, 0)],
        [(0.2, 0.4), (0.8, 0.4)],
    ],
    "B": [
        [
            (0, 1),
            (0, 0),
            (0.6, 0),
            (0.8, 0.2),
            (0.6, 0.4),
            (0, 0.4),
            (0.7, 0.4),
            (0.9, 0.6),
            (0.7, 1),
            (0, 1),
        ],
    ],
    "C": [
        [(0.9, 0.2), (0.7, 0), (0.3, 0), (0, 0.5), (0.3, 1), (0.7, 1), (0.9, 0.8)],
    ],
    "D": [
        [(0, 1), (0, 0), (0.5, 0), (0.9, 0.5), (0.5, 1), (0, 1)],
    ],
    "E": [
        [(0, 1), (0, 0), (0.8, 0)],
        [(0, 0.5), (0.6, 0.5)],
        [(0, 1), (0.8, 1)],
    ],
    "F": [
        [(0, 1), (0, 0), (0.8, 0)],
        [(0, 0.5), (0.6, 0.5)],
    ],
    "G": [
        [
            (0.9, 0.2),
            (0.7, 0),
            (0.3, 0),
            (0, 0.5),
            (0.3, 1),
            (0.7, 1),
            (0.9, 0.8),
            (0.9, 0.5),
            (0.5, 0.5),
        ],
    ],
    "H": [
        [(0, 1), (0, 0)],
        [(1, 1), (1, 0)],
        [(0, 0.5), (1, 0.5)],
    ],
    "I": [
        [(0.2, 1), (0.8, 1)],
        [(0.5, 1), (0.5, 0)],
        [(0.2, 0), (0.8, 0)],
    ],
    "J": [
        [(0.2, 1), (0.8, 1)],
        [(0.5, 1), (0.5, 0.2), (0.3, 0), (0, 0.2)],
    ],
    "K": [
        [(0, 1), (0, 0)],
        [(0.8, 1), (0, 0.5), (0.8, 0)],
    ],
    "L": [
        [(0, 1), (0, 0), (0.8, 0)],
    ],
    "M": [
        [(0, 0), (0, 1), (0.5, 0.5), (1, 1), (1, 0)],
    ],
    "N": [
        [(0, 0), (0, 1), (1, 0), (1, 1)],
    ],
    "O": [
        [(0.2, 0), (0, 0.5), (0.2, 1), (0.8, 1), (1, 0.5), (0.8, 0), (0.2, 0)],
    ],
    "P": [
        [(0, 0), (0, 1), (0.7, 1), (0.9, 0.8), (0.7, 0.5), (0, 0.5)],
    ],
    "Q": [
        [(0.2, 0), (0, 0.5), (0.2, 1), (0.8, 1), (1, 0.5), (0.8, 0), (0.2, 0)],
        [(0.6, 0.5), (1, 0)],
    ],
    "R": [
        [
            (0, 0),
            (0, 1),
            (0.7, 1),
            (0.9, 0.8),
            (0.7, 0.5),
            (0, 0.5),
            (0.8, 0.5),
            (1, 0),
        ],
    ],
    "S": [
        [
            (0.9, 0.2),
            (0.7, 0),
            (0.3, 0),
            (0.1, 0.2),
            (0.3, 0.5),
            (0.7, 0.5),
            (0.9, 0.8),
            (0.7, 1),
            (0.3, 1),
            (0.1, 0.8),
        ],
    ],
    "T": [
        [(0, 1), (1, 1)],
        [(0.5, 1), (0.5, 0)],
    ],
    "U": [
        [(0, 1), (0, 0.2), (0.3, 0), (0.7, 0), (1, 0.2), (1, 1)],
    ],
    "V": [
        [(0, 1), (0.5, 0), (1, 1)],
    ],
    "W": [
        [(0, 1), (0.25, 0), (0.5, 0.6), (0.75, 0), (1, 1)],
    ],
    "X": [
        [(0, 1), (1, 0)],
        [(0, 0), (1, 1)],
    ],
    "Y": [
        [(0, 1), (0.5, 0.5)],
        [(1, 1), (0.5, 0.5)],
        [(0.5, 0.5), (0.5, 0)],
    ],
    "Z": [
        [(0, 1), (1, 1), (0, 0), (1, 0)],
    ],
    "0": [
        [(0.2, 0), (0, 0.5), (0.2, 1), (0.8, 1), (1, 0.5), (0.8, 0), (0.2, 0)],
    ],
    "1": [
        [(0.3, 0.2), (0.5, 0), (0.5, 0), (0.5, 1)],
    ],
    "2": [
        [(0, 0.2), (0.3, 0), (0.7, 0), (1, 0.3), (0, 1), (1, 1)],
    ],
    "3": [
        [
            (0, 0.8),
            (0.4, 0.6),
            (0.8, 0.6),
            (0.6, 0.5),
            (0.8, 0.4),
            (0.4, 0.4),
            (0.6, 0.4),
            (0.9, 0.2),
            (0.7, 0),
            (0.3, 0),
            (0, 0.2),
        ],
    ],
    "4": [
        [(0.7, 1), (0.7, 0), (0, 0.7), (1, 0.7)],
    ],
    "5": [
        [
            (1, 1),
            (0, 1),
            (0, 0.5),
            (0.7, 0.5),
            (0.9, 0.3),
            (0.7, 0),
            (0.3, 0),
            (0.1, 0.2),
        ],
    ],
    "6": [
        [
            (0.8, 0.2),
            (0.6, 0),
            (0.2, 0),
            (0, 0.5),
            (0.2, 1),
            (0.8, 1),
            (1, 0.5),
            (0.8, 0.5),
            (0.2, 0.5),
        ],
    ],
    "7": [
        [(0, 1), (1, 1), (0.3, 0)],
    ],
    "8": [
        [(0.3, 0), (0, 0.5), (0.3, 1), (0.7, 1), (1, 0.5), (0.7, 0), (0.3, 0)],
        [(0.7, 0), (0.9, 0.5), (0.7, 1)],
    ],
    "9": [
        [(0.2, 1), (0.4, 1), (1, 1), (1, 0.5), (0.8, 0), (0.2, 0), (0.3, 0.5)],
    ],
    "-": [
        [(0.2, 0.5), (0.8, 0.5)],
    ],
    "/": [
        [(0.2, 1), (0.8, 0)],
    ],
    '"': [
        [(0.2, 0.9), (0.2, 0.7)],
        [(0.8, 0.9), (0.8, 0.7)],
    ],
    "'": [
        [(0.5, 1), (0.5, 0.7)],
    ],
}


class HandTextRenderer:
    """Renders text with a hand-drawn wabi-sabi aesthetic."""

    def __init__(self, config: TextConfig | None = None):
        self.config = config or TextConfig()

    def _wobble_point(
        self,
        x: float,
        y: float,
        seed: int,
    ) -> tuple[float, float]:
        """Apply small random wobble to a point."""
        np.random.seed(seed)
        dx = (np.random.random() - 0.5) * self.config.wobble
        dy = (np.random.random() - 0.5) * self.config.wobble
        return (x + dx, y + dy)

    def render_character(
        self,
        char: str,
        x: float,
        y: float,
        seed: int = 0,
    ) -> list[list[tuple[float, float]]]:
        """Render a single character as stroke paths."""
        char_upper = char.upper()
        if char_upper not in ROMAN_LETTERS:
            return []

        strokes = ROMAN_LETTERS[char_upper]
        scale = self.config.size / 12.0

        rendered = []
        for stroke in strokes:
            path = []
            for px, py in stroke:
                sx = x + px * scale
                sy = y - py * scale + scale
                sx, sy = self._wobble_point(sx, sy, seed)
                path.append((sx, sy))
            rendered.append(path)

        return rendered

    def render_text(
        self,
        text: str,
        x: float,
        y: float,
    ) -> list[list[tuple[float, float]]]:
        """Render a string of text as stroke paths."""
        scale = self.config.size / 12.0
        spacing = scale * self.config.letter_spacing

        all_strokes = []
        current_x = x
        char_seed = 0

        for char in text:
            if char == " ":
                current_x += spacing * 2
                continue

            strokes = self.render_character(char, current_x, y, seed=char_seed)
            all_strokes.extend(strokes)

            current_x += spacing * 1.5
            char_seed += 1

        return all_strokes
