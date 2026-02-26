"""Base interface for runtime adapters (T024)."""

from __future__ import annotations

import abc
from pathlib import Path
from typing import Any


class RuntimeAdapter(abc.ABC):
    """Each runtime adapter emits IaC and runtime config."""

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    def get_template_root(self) -> Path | None: ...

    @abc.abstractmethod
    def get_context(self) -> dict[str, Any]: ...
