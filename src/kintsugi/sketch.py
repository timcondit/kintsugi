"""
Wabi-sabi sketch generation.

Applies organic noise-based perturbation to lines and curves
to create a hand-drawn aesthetic while preserving precision.
"""

from dataclasses import dataclass
import math

import numpy as np


@dataclass
class SketchConfig:
    """Configuration for wabi-sabi sketch effect."""

    noise_scale: float = 0.02
    noise_amplitude: float = 1.5
    seed: int | None = None


def simplex_noise_2d(x: float, y: float, seed: int | None = None) -> float:
    """Generate 2D simplex-like noise for coordinates."""
    vec = np.array([x, y])
    return float(np.sin(vec[0] * 12.9898 + vec[1] * 78.233) * 43758.5453 % 1)


def perturb_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    config: SketchConfig,
) -> list[tuple[float, float]]:
    """
    Apply wabi-sabi perturbation to a line segment.

    Returns a polyline with intermediate points that have
    noise applied perpendicular to the line direction.
    """
    dx = x2 - x1
    dy = y2 - y1
    length = math.hypot(dx, dy)

    if length < 0.001:
        return [(x1, y1), (x2, y2)]

    nx = -dy / length
    ny = dx / length

    num_points = max(3, int(length * 20))

    points = []
    for i in range(num_points + 1):
        t = i / num_points
        base_x = x1 + dx * t
        base_y = y1 + dy * t

        noise_val = simplex_noise_2d(
            base_x * config.noise_scale + t,
            base_y * config.noise_scale,
            config.seed,
        )

        offset = noise_val * config.noise_amplitude

        points.append(
            (
                base_x + nx * offset,
                base_y + ny * offset,
            )
        )

    return points


def perturb_circle(
    cx: float,
    cy: float,
    radius: float,
    config: SketchConfig,
    num_points: int = 60,
) -> list[tuple[float, float]]:
    """Apply wabi-sabi perturbation to a circle."""
    points = []
    for i in range(num_points):
        angle = (i / num_points) * 2 * math.pi

        noise_val = simplex_noise_2d(
            cx * config.noise_scale + math.cos(angle),
            cy * config.noise_scale + math.sin(angle),
            config.seed,
        )

        r = radius + noise_val * config.noise_amplitude

        points.append(
            (
                cx + r * math.cos(angle),
                cy + r * math.sin(angle),
            )
        )

    return points


class WabiSketch:
    """Applies wabi-sabi perturbation to geometric primitives."""

    def __init__(self, config: SketchConfig | None = None):
        self.config = config or SketchConfig()

    def sketch_line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
    ) -> list[tuple[float, float]]:
        """Sketch a line with wabi-sabi effect."""
        return perturb_line(x1, y1, x2, y2, self.config)

    def sketch_circle(
        self,
        cx: float,
        cy: float,
        radius: float,
    ) -> list[tuple[float, float]]:
        """Sketch a circle with wabi-sabi effect."""
        return perturb_circle(cx, cy, radius, self.config)

    def sketch_arc(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        cx: float,
        cy: float,
        radius: float,
    ) -> list[tuple[float, float]]:
        """Sketch an arc with wabi-sabi effect."""
        start_angle = math.atan2(y1 - cy, x1 - cx)
        end_angle = math.atan2(y2 - cy, x2 - cx)

        num_points = max(10, int(radius * 5))

        points = []
        for i in range(num_points + 1):
            t = i / num_points
            angle = start_angle + (end_angle - start_angle) * t

            noise_val = simplex_noise_2d(
                cx * self.config.noise_scale + math.cos(angle),
                cy * self.config.noise_scale + math.sin(angle),
                self.config.seed,
            )

            r = radius + noise_val * self.config.noise_amplitude

            points.append(
                (
                    cx + r * math.cos(angle),
                    cy + r * math.sin(angle),
                )
            )

        return points
