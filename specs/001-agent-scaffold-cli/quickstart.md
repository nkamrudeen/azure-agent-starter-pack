# Quickstart: Azure Agent Starter Pack CLI

**Branch**: `001-agent-scaffold-cli` | **Date**: 2025-02-25  
**Audience**: Developers implementing or testing the CLI.

## Prerequisites

- Python 3.12+
- uv (recommended): `pip install uv` or [install guide](https://github.com/astral-sh/uv)
- Azure subscription (for deploying generated projects; optional for local scaffold and tests)

## Install CLI

From the repo root (development):

```bash
uv sync
uv run azure-agent-starter-pack --help
```

Or install as a global tool from the local checkout:

```bash
uv tool install --from /path/to/azure-agent-starter-pack azure-agent-starter-pack
```

> **Note**: The package is not yet published to PyPI. Once published, you will be able to run `uv tool install azure-agent-starter-pack` directly.

## First scaffold (init)

1. Create an empty directory:

   ```bash
   mkdir my-agent && cd my-agent
   ```

2. Run init (interactive):

   ```bash
   azure-agent-starter-pack init
   ```

   You will be prompted for: framework, project type, pipeline, runtime, IaC. Defaults may be offered.

3. Or run init non-interactive (CI):

   ```bash
   azure-agent-starter-pack init --framework microsoft-agent-framework --project-type multi-agent-api --pipeline github-actions --runtime aks --iac bicep --non-interactive
   ```

4. Verify:

   ```bash
   # Build and test (example for Python backend)
   uv sync
   uv run pytest
   ```

## Validate environment (doctor)

```bash
azure-agent-starter-pack doctor
```

- Required checks (must pass for init): e.g. Python version, template access.
- Optional checks (reported only): e.g. Azure CLI logged in, Docker.

## Upgrade a scaffolded project

From the project root of a previously scaffolded project:

```bash
azure-agent-starter-pack upgrade
```

- Template-owned files are updated; user customizations outside those paths are preserved. Conflicts are warned.

## Project layout (generated)

After init, you get (example for Multi-Agent API + AKS + GitHub Actions):

- **Agent / app**: `src/` (or backend layout per project type)
- **CI/CD**: `.github/workflows/` or Azure DevOps YAML
- **Infra**: `infra/` (Bicep or Terraform for AKS / Container Apps / App Service)
- **Config**: Environment-specific config; no hardcoded secrets; Key Vault example
- **Manifest**: `.azure-agent-starter-pack/manifest.json` for upgrade

## Key constraints (from spec)

- **Empty directory**: Init requires an empty target directory unless `--overwrite` is set.
- **Valid combination**: Framework × project type × pipeline × runtime × IaC must be a supported combination; otherwise init fails with clear error and no partial generation.
- **Template fetch**: If templates cannot be fetched and no cache exists, init fails with clear error.

## Next steps

- Implement Phase 1 (MVP): Microsoft Agent Framework + LangGraph, Multi-Agent API, GitHub Actions, AKS (see [plan.md](./plan.md) Phased Rollout).
- Add unit and snapshot tests per [plan.md](./plan.md) Testing Strategy.
- Run Constitution Check on generated output (see [plan.md](./plan.md) Constitution Check).
