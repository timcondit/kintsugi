"""
SVG export for kintsugi drawings.

Renders Drawing objects to SVG strings with wabi-sabi styling.
"""

import math

from ..drawing import (
    PALETTE,
    STROKE_HEAVY,
    STROKE_LIGHT,
    STROKE_MEDIUM,
    Callout,
    CenterLine,
    Dimension,
    Drawing,
    HatchRegion,
)


def _points_to_svg(points: list[tuple[float, float]]) -> str:
    """Convert a list of points to an SVG path d attribute."""
    if not points:
        return ""
    d = f"M {points[0][0]:.2f},{points[0][1]:.2f}"
    for x, y in points[1:]:
        d += f" L {x:.2f},{y:.2f}"
    return d


def _arrow_head(x: float, y: float, angle_deg: float, size: float = 6.0) -> str:
    """Render a filled arrow head."""
    rad = math.radians(angle_deg)
    tip_x, tip_y = x, y
    b1_x = tip_x - size * math.cos(rad) + (size * 0.4) * math.sin(rad)
    b1_y = tip_y - size * math.sin(rad) - (size * 0.4) * math.cos(rad)
    b2_x = tip_x - size * math.cos(rad) - (size * 0.4) * math.sin(rad)
    b2_y = tip_y - size * math.sin(rad) + (size * 0.4) * math.cos(rad)
    return (
        f'<polygon points="{tip_x:.2f},{tip_y:.2f} '
        f"{b1_x:.2f},{b1_y:.2f} "
        f'{b2_x:.2f},{b2_y:.2f}" '
        f'fill="{PALETTE["amber"]}" />'
    )


def _render_dimension(d: Dimension) -> str:
    """Render a dimension line."""
    dx = d.x2 - d.x1
    dy = d.y2 - d.y1
    length_px = math.hypot(dx, dy)
    if length_px < 1:
        return ""

    perp_x = -dy / length_px
    perp_y = dx / length_px

    if d.side in ("below", "right"):
        perp_x, perp_y = -perp_x, -perp_y

    ox = perp_x * d.offset
    oy = perp_y * d.offset

    lx1, ly1 = d.x1 + ox, d.y1 + oy
    lx2, ly2 = d.x2 + ox, d.y2 + oy

    ext_gap = 2.0
    ext_x1 = d.x1 + perp_x * ext_gap
    ext_y1 = d.y1 + perp_y * ext_gap
    ext_x2 = d.x2 + perp_x * ext_gap
    ext_y2 = d.y2 + perp_y * ext_gap

    line_angle = math.degrees(math.atan2(dy, dx))
    arrow1_angle = line_angle + 180
    arrow2_angle = line_angle

    mid_x = (lx1 + lx2) / 2
    mid_y = (ly1 + ly2) / 2
    label_x = mid_x + perp_x * 8
    label_y = mid_y + perp_y * 8

    label = d.label or ""

    parts = [
        f'<line x1="{ext_x1:.2f}" y1="{ext_y1:.2f}" x2="{lx1:.2f}" y2="{ly1:.2f}" '
        f'stroke="{PALETTE["amber"]}" stroke-width="{STROKE_LIGHT}" />',
        f'<line x1="{ext_x2:.2f}" y1="{ext_y2:.2f}" x2="{lx2:.2f}" y2="{ly2:.2f}" '
        f'stroke="{PALETTE["amber"]}" stroke-width="{STROKE_LIGHT}" />',
        f'<line x1="{lx1:.2f}" y1="{ly1:.2f}" x2="{lx2:.2f}" y2="{ly2:.2f}" '
        f'stroke="{PALETTE["amber"]}" stroke-width="{STROKE_MEDIUM}" />',
        _arrow_head(lx1, ly1, arrow1_angle),
        _arrow_head(lx2, ly2, arrow2_angle),
    ]

    if label:
        parts.append(
            f'<rect x="{label_x - 18:.2f}" y="{label_y - 7:.2f}" '
            f'width="36" height="14" rx="2" '
            f'fill="{PALETTE["cream"]}" opacity="0.85" />'
        )
        parts.append(
            f'<text x="{label_x:.2f}" y="{label_y + 4:.2f}" '
            f'text-anchor="middle" font-family="serif" font-size="10" '
            f'fill="{PALETTE["amber"]}">{label}</text>'
        )

    return "\n".join(parts)


