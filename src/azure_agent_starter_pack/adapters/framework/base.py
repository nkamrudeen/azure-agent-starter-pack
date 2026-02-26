"""Base interface for framework adapters (T019)."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any


class FrameworkAdapter(abc.ABC):
    """Each framework adapter provides template context and supported project types."""

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @property
    @abc.abstractmethod
    def supported_project_types(self) -> tuple[str, ...]: ...

    @abc.abstractmethod
    def get_template_root(self) -> Path | None:
        """Return optional framework-specific template directory overlay."""
        ...

    @abc.abstractmethod
    def get_context(self) -> dict[str, Any]:
        """Return Jinja2 context keys contributed by this framework."""
        ...
