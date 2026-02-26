"""Unit tests for config schema."""

from pathlib import Path

from azure_agent_starter_pack.config.schema import (
    FRAMEWORKS,
    IAC_OPTIONS,
    PIPELINES,
    PROJECT_TYPES,
    RUNTIMES,
    ProjectConfig,
)


def test_project_config_requires_framework_project_type_pipeline_runtime_iac() -> None:
    cfg = ProjectConfig(
        framework="microsoft_agent_framework",
        project_type="multi_agent_api",
        pipeline="github_actions",
        runtime="aks",
        iac="bicep",
    )
    assert cfg.framework == "microsoft_agent_framework"
    assert cfg.target_dir == Path(".")


def test_project_config_accepts_target_dir_overwrite_non_interactive() -> None:
    cfg = ProjectConfig(
        framework="langgraph",
        project_type="agentic_rag",
        pipeline="github_actions",
        runtime="aks",
        iac="bicep",
        target_dir=Path("/tmp/out"),
        overwrite=True,
        non_interactive=True,
    )
    assert cfg.target_dir == Path("/tmp/out")
    assert cfg.overwrite is True
    assert cfg.non_interactive is True


def test_enums_defined() -> None:
    assert "microsoft_agent_framework" in FRAMEWORKS
    assert "multi_agent_api" in PROJECT_TYPES
    assert "github_actions" in PIPELINES
    assert "aks" in RUNTIMES
    assert "bicep" in IAC_OPTIONS
