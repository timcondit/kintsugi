"""Tests for kintsugi sketch module."""

from kintsugi.sketch import WabiSketch, SketchConfig


def test_wabisketch_default_config():
    """Test WabiSketch initializes with defaults."""
    wabi = WabiSketch()
    assert wabi.config.noise_scale == 0.02
    assert wabi.config.noise_amplitude == 1.5
    assert wabi.config.seed is None


def test_wabisketch_custom_config():
    """Test WabiSketch accepts custom config."""
    config = SketchConfig(noise_scale=0.05, noise_amplitude=2.0, seed=42)
    wabi = WabiSketch(config)
    assert wabi.config.noise_scale == 0.05
    assert wabi.config.noise_amplitude == 2.0
    assert wabi.config.seed == 42


def test_sketch_line_returns_points():
    """Test that sketch_line returns a list of points."""
    wabi = WabiSketch()
    points = wabi.sketch_line(0, 0, 100, 0)
    assert len(points) > 2
    # First point should be near origin
    assert abs(points[0][0]) < 1
    assert abs(points[0][1]) < 1
    # Last point should be near endpoint
    assert abs(points[-1][0] - 100) < 1
    assert abs(points[-1][1]) < 1


def test_sketch_circle_returns_points():
    """Test that sketch_circle returns a list of points."""
    wabi = WabiSketch()
    points = wabi.sketch_circle(50, 50, 25)
    assert len(points) > 10
    # First and last points should be close (closed circle)
    assert abs(points[0][0] - points[-1][0]) < 5
    assert abs(points[0][1] - points[-1][1]) < 5


def test_sketch_line_short():
    """Test short line handling."""
    wabi = WabiSketch()
    points = wabi.sketch_line(0, 0, 0.001, 0)
    # Short lines get minimal points (but wabi-sabi adds some)
    assert len(points) >= 2
