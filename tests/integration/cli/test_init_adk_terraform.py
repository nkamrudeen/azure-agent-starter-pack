"""Integration test: Google ADK + Terraform scaffold produces real agent and IaC files."""

import subprocess
import sys
from pathlib import Path


def _scaffold_adk(tmp_path: Path) -> Path:
    target = tmp_path / "adk_project"
    target.mkdir()
    result = subprocess.run(
        [
            sys.executable, "-m", "azure_agent_starter_pack.cli.app",
            "init", str(target),
            "--framework", "google_adk",
            "--project-type", "multi_agent_api",
            "--pipeline", "github_actions",
            "--runtime", "aks",
            "--iac", "terraform",
            "--non-interactive",
        ],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, f"stderr: {result.stderr}"
    return target


def test_adk_agent_files_present(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    assert (target / "app" / "agents" / "root_agent.py").is_file()
    assert (target / "app" / "agents" / "research_agent.py").is_file()
    assert (target / "app" / "agents" / "summariser_agent.py").is_file()
    assert (target / "app" / "tools" / "search_tool.py").is_file()
    assert (target / "app" / "main.py").is_file()


def test_adk_root_agent_has_real_code(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    content = (target / "app" / "agents" / "root_agent.py").read_text()
    assert "from google.adk.agents import Agent" in content
    assert "sub_agents=" in content
    assert "root_agent" in content


def test_requirements_txt_has_adk_deps(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    reqs = (target / "requirements.txt").read_text()
    assert "google-adk" in reqs
    assert "azure-identity" in reqs
    assert "fastapi" in reqs
    assert "uvicorn" in reqs


def test_dockerfile_present(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    dockerfile = (target / "Dockerfile").read_text()
    assert "requirements.txt" in dockerfile
    assert "uvicorn" in dockerfile


def test_env_example_present(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    env = (target / ".env.example").read_text()
    assert "GOOGLE_API_KEY" in env
    assert "KEY_VAULT_URL" in env


def test_terraform_infra_files_present(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    assert (target / "infra" / "main.tf").is_file()
    assert (target / "infra" / "variables.tf").is_file()
    assert (target / "infra" / "outputs.tf").is_file()
    assert (target / "infra" / "dev.tfvars").is_file()
    assert (target / "infra" / ".gitignore").is_file()


def test_terraform_main_has_aks_resources(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    main_tf = (target / "infra" / "main.tf").read_text()
    assert "azurerm_kubernetes_cluster" in main_tf
    assert "azurerm_container_registry" in main_tf
    assert "azurerm_key_vault" in main_tf
    assert "azurerm_resource_group" in main_tf
    assert "azurerm_log_analytics_workspace" in main_tf


def test_terraform_variables_has_aks_vars(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    variables = (target / "infra" / "variables.tf").read_text()
    assert "aks_node_count" in variables
    assert "aks_vm_size" in variables


def test_agent_tests_scaffold(tmp_path: Path) -> None:
    target = _scaffold_adk(tmp_path)
    test_file = (target / "tests" / "test_agents.py").read_text()
    assert "root_agent" in test_file
    assert "research_agent" in test_file
