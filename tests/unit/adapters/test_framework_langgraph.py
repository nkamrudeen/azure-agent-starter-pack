"""Unit tests for LangGraph adapter (T029)."""

from azure_agent_starter_pack.adapters.framework.langgraph import LangGraphAdapter


def test_name() -> None:
    adapter = LangGraphAdapter()
    assert adapter.name == "langgraph"


def test_supported_project_types() -> None:
    adapter = LangGraphAdapter()
    assert "multi_agent_api" in adapter.supported_project_types
    assert "agentic_rag" in adapter.supported_project_types


def test_context_contains_langgraph_keys() -> None:
    adapter = LangGraphAdapter()
    ctx = adapter.get_context()
    assert ctx["graph_nodes"] is True
    assert ctx["state_management"] is True
    assert ctx["azure_openai_config"] is True
    assert ctx["streaming_support"] is True
    assert ctx["framework"] == "langgraph"
