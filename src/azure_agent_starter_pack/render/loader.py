"""Template loader: bundled path or cache; cache fallback when fetch fails (FR-023)."""

from pathlib import Path

from . import cache

# Bundled templates live inside the package
_BUNDLED_ROOT = Path(__file__).resolve().parent.parent / "templates"


def load_templates(version: str | None = None) -> Path:
    """Return the templates root directory.

    The templates root contains:
      _common/           — shared files (config, identity, pyproject, etc.)
      <framework>/<pt>/  — self-contained per framework × project type
      pipelines/         — pipeline overlays
      runtimes/          — runtime overlays
      iac/               — IaC overlays
    """
    ver = version or "default"
    cached = cache.read_cached(ver)
    if cached is not None:
        return cached
    if _BUNDLED_ROOT.is_dir():
        return _BUNDLED_ROOT
    raise FileNotFoundError(
        f"No templates found for version {ver!r} (no cache and no bundled templates). "
        "Run init once with network to populate cache, or ensure bundled templates exist."
    )
