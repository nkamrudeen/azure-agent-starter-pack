"""Microsoft Agent Framework adapter (T020)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import FrameworkAdapter

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates" / "microsoft_agent_framework"


class MicrosoftAgentFrameworkAdapter(FrameworkAdapter):
    @property
    def name(self) -> str:
        return "microsoft_agent_framework"

    @property
    def supported_project_types(self) -> tuple[str, ...]:
        return ("multi_agent_api", "multi_agent_react_ui", "agentic_rag")

    def get_template_root(self) -> Path | None:
        return _TEMPLATE_DIR if _TEMPLATE_DIR.is_dir() else None

    def get_context(self) -> dict[str, Any]:
        return {
            "framework": self.name,
            "framework_display": "Microsoft Agent Framework",
            "azure_ai_foundry": True,
            "managed_identity": True,
            "azure_sdk_integration": True,
            "azure_monitor_hooks": True,
            "agent_composition": True,
            "memory_tool_orchestration": True,
        }
