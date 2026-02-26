"""Unit tests for compatibility matrix (FR-022)."""

import pytest

from azure_agent_starter_pack.config.compatibility import (
    InvalidCombinationError,
    is_valid_combination,
    validate_combination,
)


def test_valid_combination_microsoft_multi_agent_api() -> None:
    validate_combination(
        "microsoft_agent_framework",
        "multi_agent_api",
        "github_actions",
        "aks",
        "bicep",
    )
    assert is_valid_combination(
        "microsoft_agent_framework",
        "multi_agent_api",
        "github_actions",
        "aks",
        "bicep",
    ) is True


def test_valid_combination_langgraph_agentic_rag() -> None:
    validate_combination("langgraph", "agentic_rag", "github_actions", "aks", "bicep")
    assert is_valid_combination("langgraph", "agentic_rag", "github_actions", "aks", "bicep") is True


def test_valid_combination_crewai_container_apps_terraform() -> None:
    validate_combination("crewai", "multi_agent_api", "github_actions", "container_apps", "terraform")
    assert is_valid_combination("crewai", "multi_agent_api", "github_actions", "container_apps", "terraform") is True


def test_invalid_combination_raises() -> None:
    with pytest.raises(InvalidCombinationError) as exc_info:
        validate_combination(
            "nonexistent_framework",
            "multi_agent_api",
            "github_actions",
            "aks",
            "bicep",
        )
    assert "Unsupported combination" in str(exc_info.value)
    assert exc_info.value.framework == "nonexistent_framework"


def test_invalid_combination_is_false() -> None:
    assert is_valid_combination("nonexistent", "multi_agent_api", "github_actions", "aks", "bicep") is False
