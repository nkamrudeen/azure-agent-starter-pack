# Template Manifest Contract

**Branch**: `001-agent-scaffold-cli` | **Date**: 2025-02-25  
**Purpose**: Machine-readable manifest embedded in scaffolded projects for upgrade and validation.

## Location

Inside scaffolded project:

- **Path**: `.azure-agent-starter-pack/manifest.json` (or equivalent; exact path TBD in implementation)

## Schema (conceptual)

Manifest identifies the project as scaffolded by this CLI and lists template-owned paths for safe upgrade merge.

```json
{
  "schema_version": "1",
  "cli_tool": "azure-agent-starter-pack",
  "cli_version": "<semver>",
  "template_version": "<semver or tag>",
  "generated_at": "<ISO8601>",
  "config": {
    "framework": "microsoft-agent-framework",
    "project_type": "multi-agent-api",
    "pipeline": "github-actions",
    "runtime": "aks",
    "iac": "bicep"
  },
  "owned_paths": [
    "src/",
    ".github/workflows/",
    "infra/",
    "README.md"
  ]
}
```

## Fields

| Field | Type | Description |
|-------|------|-------------|
| schema_version | string | Manifest schema version for future evolution |
| cli_tool | string | Tool name (e.g. azure-agent-starter-pack) |
| cli_version | string | CLI version that generated this project |
| template_version | string | Template version used |
| generated_at | string | ISO8601 timestamp (informational; not used for determinism) |
| config | object | Snapshot of Project Configuration (framework, project_type, pipeline, runtime, iac) |
| owned_paths | array of string | Paths (relative to project root) that belong to template; safe to overwrite on upgrade |

## Upgrade Semantics

- **upgrade** command reads manifest from `PROJECT_ROOT`.
- If manifest missing or invalid → exit with "Not a scaffolded project".
- Only files under `owned_paths` (or their children) are overwritten by template; user-added files outside these paths are preserved.
- Conflicts (user-modified template-owned file) → warn and optionally skip or report; exact behavior TBD (warn on conflicts per spec).

## Optional Extensions

- `checksums`: map of path → hash for conflict detection (optional in v1).
- `plugins` or `extensions`: for future plugin ecosystem (out of scope for Phase 1).
