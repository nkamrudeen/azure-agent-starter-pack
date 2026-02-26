"""Integration tests: verify all 4 framework overlays scaffold real agent code."""

import subprocess
import sys
from pathlib import Path

import pytest

FRAMEWORKS = [
    ("google_adk", "root_agent.py", "google.adk"),
    ("microsoft_agent_framework", "orchestrator.py", "azure.ai.projects"),
    ("langgraph", "graph.py", "langgraph"),
    ("crewai", "crew.py", "crewai"),
]


def _scaffold(tmp_path: Path, framework: str) -> Path:
    target = tmp_path / f"{framework}_project"
    target.mkdir()
    result = subprocess.run(
        [
            sys.executable, "-m", "azure_agent_starter_pack.cli.app",
            "init", str(target),
            "--framework", framework,
            "--project-type", "multi_agent_api",
            "--pipeline", "github_actions",
            "--runtime", "aks",
            "--iac", "terraform",
            "--non-interactive",
        ],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"[{framework}] stderr: {result.stderr}"
    return target


@pytest.mark.parametrize("framework,main_agent_file,import_marker", FRAMEWORKS)
def test_framework_agent_code_present(tmp_path: Path, framework: str, main_agent_file: str, import_marker: str) -> None:
    target = _scaffold(tmp_path, framework)
    agent_file = target / "app" / "agents" / main_agent_file
    assert agent_file.is_file(), f"Expected {main_agent_file} for {framework}"
    content = agent_file.read_text()
    assert import_marker in content, f"{import_marker} not found in {main_agent_file}"


@pytest.mark.parametrize("framework,main_agent_file,import_marker", FRAMEWORKS)
def test_framework_has_requirements(tmp_path: Path, framework: str, main_agent_file: str, import_marker: str) -> None:
    target = _scaffold(tmp_path, framework)
    reqs = (target / "requirements.txt").read_text()
    assert "fastapi" in reqs
    assert "uvicorn" in reqs
    assert "azure-identity" in reqs


@pytest.mark.parametrize("framework,main_agent_file,import_marker", FRAMEWORKS)
def test_framework_has_dockerfile(tmp_path: Path, framework: str, main_agent_file: str, import_marker: str) -> None:
    target = _scaffold(tmp_path, framework)
    assert (target / "Dockerfile").is_file()
    content = (target / "Dockerfile").read_text()
    assert "requirements.txt" in content


@pytest.mark.parametrize("framework,main_agent_file,import_marker", FRAMEWORKS)
def test_framework_has_env_example(tmp_path: Path, framework: str, main_agent_file: str, import_marker: str) -> None:
    target = _scaffold(tmp_path, framework)
    assert (target / ".env.example").is_file()


@pytest.mark.parametrize("framework,main_agent_file,import_marker", FRAMEWORKS)
def test_framework_has_agent_tests(tmp_path: Path, framework: str, main_agent_file: str, import_marker: str) -> None:
    target = _scaffold(tmp_path, framework)
    assert (target / "tests" / "test_agents.py").is_file()


def test_aks_kubernetes_manifests(tmp_path: Path) -> None:
    target = _scaffold(tmp_path, "google_adk")
    k8s = target / "k8s"
    assert k8s.is_dir(), "k8s/ directory should exist for AKS runtime"
    expected = ["namespace.yaml", "deployment.yaml", "service.yaml", "ingress.yaml",
                "hpa.yaml", "configmap.yaml", "service-account.yaml", "kustomization.yaml"]
    for f in expected:
        assert (k8s / f).is_file(), f"k8s/{f} missing"


def test_aks_deployment_has_health_probes(tmp_path: Path) -> None:
    target = _scaffold(tmp_path, "microsoft_agent_framework")
    deployment = (target / "k8s" / "deployment.yaml").read_text()
    assert "livenessProbe" in deployment
    assert "readinessProbe" in deployment
    assert "/health" in deployment


def test_aks_hpa_configured(tmp_path: Path) -> None:
    target = _scaffold(tmp_path, "langgraph")
    hpa = (target / "k8s" / "hpa.yaml").read_text()
    assert "HorizontalPodAutoscaler" in hpa
    assert "minReplicas" in hpa
