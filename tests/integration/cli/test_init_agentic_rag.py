"""Integration tests: agentic_rag project type generates RAG-specific code."""

import subprocess
import sys
from pathlib import Path

import pytest

FRAMEWORKS = ["google_adk", "microsoft_agent_framework", "langgraph", "crewai"]


def _scaffold_rag(tmp_path: Path, framework: str) -> Path:
    target = tmp_path / f"rag_{framework}"
    target.mkdir()
    result = subprocess.run(
        [
            sys.executable, "-m", "azure_agent_starter_pack.cli.app",
            "init", str(target),
            "--framework", framework,
            "--project-type", "agentic_rag",
            "--pipeline", "github_actions",
            "--runtime", "aks",
            "--iac", "terraform",
            "--non-interactive",
        ],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"[{framework}] stderr: {result.stderr}"
    return target


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_rag_pipeline_present(tmp_path: Path, framework: str) -> None:
    target = _scaffold_rag(tmp_path, framework)
    rag_dir = target / "app" / "rag"
    assert rag_dir.is_dir(), "app/rag/ directory should exist"
    for f in ["config.py", "chunker.py", "embedder.py", "indexer.py", "retriever.py"]:
        assert (rag_dir / f).is_file(), f"app/rag/{f} missing"


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_rag_requirements_present(tmp_path: Path, framework: str) -> None:
    target = _scaffold_rag(tmp_path, framework)
    rag_reqs = target / "requirements-rag.txt"
    assert rag_reqs.is_file()
    content = rag_reqs.read_text()
    assert "azure-search-documents" in content
    assert "langchain" in content


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_sample_document_present(tmp_path: Path, framework: str) -> None:
    target = _scaffold_rag(tmp_path, framework)
    assert (target / "data" / "sample.txt").is_file()


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_indexing_script_present(tmp_path: Path, framework: str) -> None:
    target = _scaffold_rag(tmp_path, framework)
    script = target / "scripts" / "index_documents.py"
    assert script.is_file()
    content = script.read_text()
    assert "ensure_index" in content


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_retrieval_tool_present(tmp_path: Path, framework: str) -> None:
    target = _scaffold_rag(tmp_path, framework)
    tool = target / "app" / "tools" / "retrieval_tool.py"
    assert tool.is_file()
    content = tool.read_text()
    assert "retrieve" in content


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_rag_main_has_search_endpoint(tmp_path: Path, framework: str) -> None:
    target = _scaffold_rag(tmp_path, framework)
    main = (target / "app" / "main.py").read_text()
    assert "/search" in main
    assert "Agentic RAG" in main


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_rag_env_has_search_config(tmp_path: Path, framework: str) -> None:
    target = _scaffold_rag(tmp_path, framework)
    env = (target / ".env.example").read_text()
    assert "AZURE_AI_SEARCH_ENDPOINT" in env
    assert "AZURE_OPENAI_EMBEDDING_DEPLOYMENT" in env


def test_rag_differs_from_api(tmp_path: Path) -> None:
    """Verify agentic_rag generates different files from multi_agent_api."""
    rag_target = tmp_path / "rag"
    rag_target.mkdir()
    api_target = tmp_path / "api"
    api_target.mkdir()

    for pt, target in [("agentic_rag", rag_target), ("multi_agent_api", api_target)]:
        subprocess.run(
            [
                sys.executable, "-m", "azure_agent_starter_pack.cli.app",
                "init", str(target),
                "--framework", "google_adk",
                "--project-type", pt,
                "--pipeline", "github_actions",
                "--runtime", "aks",
                "--iac", "terraform",
                "--non-interactive",
            ],
            capture_output=True, text=True, timeout=120,
        )

    rag_files = {str(p.relative_to(rag_target)) for p in rag_target.rglob("*") if p.is_file()}
    api_files = {str(p.relative_to(api_target)) for p in api_target.rglob("*") if p.is_file()}

    rag_only = rag_files - api_files
    assert len(rag_only) > 5, f"RAG should have many files not in API, got: {rag_only}"
    assert any("rag" in f for f in rag_only), "RAG-specific files should contain 'rag'"
