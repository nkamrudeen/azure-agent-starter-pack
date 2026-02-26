"""Adapter registry: resolve adapters from config values."""

from __future__ import annotations

from azure_agent_starter_pack.adapters.framework.base import FrameworkAdapter
from azure_agent_starter_pack.adapters.framework.crewai import CrewAiAdapter
from azure_agent_starter_pack.adapters.framework.google_adk import GoogleAdkAdapter
from azure_agent_starter_pack.adapters.framework.langgraph import LangGraphAdapter
from azure_agent_starter_pack.adapters.framework.microsoft import MicrosoftAgentFrameworkAdapter
from azure_agent_starter_pack.adapters.pipeline.azure_devops import AzureDevOpsGenerator
from azure_agent_starter_pack.adapters.pipeline.base import PipelineGenerator
from azure_agent_starter_pack.adapters.pipeline.github_actions import GitHubActionsGenerator
from azure_agent_starter_pack.adapters.project_type.agentic_rag import AgenticRagGenerator
from azure_agent_starter_pack.adapters.project_type.base import ProjectTypeGenerator
from azure_agent_starter_pack.adapters.project_type.multi_agent_api import MultiAgentApiGenerator
from azure_agent_starter_pack.adapters.project_type.multi_agent_react_ui import (
    MultiAgentReactUiGenerator,
)
from azure_agent_starter_pack.adapters.runtime.aks import AksAdapter
from azure_agent_starter_pack.adapters.runtime.app_service import AppServiceAdapter
from azure_agent_starter_pack.adapters.runtime.base import RuntimeAdapter
from azure_agent_starter_pack.adapters.runtime.container_apps import ContainerAppsAdapter

_FRAMEWORK_MAP: dict[str, type[FrameworkAdapter]] = {
    "microsoft_agent_framework": MicrosoftAgentFrameworkAdapter,
    "langgraph": LangGraphAdapter,
    "google_adk": GoogleAdkAdapter,
    "crewai": CrewAiAdapter,
}

_PROJECT_TYPE_MAP: dict[str, type[ProjectTypeGenerator]] = {
    "multi_agent_api": MultiAgentApiGenerator,
    "multi_agent_react_ui": MultiAgentReactUiGenerator,
    "agentic_rag": AgenticRagGenerator,
}

_RUNTIME_MAP: dict[str, type[RuntimeAdapter]] = {
    "aks": AksAdapter,
    "container_apps": ContainerAppsAdapter,
    "app_service": AppServiceAdapter,
}

_PIPELINE_MAP: dict[str, type[PipelineGenerator]] = {
    "github_actions": GitHubActionsGenerator,
    "azure_devops": AzureDevOpsGenerator,
}


def get_framework_adapter(name: str) -> FrameworkAdapter:
    cls = _FRAMEWORK_MAP.get(name)
    if cls is None:
        raise KeyError(f"Unknown framework adapter: {name!r}")
    return cls()


def get_project_type_generator(name: str) -> ProjectTypeGenerator:
    cls = _PROJECT_TYPE_MAP.get(name)
    if cls is None:
        raise KeyError(f"Unknown project type generator: {name!r}")
    return cls()


def get_runtime_adapter(name: str) -> RuntimeAdapter:
    cls = _RUNTIME_MAP.get(name)
    if cls is None:
        raise KeyError(f"Unknown runtime adapter: {name!r}")
    return cls()


def get_pipeline_generator(name: str) -> PipelineGenerator:
    cls = _PIPELINE_MAP.get(name)
    if cls is None:
        raise KeyError(f"Unknown pipeline generator: {name!r}")
    return cls()
