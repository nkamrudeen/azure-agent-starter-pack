<!--
Sync Impact Report
- Version change: 1.0.0 → 2.0.0 (MINOR: new sections + expanded principles; formal constitution scope)
- Modified principles: Security Built-In → Secure-by-default; DX expanded; added Enterprise readiness, Versioned templates
- Added sections: Preamble, Architecture Standards, Security Mandates, Non-Goals
- Removed sections: None
- Templates: plan-template.md ✅ updated (Constitution Check gates)
- Follow-up TODOs: None
-->

# Azure Agent Starter Pack — Engineering Constitution

## Preamble

**Project**: azure-agent-starter-pack  
**Type**: Open-source CLI  
**Install**: `uv tool install azure-agent-starter-pack`

This constitution governs the design, implementation, and evolution of a **production-grade Azure-native AI Agent scaffolding CLI**. All generated templates, defaults, and tooling MUST comply with the principles and mandates below. This document is the authoritative source for compliance checks in `/speckit.plan` and `/speckit.analyze`.

---

## 1. Governing Principles

### 1.1 Azure-Native First

All generated templates and defaults MUST:

- Use **Managed Identity** by default for Azure resource access
- Integrate **Azure RBAC** for authorization
- Use **Azure Key Vault** (or equivalent) for secrets; no static secrets in code or config
- Align with **Entra ID** for identity and **Azure Well-Architected Framework** for resilience, security, and cost

### 1.2 Production-Ready Defaults

Every scaffolded project MUST include:

- **CI/CD** pipelines (build, test, deploy)
- **Security scanning** (SAST, dependency scan) in pipeline
- **Observability** hooks (logging, metrics, tracing where applicable)
- **Environment separation**: dev, stage, prod MUST be supported

No toy or demo-only examples in official templates.

### 1.3 Opinionated Golden Path Architecture

The CLI MUST enforce a single, well-documented golden path:

- Structured repository layout
- Clear separation of agent logic, orchestration, infrastructure, and pipelines
- Standardized configuration model
- Infrastructure-as-Code as the default deployment model

### 1.4 Secure-by-Default Templates

Every template MUST:

- Assume zero trust: no hardcoded secrets, no implicit trust boundaries
- Include Managed Identity integration and Key Vault pattern
- Include SAST and dependency scanning examples
- Include ZAP baseline or DAST example where applicable
- Use environment variable isolation for configuration

### 1.5 Extensible Plugin Architecture

The CLI MUST:

- Support **pluggable frameworks** (agent runtimes, orchestration backends)
- Support **new runtimes** without forking the core
- Enable a **future plugin ecosystem** (discovery, versioning, lifecycle)

### 1.6 Versioned Template System

Templates MUST be versioned. The CLI MUST:

- Allow template versioning and selection
- Support backward-compatible upgrades and clear upgrade paths
- Produce **deterministic template output** for a given version and options

### 1.7 Enterprise Readiness

Scaffolded output MUST be suitable for enterprise use:

- Compliance-friendly patterns (secrets in vaults, audit-friendly logging)
- Dev/Stage/Prod separation mandatory
- Documentation and operational runbooks where applicable

---

## 2. Architecture Standards

### 2.1 Separation of Concerns

Generated projects MUST clearly separate:

- **Agent logic**: core reasoning, tools, prompts
- **Orchestration**: workflow, scheduling, retries
- **Infrastructure**: compute, networking, identity
- **Pipelines**: CI/CD, security scans, deployment

These boundaries MUST be reflected in repository layout and configuration.

### 2.2 Infrastructure-as-Code Required

Deployment and environment definition MUST be expressed as code:

- **Bicep** and/or **Helm** and/or **YAML** (e.g., GitHub Actions, Azure DevOps) as appropriate
- No manual-only or one-off scripts as the primary deployment path
- IaC MUST be part of the scaffolded output

### 2.3 No Hardcoded Secrets

Secrets MUST NOT appear in source code, config files, or IaC in plain form. Use:

- Managed Identity, Key Vault references, or environment variables
- Pipeline secrets (e.g., GitHub Secrets, Azure DevOps variables) for pipeline-only values

