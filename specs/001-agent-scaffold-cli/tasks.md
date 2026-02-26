# Tasks: Azure Agent Starter Pack CLI

**Input**: Design documents from `specs/001-agent-scaffold-cli/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing. Tests are included per plan (unit per adapter, snapshot, CLI integration).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story (US1–US5)
- Include exact file paths in descriptions

## Path Conventions

- **CLI package**: `src/azure_agent_starter_pack/` (cli/, config/, render/, adapters/, templates/)
- **Tests**: `tests/unit/`, `tests/integration/`, `tests/snapshot/`, `tests/contract/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure per plan.md

- [x] T001 Create directory structure: `src/azure_agent_starter_pack/{cli,config,render,adapters/framework,adapters/project_type,adapters/runtime,adapters/pipeline,templates}` and `tests/{unit,integration,snapshot,contract}` per plan.md
- [x] T002 Add `pyproject.toml` with Python 3.12+ requirement, project name `azure-agent-starter-pack`, and entry point for CLI
- [x] T003 Add dependencies to `pyproject.toml`: typer, pydantic, jinja2, rich, pytest (and dev: pytest-snapshot or similar if used)
- [x] T004 [P] Configure Ruff or Black and Ruff linter in `pyproject.toml` and add minimal config under `src/`

**Checkpoint**: Repo builds with `uv sync`; no CLI commands yet

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story. No user story work can begin until this phase is complete.

- [x] T005 Define Pydantic schema for project configuration in `src/azure_agent_starter_pack/config/schema.py`: framework, project_type, pipeline, runtime, iac, target_dir, template_version, overwrite, non_interactive (enums and validation)
- [x] T006 Implement compatibility matrix in `src/azure_agent_starter_pack/config/compatibility.py`: validate (framework, project_type, pipeline, runtime, iac) and raise clear error for invalid combination (FR-022)
- [x] T007 Implement template loader in `src/azure_agent_starter_pack/render/loader.py`: load templates from bundled path or cache; support cache fallback when network fetch fails (FR-023); return template roots
- [x] T008 Implement template cache in `src/azure_agent_starter_pack/render/cache.py`: cache dir (e.g. user dir), read/write cached templates, version keying
- [x] T009 Implement Jinja2 renderer in `src/azure_agent_starter_pack/render/renderer.py`: render template tree with context; ensure deterministic output (no random/time in context unless fixed); sorted file output
- [x] T010 Create Typer app skeleton in `src/azure_agent_starter_pack/cli/app.py`: `azure-agent-starter-pack` entrypoint, placeholder for init, upgrade, doctor subcommands
- [x] T011 Add base template layout under `src/azure_agent_starter_pack/templates/` (or bundled path): version file, base directory structure for one project type (e.g. multi-agent-api) so renderer has input
- [x] T012 [P] Add unit tests for config schema and compatibility in `tests/unit/test_config_schema.py` and `tests/unit/test_compatibility.py`

**Checkpoint**: Config validates; compatibility matrix fails invalid combos; loader + cache + renderer exist; CLI runs with empty subcommands; foundation ready for user stories

---

## Phase 3: User Story 1 – First-Time Project Scaffold (Priority: P1) – MVP

**Goal**: User runs `init` (interactive or non-interactive) and gets a complete, runnable project with CI/CD, IaC, and Azure config placeholders.

**Independent Test**: Run `azure-agent-starter-pack init` with fixed options in empty dir; verify project generated, build/test pass, deployment docs present.

### Implementation for User Story 1

- [x] T013 [US1] Implement init subcommand in `src/azure_agent_starter_pack/cli/init_cmd.py`: parse options (flags + env for non-interactive); when no TTY, treat as non-interactive and require all options (edge case spec)
- [x] T014 [US1] Add target directory validation in `src/azure_agent_starter_pack/cli/init_cmd.py`: require empty directory or `--overwrite`; fail with clear error otherwise (FR-021)
- [x] T015 [US1] Wire init to config resolution in `src/azure_agent_starter_pack/cli/init_cmd.py`: build Project Configuration from options; validate via compatibility matrix; fail fast on invalid combination without writing files (FR-022)
- [x] T016 [US1] Implement init orchestration in `src/azure_agent_starter_pack/cli/init_cmd.py`: call loader (use cache if fetch fails), renderer with config context, write all files to target_dir; write manifest (`.azure-agent-starter-pack/manifest.json`) per contracts/template-manifest.md
- [x] T017 [US1] Ensure generated project includes README with install, build, test, and deploy steps in template content under `src/azure_agent_starter_pack/templates/` (or adapter-provided)
- [x] T018 [US1] Add CLI integration test for init in `tests/integration/cli/test_init.py`: run init with non-interactive flags in temp empty dir; assert exit 0 and expected files exist; assert no placeholder tokens in key files