def _render_callout(c: Callout) -> str:
    """Render a callout bubble."""
    circled = "①②③④⑤⑥⑦⑧⑨"
    char = circled[c.number - 1] if 1 <= c.number <= 9 else str(c.number)
    return (
        f'<circle cx="{c.x:.2f}" cy="{c.y:.2f}" r="{c.radius:.2f}" '
        f'fill="{PALETTE["cream"]}" stroke="{PALETTE["amber"]}" '
        f'stroke-width="{STROKE_MEDIUM}" />'
        f'<text x="{c.x:.2f}" y="{c.y + 4.5:.2f}" '
        f'text-anchor="middle" font-family="serif" font-size="{c.radius * 1.2:.1f}" '
        f'fill="{PALETTE["amber"]}">{char}</text>'
    )


def _render_hatch(h: HatchRegion) -> str:
    """Render diagonal hatching."""
    import itertools

    clip_id = f"hatch-clip-{next(itertools.count(1))}"
    angle_rad = math.radians(h.angle_deg)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    lines = []
    diagonal = math.hypot(h.width, h.height)
    t = -diagonal
    while t <= diagonal * 2:
        cx = h.x + h.width / 2 + t * cos_a
        cy = h.y + h.height / 2 + t * sin_a
        perp_len = diagonal
        lx1 = cx + perp_len * (-sin_a)
        ly1 = cy + perp_len * cos_a
        lx2 = cx - perp_len * (-sin_a)
        ly2 = cy - perp_len * cos_a
        lines.append(
            f'<line x1="{lx1:.2f}" y1="{ly1:.2f}" '
            f'x2="{lx2:.2f}" y2="{ly2:.2f}" '
            f'stroke="{PALETTE["hatch"]}" stroke-width="{STROKE_LIGHT}" />'
        )
        t += h.spacing

    return (
        f'<defs><clipPath id="{clip_id}">'
        f'<rect x="{h.x:.2f}" y="{h.y:.2f}" '
        f'width="{h.width:.2f}" height="{h.height:.2f}" /></clipPath></defs>'
        f'<g clip-path="url(#{clip_id})" opacity="0.5">' + "\n".join(lines) + "</g>"
    )


def _render_centerline(c: CenterLine) -> str:
    """Render a center line."""
    return (
        f'<line x1="{c.x1:.2f}" y1="{c.y1:.2f}" '
        f'x2="{c.x2:.2f}" y2="{c.y2:.2f}" '
        f'stroke="{PALETTE["amber"]}" '
        f'stroke-width="{STROKE_LIGHT}" '
        f'stroke-dasharray="8,3,2,3" '
        f'opacity="0.7" />'
    )


def render_to_svg(drawing: Drawing) -> str:
    """Render a Drawing to an SVG string."""
    svg_parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {drawing.width} {drawing.height}" '
        f'width="{drawing.width}" height="{drawing.height}">',
        f'<rect width="100%" height="100%" fill="{drawing.background}" />',
    ]

    for path in drawing.sketch_paths:
        d = _points_to_svg(path)
        if d:
            svg_parts.append(
                f'<path d="{d}" fill="none" stroke="{PALETTE["ink"]}" '
                f'stroke-width="{STROKE_HEAVY}" stroke-linecap="round" />'
            )

    for path in drawing.text_paths:
        d = _points_to_svg(path)
        if d:
            svg_parts.append(
                f'<path d="{d}" fill="none" stroke="{PALETTE["brown"]}" '
                f'stroke-width="{STROKE_MEDIUM}" stroke-linecap="round" stroke-linejoin="round" />'
            )

    for h in drawing.hatches:
        svg_parts.append(_render_hatch(h))

    for c in drawing.centerlines:
        svg_parts.append(_render_centerline(c))

    for dim in drawing.dimensions:
        svg_parts.append(_render_dimension(dim))

    for callout in drawing.callouts:
        svg_parts.append(_render_callout(callout))

    for text, x, y, style in drawing.labels:
        fill = PALETTE["amber"] if style == "dimension" else PALETTE["brown"]
        svg_parts.append(
            f'<text x="{x:.2f}" y="{y:.2f}" '
            f'font-family="serif" font-size="10" fill="{fill}">{text}</text>'
        )

    svg_parts.append("</svg>")

    return "\n".join(svg_parts)
