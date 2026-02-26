"""Template cache: read/write cached templates with version keying (FR-023)."""

import shutil
from pathlib import Path


def get_cache_dir() -> Path:
    """Return cache directory (e.g. user dir)."""
    return Path.home() / ".cache" / "azure-agent-starter-pack" / "templates"


def get_cached_path(version: str) -> Path:
    """Return path for a cached template version."""
    return get_cache_dir() / version.replace("/", "_")


def read_cached(version: str) -> Path | None:
    """Return path to cached template root if it exists, else None."""
    p = get_cached_path(version)
    return p if p.is_dir() else None


def write_cached(version: str, source_root: Path) -> Path:
    """Copy source_root to cache for version; return cached path."""
    dest = get_cached_path(version)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(source_root, dest)
    return dest