**Checkpoint**: Init produces a full project for at least one (framework, project_type, pipeline, runtime, iac) combination; integration test passes

---

## Phase 4: User Story 3 – Configure Framework and Project Type (Priority: P1)

**Goal**: User choices for framework, project type, pipeline, runtime, and IaC are reflected in generated output; at least one full combination works (MVP: Microsoft Agent Framework + Multi-Agent API + GitHub Actions + AKS + Bicep).

**Independent Test**: Run init for Microsoft + multi-agent-api + GitHub Actions + AKS + Bicep; verify structure and entrypoints match project type and runtime.

### Implementation for User Story 3

- [ ] T019 [US3] Define framework adapter interface in `src/azure_agent_starter_pack/adapters/framework/base.py`: list supported project types, provide template roots and Jinja2 context for framework (per plan)
- [ ] T020 [P] [US3] Implement Microsoft Agent Framework adapter in `src/azure_agent_starter_pack/adapters/framework/microsoft.py`: Azure AI Foundry wiring, Managed Identity config, agent composition scaffolding; implement interface from T019
- [ ] T021 [P] [US3] Implement LangGraph adapter in `src/azure_agent_starter_pack/adapters/framework/langgraph.py`: graph nodes, state, Azure OpenAI config; implement interface from T019 (Phase 1 MVP second framework)
- [ ] T022 [US3] Define project type generator interface in `src/azure_agent_starter_pack/adapters/project_type/base.py`: compose layout and entrypoints for multi-agent-api, multi-agent-react-ui, agentic-rag
- [ ] T023 [US3] Implement Multi-Agent API project type in `src/azure_agent_starter_pack/adapters/project_type/multi_agent_api.py`: FastAPI layout, health endpoint, Swagger, OpenTelemetry placeholder, unit test scaffolding (per plan)
- [ ] T024 [US3] Define runtime adapter interface in `src/azure_agent_starter_pack/adapters/runtime/base.py`: emit IaC (Bicep/Helm) and runtime config for AKS, Container Apps, App Service
- [ ] T025 [US3] Implement AKS runtime adapter in `src/azure_agent_starter_pack/adapters/runtime/aks.py`: Helm/Kustomize, HPA, Managed Identity binding, Azure Monitor integration (per plan); Bicep option for IaC
- [ ] T026 [US3] Define pipeline generator interface in `src/azure_agent_starter_pack/adapters/pipeline/base.py`: emit GitHub Actions or Azure DevOps YAML
- [ ] T027 [US3] Implement GitHub Actions pipeline generator in `src/azure_agent_starter_pack/adapters/pipeline/github_actions.py`: build, unit tests, SAST (Semgrep or Bandit), dependency scan, Docker build, push ACR, deploy to runtime (per plan)
- [ ] T028 [US3] Wire init flow to adapters in `src/azure_agent_starter_pack/cli/init_cmd.py`: select framework, project type, runtime, pipeline adapters from config; pass context to renderer; compose output (execution flow from plan)
- [ ] T029 [P] [US3] Add unit tests for Microsoft and LangGraph adapters in `tests/unit/adapters/test_framework_microsoft.py` and `tests/unit/adapters/test_framework_langgraph.py`

**Checkpoint**: Init with framework=Microsoft, project_type=multi-agent-api, pipeline=github-actions, runtime=aks, iac=bicep produces runnable project; US3 independent test passes

---

## Phase 5: User Story 4 – Azure Integration and Security Defaults (Priority: P1)

**Goal**: Generated projects include Managed Identity, Key Vault example, observability (OpenTelemetry + Azure Monitor), and pipeline security scanning (SAST, dependency scan); no hardcoded secrets.

**Independent Test**: After scaffold, inspect for no hardcoded secrets; run generated CI and confirm SAST and dependency scan run; confirm Key Vault and observability present.

### Implementation for User Story 4

- [ ] T030 [US4] Add Managed Identity and Key Vault wiring to base templates and framework adapters: ensure all generated app config uses MI or Key Vault references; add Key Vault example or doc in `src/azure_agent_starter_pack/templates/` or adapter templates (FR-015, FR-016)
- [ ] T031 [US4] Add OpenTelemetry and Azure Monitor hooks to generated project template (e.g. in Multi-Agent API template): logging and metrics export in `src/azure_agent_starter_pack/adapters/project_type/` or shared template (FR-017)
- [ ] T032 [US4] Ensure pipeline generator output includes SAST (Semgrep or Bandit) and dependency scan jobs in `src/azure_agent_starter_pack/adapters/pipeline/github_actions.py` (and future Azure DevOps) (FR-019)
- [ ] T033 [US4] Add ZAP baseline or DAST example for API project type: config or pipeline job in templates/adapters so generated API projects can enable dynamic testing (constitution)
- [ ] T034 [US4] Add unit test scaffolding to generated project template so scaffolded repo includes test layout and example test (FR-018)
- [ ] T035 [P] [US4] Add unit tests for pipeline generator output in `tests/unit/adapters/test_pipeline_github_actions.py`: assert SAST and dependency scan present in generated YAML

