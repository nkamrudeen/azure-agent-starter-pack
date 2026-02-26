# Azure Agent Starter Pack

CLI to scaffold production-ready Azure AI Agent projects with configurable frameworks, runtimes, pipelines, and IaC.

## Supported Options

| Dimension | Options |
|-----------|---------|
| **Framework** | `google_adk`, `microsoft_agent_framework`, `langgraph`, `crewai` |
| **Project type** | `multi_agent_api`, `multi_agent_react_ui`, `agentic_rag` |
| **Runtime** | `aks`, `container_apps`, `app_service` |
| **Pipeline** | `github_actions`, `azure_devops` |
| **IaC** | `terraform`, `bicep` |

## Install (development)

```bash
git clone <repo-url> && cd azure-agent-starter-pack
uv sync
```

Or install as a global tool (editable, so changes take effect immediately):

```bash
uv tool install --from . --editable azure-agent-starter-pack
```

## Quick Start

```bash
# 1. Scaffold a project (interactive — prompts for each option)
azure-agent-starter-pack init my-project

# 2. Scaffold non-interactively (CI-friendly)
azure-agent-starter-pack init my-project \
  --framework google_adk \
  --project-type multi_agent_api \
  --pipeline github_actions \
  --runtime aks \
  --iac terraform \
  --non-interactive

# 3. Check prerequisites
azure-agent-starter-pack doctor

# 4. Upgrade a previously scaffolded project
azure-agent-starter-pack upgrade my-project
```

## What Gets Generated

Every scaffolded project includes:

```
my-project/
├── app/                          # Agent application code
│   ├── agents/                   # Agent definitions (framework-specific)
│   ├── tools/                    # Tool implementations
│   └── main.py                   # FastAPI entrypoint
├── tests/                        # Unit tests for agents and tools
├── config/settings.py            # Environment-based config (no hardcoded secrets)
├── src/
│   ├── identity.py               # Azure Managed Identity + Key Vault helper
│   └── observability.py          # OpenTelemetry tracing setup
├── infra/                        # IaC (Terraform or Bicep)
├── k8s/                          # Kubernetes manifests (AKS only)
├── .github/workflows/            # CI/CD pipeline (GitHub Actions)
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Container image
├── run.py                        # Local dev runner script
├── .env.example                  # Environment variable template
├── pyproject.toml                # Python project metadata
├── README.md                     # Project-specific README
└── .azure-agent-starter-pack/
    └── manifest.json             # Tracks config + owned files for upgrade
```

---

## Framework Implementations

### Google ADK

**Scaffold:**
```bash
azure-agent-starter-pack init my-adk-project \
  --framework google_adk --project-type multi_agent_api \
  --pipeline github_actions --runtime aks --iac terraform --non-interactive
```

**What you get:**
- `app/agents/root_agent.py` — Orchestrator agent using `google.adk.agents.Agent` with sub-agents
- `app/agents/research_agent.py` — Research sub-agent with tool bindings
- `app/agents/summariser_agent.py` — Summarisation sub-agent
- `app/tools/search_tool.py` — Stub search tool (replace with Azure AI Search)
- `app/main.py` — FastAPI app with `/run` endpoint that executes the ADK runner

**Run locally:**
```bash
cd my-adk-project
cp .env.example .env              # Fill in GOOGLE_API_KEY
pip install -r requirements.txt

# Option 1: run.py (easiest)
python run.py

# Option 2: uvicorn directly (from project root)
uvicorn app.main:app --reload

# Option 3: python main.py directly
python app/main.py
```

**Test the API:**
```bash
# Health check
curl http://localhost:8000/health

# Swagger UI
open http://localhost:8000/docs

# Run the agent
curl -X POST http://localhost:8000/run \
  -H 'Content-Type: application/json' \
  -d '{"message": "What is Azure AI Search?"}'
```

**Run tests:**
```bash
pip install pytest
pytest tests/
```

---

### Microsoft Agent Framework

**Scaffold:**
```bash
azure-agent-starter-pack init my-ms-project \
  --framework microsoft_agent_framework --project-type multi_agent_api \
  --pipeline github_actions --runtime aks --iac bicep --non-interactive
```

**What you get:**
- `app/agents/orchestrator.py` — Orchestrator using `azure.ai.projects.AIProjectClient` to create agents, threads, and process runs via Azure AI Foundry
- `app/agents/research_agent.py` — Factory for a research agent
- `app/agents/summariser_agent.py` — Factory for a summariser agent
- `app/main.py` — FastAPI app with `/run` endpoint

**Run locally:**
```bash
cd my-ms-project
cp .env.example .env              # Fill in AZURE_AI_PROJECT_CONNECTION_STRING, AZURE_OPENAI_DEPLOYMENT
pip install -r requirements.txt
az login                          # DefaultAzureCredential uses Azure CLI locally

# Option 1: run.py (easiest)
python run.py

# Option 2: uvicorn directly
uvicorn app.main:app --reload

# Option 3: python main.py directly
python app/main.py
```

**Test the API:**
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/run \
  -H 'Content-Type: application/json' \
  -d '{"message": "Summarise Azure Well-Architected Framework"}'
