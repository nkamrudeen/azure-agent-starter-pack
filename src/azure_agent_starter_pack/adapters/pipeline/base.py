"""Base interface for pipeline generators (T026)."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any


class PipelineGenerator(abc.ABC):
    """Each pipeline generator emits CI/CD YAML."""

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    def get_template_root(self) -> Path | None: ...

    @abc.abstractmethod
    def get_context(self) -> dict[str, Any]: ...
