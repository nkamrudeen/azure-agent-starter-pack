"""Verify that generated projects have runnable main.py (sys.path fix works)."""

import subprocess
import sys
from pathlib import Path

import pytest

FRAMEWORKS = ["google_adk", "microsoft_agent_framework", "langgraph", "crewai"]


def _scaffold(tmp_path: Path, framework: str) -> Path:
    target = tmp_path / f"{framework}_proj"
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


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_main_py_has_sys_path_fix(tmp_path: Path, framework: str) -> None:
    """Verify main.py contains sys.path insertion so it works with `python app/main.py`."""
    target = _scaffold(tmp_path, framework)
    main_py = (target / "app" / "main.py").read_text()
    assert "sys.path.insert" in main_py, f"{framework}: main.py must fix sys.path for direct execution"


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_main_py_syntax_valid(tmp_path: Path, framework: str) -> None:
    """Verify main.py has valid Python syntax (compiles without error)."""
    target = _scaffold(tmp_path, framework)
    result = subprocess.run(
        [sys.executable, "-c", f"import py_compile; py_compile.compile(r'{target / 'app' / 'main.py'}', doraise=True)"],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"[{framework}] syntax error: {result.stderr}"


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_run_py_present(tmp_path: Path, framework: str) -> None:
    """Verify run.py is generated at project root."""
    target = _scaffold(tmp_path, framework)
    assert (target / "run.py").is_file(), f"{framework}: run.py should exist"
    content = (target / "run.py").read_text()
    assert "uvicorn" in content
    assert "app.main:app" in content


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_run_py_syntax_valid(tmp_path: Path, framework: str) -> None:
    target = _scaffold(tmp_path, framework)
    result = subprocess.run(
        [sys.executable, "-c", f"import py_compile; py_compile.compile(r'{target / 'run.py'}', doraise=True)"],
        capture_output=True, text=True, timeout=30,
    )
    assert result.returncode == 0, f"[{framework}] run.py syntax error: {result.stderr}"


@pytest.mark.parametrize("framework", FRAMEWORKS)
def test_all_agent_files_syntax_valid(tmp_path: Path, framework: str) -> None:
    """Verify all generated .py files are syntactically valid."""
    target = _scaffold(tmp_path, framework)
    py_files = list(target.rglob("*.py"))
    assert len(py_files) > 0
    for py_file in py_files:
        result = subprocess.run(
            [sys.executable, "-c", f"import py_compile; py_compile.compile(r'{py_file}', doraise=True)"],
            capture_output=True, text=True, timeout=30,
        )
        assert result.returncode == 0, f"[{framework}] {py_file.relative_to(target)} syntax error: {result.stderr}"
