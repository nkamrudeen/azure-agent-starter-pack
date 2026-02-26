"""Unit tests for Microsoft Agent Framework adapter (T029)."""

from azure_agent_starter_pack.adapters.framework.microsoft import (
    MicrosoftAgentFrameworkAdapter,
)


def test_name() -> None:
    adapter = MicrosoftAgentFrameworkAdapter()
    assert adapter.name == "microsoft_agent_framework"


def test_supported_project_types() -> None:
    adapter = MicrosoftAgentFrameworkAdapter()
    assert "multi_agent_api" in adapter.supported_project_types
    assert "agentic_rag" in adapter.supported_project_types


def test_context_contains_azure_keys() -> None:
    adapter = MicrosoftAgentFrameworkAdapter()
    ctx = adapter.get_context()
    assert ctx["azure_ai_foundry"] is True
    assert ctx["managed_identity"] is True
    assert ctx["azure_sdk_integration"] is True
    assert ctx["azure_monitor_hooks"] is True
    assert ctx["framework"] == "microsoft_agent_framework"
