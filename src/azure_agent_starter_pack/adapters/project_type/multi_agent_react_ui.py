"""Multi-Agent React Chat UI project type generator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import ProjectTypeGenerator


class MultiAgentReactUiGenerator(ProjectTypeGenerator):
    @property
    def name(self) -> str:
        return "multi_agent_react_ui"

    def get_template_root(self) -> Path | None:
        return None

    def get_context(self) -> dict[str, Any]:
        return {
            "project_type": self.name,
            "project_type_display": "Multi-Agent React Chat UI",
            "fastapi": True,
            "react_frontend": True,
            "jwt_auth": True,
            "websocket": True,
            "opentelemetry": True,
        }