```

**Run tests:**
```bash
pip install pytest
pytest tests/
```

---

### LangGraph

**Scaffold:**
```bash
azure-agent-starter-pack init my-lg-project \
  --framework langgraph --project-type multi_agent_api \
  --pipeline github_actions --runtime container_apps --iac terraform --non-interactive
```

**What you get:**
- `app/agents/graph.py` — LangGraph `StateGraph` with an agent node, tool node, and conditional routing. Uses `AzureChatOpenAI` bound to tools
- `app/tools/search_tool.py` — LangChain `@tool`-decorated search function
- `app/main.py` — FastAPI app that compiles and invokes the graph

**Run locally:**
```bash
cd my-lg-project
cp .env.example .env              # Fill in AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT
pip install -r requirements.txt

# Option 1: run.py (easiest)
python run.py

# Option 2: uvicorn directly
uvicorn app.main:app --reload

# Option 3: python main.py directly
python app/main.py
```

**Test the API:**
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/run \
  -H 'Content-Type: application/json' \
  -d '{"message": "Search for latest AI trends"}'
```

**Run tests:**
```bash
pip install pytest
pytest tests/
```

---

### CrewAI

**Scaffold:**
```bash
azure-agent-starter-pack init my-crew-project \
  --framework crewai --project-type multi_agent_api \
  --pipeline github_actions --runtime app_service --iac bicep --non-interactive
```

**What you get:**
- `app/agents/crew.py` — CrewAI `Crew` with Researcher and Summariser agents, sequential process, and `AzureChatOpenAI` LLM
- `app/tools/search_tool.py` — CrewAI `BaseTool` subclass
- `app/main.py` — FastAPI app that kicks off the crew

**Run locally:**
```bash
cd my-crew-project
cp .env.example .env              # Fill in AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT
pip install -r requirements.txt

# Option 1: run.py (easiest)
python run.py

# Option 2: uvicorn directly
uvicorn app.main:app --reload

# Option 3: python main.py directly
python app/main.py
```

**Test the API:**
```bash
curl http://localhost:8000/health
curl -X POST http://localhost:8000/run \
  -H 'Content-Type: application/json' \
  -d '{"message": "Research cloud-native AI architectures"}'
```

**Run tests:**
```bash
pip install pytest
pytest tests/
```

---

## Agentic RAG (Azure AI Search)

When you select `--project-type agentic_rag`, the project includes a complete RAG pipeline on top of the chosen framework. The RAG pipeline (`app/rag/`) is shared across all frameworks; only the agent reasoning layer differs.

**Extra files generated:** `app/rag/` (config, chunker, embedder, indexer, retriever), `app/tools/retrieval_tool.py`, `data/sample.txt`, `scripts/index_documents.py`, `requirements-rag.txt`, `tests/test_rag_pipeline.py`.

**Scaffold (example with Google ADK):**

```bash
azure-agent-starter-pack init my-rag-project \
  --framework google_adk --project-type agentic_rag \
  --pipeline github_actions --runtime aks --iac terraform --non-interactive
```

**How the pipeline works:** Chunk (LangChain `RecursiveCharacterTextSplitter`) -> Embed (Azure OpenAI `text-embedding-3-small`) -> Index (Azure AI Search with HNSW vector search) -> Retrieve (hybrid keyword + vector search) -> Agent reasons over retrieved context.

The generated `main.py` exposes both `/search` (direct retrieval) and `/run` (agent-powered RAG).

**Run locally:**

```bash
cd my-rag-project
cp .env.example .env   # Fill in AZURE_AI_SEARCH_ENDPOINT, AZURE_OPENAI_ENDPOINT, API keys
pip install -r requirements.txt && pip install -r requirements-rag.txt
az login
python scripts/index_documents.py          # Index sample doc (or pass a .pdf/.txt path)
python run.py                              # Start FastAPI server
```

**Test the API:**

```bash
curl -X POST http://localhost:8000/search -H 'Content-Type: application/json' \
  -d '{"message": "What is vector search?"}'

curl -X POST http://localhost:8000/run -H 'Content-Type: application/json' \
  -d '{"message": "Explain how Azure AI Search handles hybrid queries"}'
```

---

## Infrastructure as Code

### Terraform

Generated in `infra/` with runtime-conditional resources:
- `main.tf` — Resource Group, ACR, Key Vault, Log Analytics + runtime (AKS cluster, Container App, or App Service)
- `variables.tf` — Parameterised with sensible defaults
- `outputs.tf` — ACR login server, KV URI, cluster/app endpoints
- `dev.tfvars` — Dev environment defaults

```bash
cd infra
terraform init
terraform plan -var-file=dev.tfvars
terraform apply -var-file=dev.tfvars
```

### Bicep

Generated in `infra/`:
- `main.bicep` — Same resources as Terraform, parameterised
- `params.dev.json` — Dev environment parameters

```bash
cd infra
az deployment group create \
  --resource-group <rg> \
  --template-file main.bicep \
  --parameters @params.dev.json
```

---

## AKS Deployment (Kubernetes Manifests)

