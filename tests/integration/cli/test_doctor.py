"""Integration tests for the doctor command."""

import subprocess
import sys


def test_doctor_runs_successfully() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "azure_agent_starter_pack.cli.app", "doctor"],
        capture_output=True, text=True, timeout=60,
    )
    assert result.returncode == 0
    assert "doctor" in result.stderr.lower() or "check" in result.stderr.lower()
