"""Integration tests for the upgrade command."""

import json
import subprocess
import sys
from pathlib import Path


def _init_project(tmp_path: Path) -> Path:
    target = tmp_path / "proj"
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
    assert result.returncode == 0, f"init failed: {result.stderr}"
    return target


def test_upgrade_already_up_to_date(tmp_path: Path) -> None:
    target = _init_project(tmp_path)
    result = subprocess.run(
        [sys.executable, "-m", "azure_agent_starter_pack.cli.app", "upgrade", str(target)],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0
    assert "up to date" in result.stderr.lower()


def test_upgrade_dry_run(tmp_path: Path) -> None:
    target = _init_project(tmp_path)
    manifest_path = target / ".azure-agent-starter-pack" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["template_version"] = "0.0.1"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    result = subprocess.run(
        [sys.executable, "-m", "azure_agent_starter_pack.cli.app", "upgrade", str(target), "--dry-run"],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0
    assert "dry run" in result.stderr.lower()


def test_upgrade_applies_changes(tmp_path: Path) -> None:
    target = _init_project(tmp_path)
    manifest_path = target / ".azure-agent-starter-pack" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["template_version"] = "0.0.1"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    result = subprocess.run(
        [sys.executable, "-m", "azure_agent_starter_pack.cli.app", "upgrade", str(target)],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0
    assert "upgraded" in result.stderr.lower()
    manifest_after = json.loads(manifest_path.read_text())
    assert manifest_after["template_version"] == "1.0.0"


def test_upgrade_fails_without_manifest(tmp_path: Path) -> None:
    target = tmp_path / "bare"
    target.mkdir()
    result = subprocess.run(
        [sys.executable, "-m", "azure_agent_starter_pack.cli.app", "upgrade", str(target)],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode != 0