### 2.4 Dev/Stage/Prod Separation Mandatory

Environments MUST be distinct:

- Separate config or parameter sets per environment
- No shared production credentials with non-production
- Deployment pipelines MUST support promoting through dev → stage → prod

### 2.5 Cloud-Agnostic Internal, Azure-Optimized Output

- **Internal architecture** of the CLI and templates MAY be cloud-agnostic (e.g., abstract storage, identity) to aid maintainability
- **Generated output** MUST be Azure-optimized: Azure-native services, Azure RBAC, Entra ID, Key Vault, and Well-Architected patterns

---

## 3. Security Mandates

### 3.1 Managed Identity Required

Scaffolded applications and services MUST use **Managed Identity** for Azure resource access where applicable. Static connection strings or API keys for Azure services are prohibited in templates.

### 3.2 SAST and Dependency Scan Included

Every scaffold MUST include:

- **SAST** (Static Application Security Testing) in the CI pipeline
- **Dependency scanning** (e.g., for known vulnerabilities) in the CI pipeline

### 3.3 ZAP Baseline or DAST Example

Where the scaffold produces a deployable web app or API, a **ZAP baseline** or **DAST example** MUST be included (e.g., pipeline job or documented run) so adopters can enable dynamic testing.

### 3.4 Environment Variable Isolation

Configuration MUST support environment-based isolation. Secrets and environment-specific values MUST be supplied via environment variables or a secure store (e.g., Key Vault), not baked into images or code.

### 3.5 mTLS for Multi-Service Deployments

For scaffolds that include **multi-service** or service-to-service communication, **mTLS support** MUST be documented or exemplified (e.g., via service mesh or application-level TLS with client certs) so adopters can enforce mutual authentication.

---

## 4. Developer Experience Principles

### 4.1 One-Command Scaffolding

Users MUST be able to scaffold a full project with a **single command** (e.g., `azure-agent-starter-pack init` or equivalent). Optional flags MAY customize runtime, framework, or target directory.

### 4.2 Clear CLI UX

CLI behavior MUST be predictable and documented:

- Consistent subcommands and flags
- Clear help text and error messages
- No silent failures for critical operations

### 4.3 Doctor Command for Validation

The CLI MUST provide a **doctor** (or equivalent) command that validates:

- Local environment (e.g., Azure CLI, uv, runtimes)
- Permissions and configuration
- Template or project consistency

### 4.4 Deterministic Template Output

For a given CLI version, template version, and set of options, generated output MUST be **deterministic** (reproducible) to support diffing, review, and automation.

### 4.5 Backward-Compatible Upgrades

Template and CLI upgrades SHOULD be **backward-compatible** where feasible. Breaking changes MUST be documented and, when possible, accompanied by migration guidance or versioned templates.

---

## 5. Non-Goals

The following are explicitly **out of scope** for this constitution and the CLI:

- **Not a full provisioning engine**: The CLI scaffolds structure and patterns; it does not replace Terraform, Bicep, or platform provisioning at scale beyond what is needed for the scaffold.
- **Not a low-code tool**: Output is code and IaC intended for developers; no proprietary low-code or no-code runtime is mandated.
- **Not framework-specific lock-in**: Extensibility and pluggable runtimes are required; the CLI MUST NOT mandate a single agent framework to the exclusion of others.

---

## 6. Governance

- This constitution **supersedes** ad-hoc practices for the Azure Agent Starter Pack. All PRs and reviews MUST verify compliance with the principles and mandates above.
- **Amendments** require documentation, approval, and a migration plan when existing templates or behavior are affected.
- **Versioning**: Constitution versions follow semantic versioning (MAJOR.MINOR.PATCH). MAJOR for backward-incompatible principle removals or redefinitions; MINOR for new sections or materially expanded guidance; PATCH for clarifications and non-semantic fixes.
- This file is the authority for `/speckit.plan` Constitution Check gates and `/speckit.analyze` alignment.

**Version**: 2.0.0 | **Ratified**: 2025-02-25 | **Last Amended**: 2025-02-25
