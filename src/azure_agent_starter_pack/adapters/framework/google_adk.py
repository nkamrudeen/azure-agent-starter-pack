"""Google ADK adapter."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import FrameworkAdapter

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "google_adk"


class GoogleAdkAdapter(FrameworkAdapter):
    @property
    def name(self) -> str:
        return "google_adk"

    @property
    def supported_project_types(self) -> tuple[str, ...]:
        return ("multi_agent_api", "multi_agent_react_ui", "agentic_rag")

    def get_template_root(self) -> Path | None:
        return _TEMPLATE_DIR if _TEMPLATE_DIR.is_dir() else None

    def get_context(self) -> dict[str, Any]:
        return {
            "framework": self.name,
            "framework_display": "Google ADK",
            "adk_agents": True,
            "adk_tools": True,
            "adk_sessions": True,
            "azure_openai_config": True,
        }
