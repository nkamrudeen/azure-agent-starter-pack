"""Agentic RAG project type generator."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import ProjectTypeGenerator

_TEMPLATE_DIR = Path(__file__).resolve().parent.parent.parent / "templates"


class AgenticRagGenerator(ProjectTypeGenerator):
    @property
    def name(self) -> str:
        return "agentic_rag"

    def get_template_root(self) -> Path | None:
        return None

    def get_context(self) -> dict[str, Any]:
        return {
            "project_type": self.name,
            "project_type_display": "Agentic RAG with Azure AI Search",
            "fastapi": True,
            "azure_ai_search": True,
            "vector_store": True,
            "opentelemetry": True,
        }
