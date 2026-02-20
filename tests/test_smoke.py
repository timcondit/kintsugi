"""Smoke test to verify tooling is working correctly."""


def test_smoke():
    """Basic test to verify pytest works."""


def test_ruff_works():
    """Verify ruff can lint this file."""
    import subprocess

    result = subprocess.run(
        ["ruff", "check", "tests/test_smoke.py"], capture_output=True, text=True
    )
    assert result.returncode == 0, f"Ruff found issues: {result.stdout}"


def test_ruff_format_works():
    """Verify ruff format can format this file."""
    import subprocess

    result = subprocess.run(
        ["ruff", "format", "--check", "tests/test_smoke.py"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"Ruff format found issues: {result.stdout}"


def test_mypy_works():
    """Verify mypy can type-check this file."""
    import subprocess

    result = subprocess.run(
        ["mypy", "tests/test_smoke.py"], capture_output=True, text=True
    )
    # mypy returns 0 if no errors, or 1 if errors found
    # We're just checking it runs without crashing
    assert result.returncode in (0, 1), f"Mypy crashed: {result.stderr}"
