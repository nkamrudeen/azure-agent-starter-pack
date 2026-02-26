"""Integration tests: Azure security, observability, and CI/CD in scaffolded output (T030–T035)."""

import json
import subprocess
import sys
from pathlib import Path


def _scaffold(tmp_path: Path) -> Path:
    target = tmp_path / "azure_project"
    target.mkdir()
    result = subprocess.run(
        [
            sys.executable, "-m", "azure_agent_starter_pack.cli.app",
            "init", str(target),
            "--framework", "microsoft_agent_framework",
            "--project-type", "multi_agent_api",
            "--pipeline", "github_actions",
            "--runtime", "aks",
            "--iac", "bicep",
            "--non-interactive",
        ],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    return target


def test_managed_identity_helper_present(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    identity = target / "src" / "identity.py"
    assert identity.is_file(), "identity.py should be generated"
    content = identity.read_text()
    assert "DefaultAzureCredential" in content
    assert "SecretClient" in content


def test_observability_helper_present(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    obs = target / "src" / "observability.py"
    assert obs.is_file(), "observability.py should be generated"
    content = obs.read_text()
    assert "TracerProvider" in content
    assert "OTLPSpanExporter" in content


def test_ci_cd_pipeline_present(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    ci = target / ".github" / "workflows" / "ci.yml"
    assert ci.is_file(), "ci.yml should be generated"
    content = ci.read_text()
    assert "sast" in content.lower() or "bandit" in content.lower()
    assert "pip-audit" in content
    assert "docker build" in content


def test_sast_and_dependency_scan_in_pipeline(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    ci = target / ".github" / "workflows" / "ci.yml"
    content = ci.read_text()
    assert "bandit" in content
    assert "pip-audit" in content


def test_unit_test_scaffold_present(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    test_file = target / "tests" / "test_example.py"
    assert test_file.is_file(), "test_example.py scaffold should be generated"


def test_pyproject_generated(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    pyproject = target / "pyproject.toml"
    assert pyproject.is_file()
    content = pyproject.read_text()
    assert "requires-python" in content


def test_infra_readme_references_iac(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    readme = target / "infra" / "README.md"
    assert readme.is_file()
    content = readme.read_text()
    assert "bicep" in content.lower()


def test_manifest_tracks_all_generated_files(tmp_path: Path) -> None:
    target = _scaffold(tmp_path)
    manifest_path = target / ".azure-agent-starter-pack" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    owned = manifest["owned_paths"]
    assert any("ci.yml" in p for p in owned)
    assert any("identity.py" in p for p in owned)
    assert any("observability.py" in p for p in owned)
