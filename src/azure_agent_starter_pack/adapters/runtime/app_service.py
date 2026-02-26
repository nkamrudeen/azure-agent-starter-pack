"""Azure App Service runtime adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import RuntimeAdapter

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "runtimes" / "app_service"


class AppServiceAdapter(RuntimeAdapter):
    @property
    def name(self) -> str:
        return "app_service"

    def get_template_root(self) -> Path | None:
        return _TEMPLATE_DIR if _TEMPLATE_DIR.is_dir() else None

    def get_context(self) -> dict[str, Any]:
        return {
            "runtime": self.name,
            "runtime_display": "Azure App Service",
            "managed_identity_binding": True,
            "app_settings": True,
            "deployment_slots": True,
            "azure_monitor_integration": True,
        }
