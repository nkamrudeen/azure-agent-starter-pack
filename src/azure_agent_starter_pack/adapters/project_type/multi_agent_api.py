"""Multi-Agent API project type generator (T023)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import ProjectTypeGenerator


class MultiAgentApiGenerator(ProjectTypeGenerator):
    @property
    def name(self) -> str:
        return "multi_agent_api"

    def get_template_root(self) -> Path | None:
        return None

    def get_context(self) -> dict[str, Any]:
        return {
            "project_type": self.name,
            "project_type_display": "Multi-Agent API",
            "fastapi": True,
            "health_endpoint": True,
            "swagger": True,
            "opentelemetry": True,
            "unit_test_scaffold": True,
        }
