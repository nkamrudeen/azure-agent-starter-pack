"""GitHub Actions pipeline generator (T027)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .base import PipelineGenerator

_TEMPLATE_DIR = (
    Path(__file__).resolve().parent.parent.parent / "templates" / "pipelines" / "github_actions"
)


class GitHubActionsGenerator(PipelineGenerator):
    @property
    def name(self) -> str:
        return "github_actions"

    def get_template_root(self) -> Path | None:
        return _TEMPLATE_DIR if _TEMPLATE_DIR.is_dir() else None

    def get_context(self) -> dict[str, Any]:
        return {
            "pipeline": self.name,
            "pipeline_display": "GitHub Actions",
            "sast": True,
            "dependency_scan": True,
            "docker_build": True,
            "acr_push": True,
            "deploy_to_runtime": True,
        }
