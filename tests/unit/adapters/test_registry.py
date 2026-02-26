"""Unit tests for adapter registry."""

import pytest

from azure_agent_starter_pack.adapters.registry import (
    get_framework_adapter,
    get_pipeline_generator,
    get_project_type_generator,
    get_runtime_adapter,
)


@pytest.mark.parametrize("name", ["microsoft_agent_framework", "langgraph", "google_adk", "crewai"])
def test_framework_adapter_registered(name: str) -> None:
    adapter = get_framework_adapter(name)
    assert adapter.name == name


@pytest.mark.parametrize("name", ["multi_agent_api", "multi_agent_react_ui", "agentic_rag"])
def test_project_type_generator_registered(name: str) -> None:
    gen = get_project_type_generator(name)
    assert gen.name == name


@pytest.mark.parametrize("name", ["aks", "container_apps", "app_service"])
def test_runtime_adapter_registered(name: str) -> None:
    adapter = get_runtime_adapter(name)
    assert adapter.name == name


@pytest.mark.parametrize("name", ["github_actions", "azure_devops"])
def test_pipeline_generator_registered(name: str) -> None:
    gen = get_pipeline_generator(name)
    assert gen.name == name


def test_unknown_framework_raises() -> None:
    with pytest.raises(KeyError):
        get_framework_adapter("unknown")


def test_unknown_project_type_raises() -> None:
    with pytest.raises(KeyError):
        get_project_type_generator("unknown")