**Checkpoint**: Generated project has MI, Key Vault example, observability, SAST/dep scan, unit test scaffolding; US4 independent test passes

---

## Phase 6: User Story 2 – Upgrade Existing Scaffolded Project (Priority: P2)

**Goal**: User runs `upgrade` from project root; CLI applies template changes to template-owned files only; warns on conflicts; preserves user customizations outside owned paths.

**Independent Test**: Scaffold with version N, bump template version to N+1, run upgrade; verify build/tests still pass and manifest updated.

### Implementation for User Story 2

- [ ] T036 [US2] Implement upgrade subcommand in `src/azure_agent_starter_pack/cli/upgrade_cmd.py`: accept PROJECT_ROOT; read `.azure-agent-starter-pack/manifest.json`; if missing or invalid, exit with clear error and do not modify files (FR-003)
- [ ] T037 [US2] Implement upgrade merge logic in `src/azure_agent_starter_pack/cli/upgrade_cmd.py`: load new template version; for each path in manifest `owned_paths`, overwrite with template content; detect conflicts (e.g. user-modified) and warn; do not overwrite paths outside owned_paths
- [ ] T038 [US2] After upgrade, write updated manifest (template_version, etc.) to project in `src/azure_agent_starter_pack/cli/upgrade_cmd.py`
- [ ] T039 [US2] Add `--dry-run` support to upgrade in `src/azure_agent_starter_pack/cli/upgrade_cmd.py`: report changes only, no file writes (per contracts/cli-commands.md)
- [ ] T040 [US2] Add CLI integration test for upgrade in `tests/integration/cli/test_upgrade.py`: scaffold project, run upgrade (or dry-run); assert manifest present and no broken state when upgrade applied

**Checkpoint**: Upgrade updates template-owned files and warns on conflicts; US2 independent test passes

---

## Phase 7: User Story 5 – Deterministic and Fast Scaffolding (Priority: P2)

**Goal**: Same init options produce identical output; init completes in &lt;5 min; doctor command reports required (init needs) vs optional checks and fails only when required checks fail.

**Independent Test**: Run init twice with same options, diff output; run init and measure time; run doctor and verify required/optional reporting.

### Implementation for User Story 5

- [ ] T041 [US5] Implement doctor subcommand in `src/azure_agent_starter_pack/cli/doctor_cmd.py`: run required checks (e.g. Python version, template access/cache); run optional checks (e.g. Azure CLI logged in, Docker); output pass/fail and remediation hints; exit 1 only when required check fails (FR-020, spec clarification)
- [ ] T042 [US5] Audit template context and renderer for determinism in `src/azure_agent_starter_pack/render/renderer.py` and adapter context: no timestamps or random values in output; fixed order for directory listing and file writes (NFR-001)
- [ ] T043 [US5] Add snapshot (golden) test in `tests/snapshot/test_init_output.py`: run init with fixed options, capture tree or checksums; second run must match (deterministic)
- [ ] T044 [US5] Add performance assertion or doc in `tests/integration/cli/test_init.py` or README: init with standard options should complete in under 5 minutes on typical hardware (NFR-002); log duration in CI
- [ ] T045 [US5] Add CLI integration test for doctor in `tests/integration/cli/test_doctor.py`: run doctor; assert required checks reported; assert exit 0 when required pass, exit 1 when required fail (e.g. no template cache)

**Checkpoint**: Init output is deterministic; doctor reports required/optional and exits correctly; US5 independent test passes

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, cross-story tests, and release readiness.