When `--runtime aks` is selected, a `k8s/` directory is generated with:

| File | Purpose |
|------|---------|
| `namespace.yaml` | Dedicated namespace |
| `deployment.yaml` | Pod spec with health probes, resource limits, Workload Identity |
| `service.yaml` | ClusterIP service |
| `ingress.yaml` | NGINX ingress with TLS |
| `hpa.yaml` | Horizontal Pod Autoscaler (CPU/memory) |
| `configmap.yaml` | Environment config (non-secret values) |
| `service-account.yaml` | Workload Identity service account |
| `kustomization.yaml` | Kustomize entrypoint |

**Deploy to AKS:**
```bash
# Get AKS credentials
az aks get-credentials --resource-group <rg> --name <cluster>

# Build and push container
docker build -t <acr>.azurecr.io/my-project:latest .
docker push <acr>.azurecr.io/my-project:latest

# Update image reference in k8s/deployment.yaml, then:
kubectl apply -k k8s/
```

---

## CI/CD Pipeline

GitHub Actions pipeline (`.github/workflows/ci.yml`) includes:
- **Build & Test** — `uv sync` + `pytest`
- **SAST** — Bandit static analysis
- **Dependency Scan** — pip-audit
- **ZAP DAST** — Baseline scan (for API project types)
- **Docker Build** — Container image
- **Deploy** — Multi-environment (dev/stage/prod)

---

## Security

Every generated project follows Azure security best practices:
- **Managed Identity** via `DefaultAzureCredential` (no static keys)
- **Key Vault** integration for secrets
- **Workload Identity** on AKS (federated credential binding)
- **RBAC** — ACR pull role for AKS, KV access via RBAC
- **No secrets in code or config** — `.env.example` is a template, `.env` is gitignored

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `init <dir>` | Scaffold a new project |
| `upgrade <dir>` | Update to newer template version |
| `doctor` | Check prerequisites |

| Flag | Description |
|------|-------------|
| `--framework` / `-f` | Agent framework |
| `--project-type` / `-p` | Project type |
| `--pipeline` | CI/CD pipeline |
| `--runtime` / `-r` | Runtime environment |
| `--iac` | Infrastructure as Code |
| `--non-interactive` | Fail if any option missing (CI mode) |
| `--overwrite` | Allow scaffold into non-empty directory |
| `--template-version` | Pin template version |
� Bandit static analysis
- **Dependency Scan** — pip-audit
- **ZAP DAST** — Baseline scan (for API project types)
- **Docker Build** — Container image
- **Deploy** — Multi-environment (dev/stage/prod)

---

## Security

Every generated project follows Azure security best practices:
- **Managed Identity** via `DefaultAzureCredential` (no static keys)
- **Key Vault** integration for secrets
- **Workload Identity** on AKS (federated credential binding)
- **RBAC** — ACR pull role for AKS, KV access via RBAC
- **No secrets in code or config** — `.env.example` is a template, `.env` is gitignored

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `init <dir>` | Scaffold a new project |
| `upgrade <dir>` | Update to newer template version |
| `doctor` | Check prerequisites |

| Flag | Description |
|------|-------------|
| `--framework` / `-f` | Agent framework |
| `--project-type` / `-p` | Project type |
| `--pipeline` | CI/CD pipeline |
| `--runtime` / `-r` | Runtime environment |
| `--iac` | Infrastructure as Code |
| `--non-interactive` | Fail if any option missing (CI mode) |
| `--overwrite` | Allow scaffold into non-empty directory |
| `--template-version` | Pin template version |

---

## Template Source Structure

Templates are organized by **framework > project type**, with shared infrastructure and overlays:

```
src/azure_agent_starter_pack/templates/
├── _common/                          # Shared across all combos
│   ├── config/settings.py.j2
│   ├── src/identity.py.j2
│   ├── src/observability.py.j2
│   ├── pyproject.toml.j2
│   └── run.py.j2
├── google_adk/
│   ├── multi_agent_api/              # Self-contained: app/, tests/, Dockerfile, etc.
│   ├── agentic_rag/                  # Includes app/rag/, scripts/, data/
│   └── multi_agent_react_ui/         # Includes frontend/ (React + Vite)
├── microsoft_agent_framework/
│   ├── multi_agent_api/
│   ├── agentic_rag/
│   └── multi_agent_react_ui/
├── langgraph/
│   ├── multi_agent_api/
│   ├── agentic_rag/
│   └── multi_agent_react_ui/
├── crewai/
│   ├── multi_agent_api/
│   ├── agentic_rag/
│   └── multi_agent_react_ui/
├── pipelines/
│   ├── github_actions/               # .github/workflows/
│   └── azure_devops/
├── runtimes/
│   ├── aks/                          # k8s/ manifests
│   ├── container_apps/
│   └── app_service/
└── iac/
    ├── terraform/                    # infra/ (main.tf, variables.tf, etc.)
    └── bicep/                        # infra/ (main.bicep, params.dev.json)
```

Rendering order: `_common/` → `<framework>/<project_type>/` → `iac/<iac>/` → `runtimes/<runtime>/` → `pipelines/<pipeline>/`
