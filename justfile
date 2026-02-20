# Kintsugi justfile

set shell := ["bash", "-c"]

default: test

# Install dependencies and set up editable package
dev:
    uv pip install -e ".[dev]"
    @echo "Setting up git hooks..."
    uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
    @echo "✓ Pre-commit hooks installed"

# Run all tests
test:
    uv run --python 3.12 pytest

# Run only fast unit tests (pre-commit subset)
test-fast:
    uv run --python 3.12 pytest -m "not slow"

# Run tests with coverage report
coverage:
    uv run --python 3.12 pytest
    @echo "\nHTML coverage report: htmlcov/index.html"

# Run mypy type checking
typecheck:
    uv run --python 3.12 mypy src/kintsugi

# Run all linters (ruff, taplo, dprint, mypy)
lint:
    ruff check .
    @RUST_LOG=warn taplo check
    dprint check
    uv run --python 3.12 mypy src/kintsugi

# Check commit messages for conventional commit compliance
check-commits:
    cog check HEAD~10..HEAD

# Bump version and generate changelog (infers bump level from commits since last tag)
release:
    cog bump --auto

# Format Python, TOML, and Markdown files
format:
    ruff format .
    @RUST_LOG=warn taplo format
    dprint fmt

# Clear Python cache files
clean:
    find . -type d -name "__pycache__" -exec rm -rf {} +
    rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov
