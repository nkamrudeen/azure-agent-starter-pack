"""Base interface for project type generators (T022)."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any


class ProjectTypeGenerator(abc.ABC):
    """Each project type contributes layout, entrypoints, and context."""

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    def get_template_root(self) -> Path | None:
        """Return optional project-type-specific template directory overlay."""
        ...

    @abc.abstractmethod
    def get_context(self) -> dict[str, Any]:
        """Return Jinja2 context keys contributed by this project type."""
        ...
