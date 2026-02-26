"""Azure Container Apps runtime adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import RuntimeAdapter

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "runtimes" / "container_apps"


class ContainerAppsAdapter(RuntimeAdapter):
    @property
    def name(self) -> str:
        return "container_apps"

    def get_template_root(self) -> Path | None:
        return _TEMPLATE_DIR if _TEMPLATE_DIR.is_dir() else None

    def get_context(self) -> dict[str, Any]:
        return {
            "runtime": self.name,
            "runtime_display": "Azure Container Apps",
            "dapr": True,
            "managed_identity_binding": True,
            "revision_management": True,
            "azure_monitor_integration": True,
        }
