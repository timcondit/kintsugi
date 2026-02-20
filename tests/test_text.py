"""Tests for kintsugi text module."""

from kintsugi.text import HandTextRenderer, TextConfig, HersheyFont


def test_text_renderer_default_config():
    """Test HandTextRenderer initializes with defaults."""
    renderer = HandTextRenderer()
    assert renderer.config.font == HersheyFont.ROMAN
    assert renderer.config.size == 12.0
    assert renderer.config.wobble == 0.3


def test_text_renderer_custom_config():
    """Test HandTextRenderer accepts custom config."""
    config = TextConfig(size=24, wobble=0.5)
    renderer = HandTextRenderer(config)
    assert renderer.config.size == 24
    assert renderer.config.wobble == 0.5


def test_render_character():
    """Test rendering a single character."""
    renderer = HandTextRenderer()
    strokes = renderer.render_character("A", 0, 0)
    assert len(strokes) > 0  # A has multiple strokes


def test_render_text():
    """Test rendering a string."""
    renderer = HandTextRenderer()
    strokes = renderer.render_text("HI", 0, 0)
    assert len(strokes) > 0


def test_render_unknown_character():
    """Test rendering unknown character returns empty."""
    renderer = HandTextRenderer()
    strokes = renderer.render_character("@", 0, 0)
    assert strokes == []
