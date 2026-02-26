"""Integration test for the init command (T018)."""

import json
import subprocess
import sys
from pathlib import Path


def _run_init(target: Path, extra_args: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [
        sys.executable,
        "-m",
        "azure_agent_starter_pack.cli.app",
        "init",
        str(target),
        "--framework", "microsoft_agent_framework",
        "--project-type", "multi_agent_api",
        "--pipeline", "github_actions",
        "--runtime", "aks",
        "--iac", "bicep",
        "--non-interactive",
    ]
    if extra_args:
        cmd.extend(extra_args)
    return subprocess.run(cmd, capture_output=True, text=True, timeout=120)


def test_init_creates_project_in_empty_dir(tmp_path: Path) -> None:
    target = tmp_path / "my_project"
    target.mkdir()
    result = _run_init(target)
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert (target / "README.md").is_file(), "README.md should exist"
    assert (target / ".azure-agent-starter-pack" / "manifest.json").is_file()
    manifest = json.loads((target / ".azure-agent-starter-pack" / "manifest.json").read_text())
    assert manifest["config"]["framework"] == "microsoft_agent_framework"
    assert manifest["config"]["project_type"] == "multi_agent_api"
    readme = (target / "README.md").read_text()
    assert "microsoft_agent_framework" in readme
    assert "{{" not in readme, "No unresolved Jinja2 placeholders"


def test_init_fails_in_non_empty_dir_without_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "non_empty"
    target.mkdir()
    (target / "existing.txt").write_text("keep")
    result = _run_init(target)
    assert result.returncode != 0
    assert "not empty" in result.stderr.lower() or "not empty" in result.stdout.lower() or result.returncode == 1


def test_init_succeeds_in_non_empty_dir_with_overwrite(tmp_path: Path) -> None:
    target = tmp_path / "non_empty2"
    target.mkdir()
    (target / "existing.txt").write_text("keep")
    result = _run_init(target, ["--overwrite"])
    assert result.returncode == 0, f"stderr: {result.stderr}"
    assert (target / "README.md").is_file()


def test_init_fails_for_invalid_combination(tmp_path: Path) -> None:
    target = tmp_path / "bad_combo"
    target.mkdir()
    cmd = [
        sys.executable,
        "-m",
        "azure_agent_starter_pack.cli.app",
        "init",
        str(target),
        "--framework", "nonexistent_framework",
        "--project-type", "multi_agent_api",
        "--pipeline", "github_actions",
        "--runtime", "aks",
        "--iac", "bicep",
        "--non-interactive",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert result.returncode != 0
    generated_files = list(target.iterdir())
    assert len(generated_files) == 0, "No files should be generated for invalid combo"


def test_init_non_interactive_fails_when_option_missing(tmp_path: Path) -> None:
    target = tmp_path / "missing_opt"
    target.mkdir()
    cmd = [
        sys.executable,
        "-m",
        "azure_agent_starter_pack.cli.app",
        "init",
        str(target),
        "--framework", "microsoft_agent_framework",
        "--non-interactive",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    assert result.returncode != 0
