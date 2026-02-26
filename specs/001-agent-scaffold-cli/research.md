# Research: Azure Agent Starter Pack CLI

**Branch**: `001-agent-scaffold-cli` | **Date**: 2025-02-25  
**Purpose**: Resolve technical unknowns and document decisions for the implementation plan.

## Technical Context Resolutions

No NEEDS CLARIFICATION remained in the plan; the following decisions are documented for traceability.

### 1. CLI Framework and Config Validation

**Decision**: Typer for CLI; Pydantic for configuration schema validation.

**Rationale**: Typer provides subcommands, flags, and Rich-compatible UX with minimal boilerplate. Pydantic gives strict validation for framework/project type/pipeline/runtime/IaC combinations and clear error messages for invalid combinations (fail fast, no partial generation).

**Alternatives considered**: Click (more verbose); argparse (no schema validation); custom parser (unnecessary given Typer + Pydantic).

### 2. Template Rendering and Determinism

**Decision**: Jinja2 for template rendering; fixed random seed and sorted file/output order where applicable to ensure deterministic output.

**Rationale**: Jinja2 is widely used, supports includes and inheritance, and integrates with Python. Determinism is required by spec (NFR-001); ordering and no time-dependent tokens in templates achieve reproducibility.

**Alternatives considered**: Mako (less common); string.Template (too limited); code-generation (harder to maintain templates).

### 3. Template Cache and Network Failure

**Decision**: Use cached templates when available; when no cache and network (or registry) fetch fails, fail with clear error and do not generate (per spec clarification).

**Rationale**: Aligns with spec FR-023 and clarification: cache improves offline/CI UX; no silent fallback to stale or missing templates.

**Alternatives considered**: Always require network (poor offline); always use bundle only (no updates without new CLI release). Chosen approach balances both.

### 4. Framework Adapter Interface

**Decision**: Each framework adapter implements a common interface: list supported project types, provide template roots and context, inject Azure (MI, Key Vault, OpenAI/Foundry) wiring.

**Rationale**: Enables pluggable frameworks and consistent behavior across Google ADK, Microsoft Agent Framework, CrewAI, LangGraph. Isolates framework API drift.

**Alternatives considered**: Monolithic templates per framework (combinatorial explosion); single generic adapter (does not fit distinct framework semantics).

### 5. Upgrade Merge Strategy

**Decision**: Auto-merge for template-owned files; overwrite only files that belong to the template manifest; warn on conflicts (per spec clarification).

**Rationale**: Spec clarification chose auto-merge with overwrite only template-owned files and warn on conflicts. Template manifest (list of template-owned paths) enables safe merge.

**Alternatives considered**: Report-only (rejected per user choice A); full three-way merge (higher complexity; deferred if needed).

### 6. Doctor Required vs Optional Checks

**Decision**: Required checks = only what init needs (e.g. Python/runtime, template access). Optional = Azure login, cloud CLI, etc.; report but do not fail doctor (per spec clarification).

**Rationale**: Spec clarification: doctor fails only when a required check fails; optional checks give hints without blocking.

**Alternatives considered**: All advisory (rejected); all required (too strict for pre-deploy validation).

## Best Practices Referenced

- **Azure Well-Architected**: Resilience, security, cost; Managed Identity and Key Vault patterns.
- **CI/CD**: Security scanning (SAST, dependency scan) in pipeline; environment promotion dev → stage → prod.
- **Template versioning**: Embedded version metadata; backward-compatible upgrades; migration scripts for breaking changes.

## Open Items (Deferred to Implementation)

- Exact template manifest format for upgrade (list of paths or checksums).
- Optional template registry URL and update-check behavior.
- Golden file set for snapshot tests (per combination subset for Phase 1).
