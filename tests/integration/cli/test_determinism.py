"""Snapshot / determinism test (NFR-001): same inputs → identical output."""

import subprocess
import sys
from pathlib import Path


def _scaffold(target: Path) -> dict[str, str]:
    """Scaffold and return {relative_path: content} dict."""
    result = subprocess.run(
        [
            sys.executable, "-m", "azure_agent_starter_pack.cli.app",
            "init", str(target),
            "--framework", "langgraph",
            "--project-type", "agentic_rag",
            "--pipeline", "github_actions",
            "--runtime", "container_apps",
            "--iac", "terraform",
            "--non-interactive",
        ],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    files: dict[str, str] = {}
    for p in sorted(target.rglob("*")):
        if p.is_file():
            rel = str(p.relative_to(target))
            try:
                files[rel] = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                files[rel] = "<binary>"
    return files


def test_deterministic_output(tmp_path: Path) -> None:
    a = tmp_path / "workspace_a" / "my_project"
    a.mkdir(parents=True)
    b = tmp_path / "workspace_b" / "my_project"
    b.mkdir(parents=True)

    files_a = _scaffold(a)
    files_b = _scaffold(b)

    assert set(files_a.keys()) == set(files_b.keys()), "Same file set"
    for key in files_a:
        assert files_a[key] == files_b[key], f"File {key} differs between runs"