- [ ] T046 [P] Add README at repository root: install (`uv tool install azure-agent-starter-pack`), init/upgrade/doctor usage, options, and link to quickstart
- [ ] T047 Add contract test for CLI exit codes and help in `tests/contract/test_cli_contract.py`: init/upgrade/doctor per contracts/cli-commands.md (exit 0/1, --help)
- [ ] T048 [P] Add golden-file or snapshot tests for at least one full combination (e.g. Microsoft + multi-agent-api + GitHub Actions + AKS) in `tests/snapshot/` to guard regressions
- [ ] T049 Run quickstart.md validation: follow steps in `specs/001-agent-scaffold-cli/quickstart.md` and fix any gaps (paths, commands, or docs)
- [ ] T050 Ensure non-interactive init works when stdin is not a TTY: add or extend test in `tests/integration/cli/test_init.py` that runs init without TTY and all flags; no prompts, deterministic output

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1 — blocks all user stories.
- **Phase 3 (US1)**: Depends on Phase 2 — first deliverable (init end-to-end).
- **Phase 4 (US3)**: Depends on Phase 2 and Phase 3 (init orchestration exists) — framework/project type/runtime/pipeline adapters and wiring.
- **Phase 5 (US4)**: Depends on Phase 4 — template and pipeline content for Azure defaults.
- **Phase 6 (US2)**: Depends on Phase 2 and Phase 3 (manifest and init exist) — upgrade command.
- **Phase 7 (US5)**: Depends on Phase 3 (init) — doctor and determinism.
- **Phase 8 (Polish)**: Depends on Phases 3–7 — docs and cross-cutting tests.

### User Story Dependencies

- **US1 (First-Time Scaffold)**: After Foundational only — MVP.
- **US3 (Framework/Project Type)**: After US1 orchestration — provides adapters so init produces varied output.
- **US4 (Azure/Security)**: After US3 — content for generated projects.
- **US2 (Upgrade)**: After US1 (manifest) — upgrade reads manifest and merges.
- **US5 (Determinism/Doctor)**: After US1 — doctor validates init prerequisites; determinism applies to init output.

### Parallel Opportunities

- Within Phase 1: T004 [P] (lint/config) can run parallel to T001–T003.
- Within Phase 2: T012 [P] (unit tests for config) parallel; T011 (base template) can overlap with T009 (renderer).
- Within Phase 4: T020, T021 [P] (framework adapters), T029 [P] (adapter tests) parallel; T023, T025, T027 (project type, runtime, pipeline) can be parallel after interfaces.
- Within Phase 5: T030–T034 can be parallelized by file; T035 [P] (pipeline tests) parallel.
- Phase 6 (US2) and Phase 7 (US5) can be developed in parallel after Phase 3.
- Phase 8: T046 [P], T048 [P] parallel.

---

## Parallel Example: User Story 3

```text
# After T019 (framework interface) and T022 (project type interface):
T020 (Microsoft adapter) | T021 (LangGraph adapter) | T029 (adapter unit tests)

# After T024 (runtime interface) and T026 (pipeline interface):
T025 (AKS adapter) | T027 (GitHub Actions pipeline)
```

---

## Implementation Strategy

### MVP First (User Story 1 + minimal US3)

1. Complete Phase 1 (Setup) and Phase 2 (Foundational).
2. Complete Phase 3 (US1): init with one hardcoded or minimal combination so a project is generated.
3. Add minimal Phase 4 (US3): one framework adapter (e.g. Microsoft), one project type (multi-agent-api), one runtime (AKS), one pipeline (GitHub Actions), one IaC (Bicep) so init produces the Phase 1 MVP combination.
4. Validate: run init, build generated project, run its tests.
5. Add US4 (Phase 5) so generated project has MI, Key Vault, observability, SAST.
6. Add US2 (upgrade) and US5 (doctor, determinism); then Polish.

### Incremental Delivery

- After Phase 2: Foundation ready; no user-visible commands yet.
- After Phase 3: Init works for one path; MVP demo possible.
- After Phase 4: Init supports framework/project type/pipeline/runtime/IaC choices (MVP matrix).
- After Phase 5: Generated projects are Azure-native and secure by default.
- After Phase 6: Upgrade available for existing users.
- After Phase 7: Doctor and determinism; CI-friendly.
- After Phase 8: Documented and contract/snapshot tested.

### Task Count Summary

| Phase | Task count | Story |
|-------|------------|--------|
| Phase 1 Setup | 4 | — |
| Phase 2 Foundational | 8 | — |
| Phase 3 US1 | 6 | US1 |
| Phase 4 US3 | 11 | US3 |
| Phase 5 US4 | 6 | US4 |
| Phase 6 US2 | 5 | US2 |
| Phase 7 US5 | 5 | US5 |
| Phase 8 Polish | 5 | — |
| **Total** | **50** | — |

**Suggested MVP scope**: Phases 1–3 plus minimal Phase 4 (one framework, one project type, one pipeline, one runtime, one IaC) and Phase 5 (Azure defaults) — delivers runnable, Azure-native scaffold in one command.

---

## Notes

- [P] tasks: different files, no dependencies; safe to run in parallel.
- [USn] labels map tasks to user stories for traceability.
- Each user story phase is independently testable per Independent Test in spec.
- Commit after each task or logical group; stop at any checkpoint to validate.
- Paths assume repo root at project root; adjust if using monorepo layout.
