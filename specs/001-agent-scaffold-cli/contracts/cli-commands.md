# CLI Command Contract: azure-agent-starter-pack

**Branch**: `001-agent-scaffold-cli` | **Date**: 2025-02-25  
**Purpose**: Public CLI surface for tools and automation.

## Entrypoint

- **Command name**: `azure-agent-starter-pack` (or `aasp` if alias provided)
- **Install**: `uv tool install azure-agent-starter-pack`

## Subcommands

### init

Scaffold a new Azure AI Agent project.

**Usage** (conceptual):

```text
azure-agent-starter-pack init [OPTIONS] [TARGET_DIR]
```

**Options** (all optional in interactive mode; required in non-interactive for deterministic CI):

| Option | Type | Default | Description |
|--------|------|--------|-------------|
| `--framework` | choice | prompt | One of: google-adk, microsoft-agent-framework, crewai, langgraph |
| `--project-type` | choice | prompt | One of: multi-agent-api, multi-agent-react-ui, agentic-rag |
| `--pipeline` | choice | prompt | One of: github-actions, azure-devops |
| `--runtime` | choice | prompt | One of: aks, container-apps, app-service |
| `--iac` | choice | prompt | One of: terraform, bicep |
| `--template-version` | string | latest | Template version (semver or tag) |
| `--overwrite` | flag | false | Allow init in non-empty directory |
| `--non-interactive` | flag | false | Fail if any option missing; no prompts |

**Environment**: Options MAY be supplied via env vars (e.g. `AASP_FRAMEWORK`) for non-interactive mode.

**Exit codes**:

- `0`: Project generated successfully.
- `1`: Validation error (invalid combination, non-empty dir without overwrite, template fetch failed with no cache), or init failed; no partial generation.

**Output**: Files written under `TARGET_DIR` (default: current directory). Deterministic for same CLI version, template version, and options (NFR-001).

---

### upgrade

Update an existing scaffolded project to a newer template version.

**Usage**:

```text
azure-agent-starter-pack upgrade [OPTIONS] [PROJECT_ROOT]
```

**Options**:

| Option | Type | Default | Description |
|--------|------|--------|-------------|
| `--template-version` | string | next compatible | Target template version |
| `--dry-run` | flag | false | Report changes only; do not modify files |

**Exit codes**:

- `0`: Upgrade applied (or dry-run completed).
- `1`: Not a scaffolded project; or upgrade failed (e.g. conflict resolution required).

**Behavior**: Auto-merge template-owned files; overwrite only paths in template manifest; warn on conflicts (per spec clarification).

---

### doctor

Validate environment and configuration for init.

**Usage**:

```text
azure-agent-starter-pack doctor [OPTIONS]
```

**Options**: None required.

**Exit codes**:

- `0`: All required checks pass (what init needs: runtime, template access).
- `1`: At least one required check failed.

**Output**: Human-readable report of required checks (pass/fail) and optional checks (status + hints). Optional checks (e.g. Azure login, cloud CLI) do not cause exit 1 (per spec clarification).

---

## Help and Version

- `azure-agent-starter-pack --help`: Global help.
- `azure-agent-starter-pack init --help`: Init-specific help.
- `azure-agent-starter-pack --version`: CLI version (and optionally template version range).

## Error Messages

- **Invalid combination**: Clear message that the (framework, project_type, pipeline, runtime, iac) combination is unsupported; suggest valid combinations if feasible.
- **Non-empty directory**: Clear message that target directory is non-empty and overwrite is not set; suggest `--overwrite` or empty directory.
- **Template fetch failed**: Clear message that template fetch failed and no cache was available; suggest connectivity or cache.
- **Not a scaffolded project**: Clear message when upgrade or doctor (in project context) is run in a directory that is not a scaffolded project.
