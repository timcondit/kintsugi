"""
CAD engine abstraction layer.

Allows swapping between different CAD backends (build123d, etc.)
while maintaining a consistent interface for kintsugi.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass
class Sketch:
    """A 2D sketch representation from a CAD engine."""

    lines: list[tuple[float, float, float, float]]
    arcs: list[tuple[float, float, float, float, float]]
    circles: list[tuple[float, float, float]]

    @classmethod
    def empty(cls) -> "Sketch":
        return cls(lines=[], arcs=[], circles=[])


class CADEngine(ABC):
    """Abstract base class for CAD engines."""

    @abstractmethod
    def project_3d_to_2d(
        self,
        part: Any,
        view: str = "front",
    ) -> Sketch:
        """
        Project a 3D part to 2D sketch.

        Args:
            part: 3D geometry object from the engine
            view: One of "front", "side", "top", or projection direction

        Returns:
            Sketch containing 2D geometry
        """
        ...

    @abstractmethod
    def get_edges(self, part: Any) -> list[Any]:
        """Extract edges from a 3D part."""
        ...

    @abstractmethod
    def get_faces(self, part: Any) -> list[Any]:
        """Extract faces from a 3D part."""
        ...


class Build123dEngine(CADEngine):
    """build123d CAD engine implementation."""

    def project_3d_to_2d(
        self,
        part: Any,
        view: str = "front",
    ) -> Sketch:
        from build123d import Plane, Project

        plane = {
            "front": Plane.XZ,
            "side": Plane.YZ,
            "top": Plane.XY,
        }.get(view, Plane.XZ)

        projected = Project(part).do_sort_by_distance(plane)

        lines = []
        arcs = []
        circles = []

        for edge in projected.edges:
            if hasattr(edge, "curve") and edge.curve:
                curve = edge.curve
                if hasattr(curve, "start_point") and hasattr(curve, "end_point"):
                    start = curve.start_point
                    end = curve.end_point
                    if hasattr(curve, "radius") and curve.radius:
                        center = edge.position
                        circles.append((center.X, center.Y, curve.radius))
                    else:
                        lines.append((start.X, start.Y, end.X, end.Y))

        return Sketch(lines=lines, arcs=arcs, circles=circles)

    def get_edges(self, part: Any) -> list[Any]:
        return part.edges() if hasattr(part, "edges") else []

    def get_faces(self, part: Any) -> list[Any]:
        return part.faces() if hasattr(part, "faces") else []
