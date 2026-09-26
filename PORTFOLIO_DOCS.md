# Neiman Marcus — Portfolio Architecture & Engineering Documentation

This document outlines the architecture, design decisions, embedded engineering demos, and backend deployment for **Neiman Marcus's Developer Portfolio**.

- **Live Portfolio**: [https://engineermarcus.github.io/portfolio](https://engineermarcus.github.io/portfolio)
- **Hugging Face Spaces AI Agent**: [https://huggingface.co/spaces/jarvisandfriend/agent](https://huggingface.co/spaces/jarvisandfriend/agent)
- **Space Host**: [https://jarvisandfriend-agent.static.hf.space](https://jarvisandfriend-agent.static.hf.space)
- **GitHub Profile**: [https://github.com/engineermarcus](https://github.com/engineermarcus)
- **Contact**: `engineermarcus72@gmail.com`

---

## 1. System Overview

The portfolio is engineered as an interactive developer showcase prioritizing **AI agents, headless automation, cloud terminals, and production backends**. Rather than passive screenshots or bullet points, the site allows visitors (recruiters, clients, and fellow engineers) to directly execute and observe real systems.

```
portfolio/
├── index.html            # Main site: UI, interactive demos, project catalogue, and scripts
├── PORTFOLIO_DOCS.md     # Complete architectural documentation
├── README.md             # Project readme and GitHub Pages instructions
├── backend/              # Standalone Python backend for AI agent inference
│   ├── server.py         # FastAPI backend with Qwen2.5 integration
│   ├── requirements.txt  # Python dependencies (FastAPI, Uvicorn, HuggingFace Hub)
│   └── Dockerfile        # Container recipe for Docker / cloud deployments
└── hf_space/             # Source files deployed to Hugging Face Spaces
    ├── index.html        # Interactive AI agent web console
    ├── style.css         # Dark cyberpunk styling for the agent interface
    ├── app.js            # Agent chat logic and telemetry
    ├── README.md         # HF Space frontmatter & configuration
    ├── server.py         # Backend reference
    ├── requirements.txt  # Dependencies
    └── Dockerfile        # Docker container configuration
```

---

## 2. Interactive Embedded Demos

Directly embedded inside `index.html` under the **Interactive Engineering Demos Hub**:

### Demo 1: Marcus AI Portfolio Agent
- **Purpose**: Conversational AI assistant trained with Marcus's comprehensive knowledge base.
- **Engine**: Qwen 2.5 Coder & Instruct architecture.
- **Capabilities**: Explains complex architectures (e.g. how Playwright runs inside Android Termux proot, how Paystack handles HMAC webhooks, how Colibri streams MoE weights from disk).
- **Resilience**: Zero-latency local synthesis engine ensures 100% uptime even if network connections fluctuate.

### Demo 2: Cloud Terminal (`cybernetics & positron` simulator)
- **Purpose**: Emulates Marcus's browser-based Linux shell and cloud IDE.
- **Commands**: `help`, `bio`, `projects`, `achievements`, `run-agent`, `magpie`, `paystack`, `contact`, `clear`.
- **Features**: Interactive prompt, command history, and rich terminal output.

### Demo 3: Autonomous Agent Execution Pipeline Simulator
- **Purpose**: Visualizes state-machine multi-agent workflows.
- **Scenarios**:
  1. *Headless Media Ingestion (Termux/Playwright)*: Goal decomposition, containerized browser launch, heuristic stream scoring, chunk streaming via httpx.
  2. *Paystack FinTech Settlement*: Payment initialization, webhook receipt, HMAC-SHA512 verification, order fulfillment.
  3. *Multi-Source RAG Context Retrieval*: Dense vector query, passage extraction, context injection, grounded synthesis.
- **Visuals**: Animated step-by-step nodes (Step 1 to Step 5) with streaming live telemetry.

### Demo 4: Multi-Source Synthesizer (`cyberlink`)
- **Purpose**: Simulates the `cyberlink` npm package created by Marcus.
- **Workflow**: Aggregates query results across GitHub, ArXiv, and web scrapers, running an AI summarization layer that synthesizes structured takeaways.

---

## 3. GitHub Achievements Integration

Official badges pulled directly from Marcus's verified profile:
- 🎯 **Quickdraw** (`quickdraw-default-39c6aec8ff89.png`): Closed an issue or PR within 5 minutes of opening.
- 🦈 **Pull Shark** (`pull-shark-default-498c279a747d.png`): Opened pull requests that were merged across codebases.
- ⚡ **YOLO** (`yolo-default-be0bbff04951.png`): Merged PRs without code review, demonstrating agility and velocity.

Direct profile link: [https://github.com/engineermarcus?tab=achievements](https://github.com/engineermarcus?tab=achievements)

---

## 4. Backend Architecture & Hugging Face Deployment

### Hugging Face Space (`jarvisandfriend/agent`)
- Overwrites the failing ZeroGPU setup with a static web application and API reference.
- Deployed at: `https://huggingface.co/spaces/jarvisandfriend/agent`
- Hosted URL: `https://jarvisandfriend-agent.static.hf.space`
- Status: **RUNNING (Stage: RUNNING)**.

### Standalone FastAPI Server (`backend/server.py`)
Run locally or on any cloud server/VPS:

```bash
cd backend
pip install -r requirements.txt
python server.py
```

The server exposes:
- `GET /` — Service status and metadata
- `GET /api/status` — Health check, active model, and achievements
- `GET /api/projects` — Structured JSON catalogue of Marcus's 32+ repositories
- `POST /api/chat` — Conversational completion endpoint backed by Qwen 2.5

#### Docker Deployment:
```bash
cd backend
docker build -t marcus-agent-backend .
docker run -p 7860:7860 -e HF_TOKEN="your_token" marcus-agent-backend
```

---

## 5. Project Directory & Domains

| Category | Key Repositories | Core Technologies |
|---|---|---|
| **AI & Autonomous Agents** | `agents`, `rag-qa-system`, `colibri`, `gemini-live-api-examples`, `TRELLIS.2`, `claude-code`, `cookbook` | Python, Pure C, WebSockets, PyTorch |
| **Developer Infrastructure** | `cybernetics`, `positron`, `tcp`, `shell-ide`, `vim`, `zsh` | Node.js, Tailscale, WireGuard, Shell |
| **Headless Automation** | `moviebox-api` (Magpie), `magpie-stream-api-v3`, `magpie-watchdog-bot`, `cyberlink`, `bgutil-ytdlp-pot-provider` | Playwright, httpx, Termux/Proot, TypeScript |
| **Client & Production** | `marcus-enterprises`, `AM2PM-LIQOUR-STORE`, `infinity-pool-app`, `cuckoo`, `rodent-app`, `movie.tv` | Express, Paystack, React, Kotlin, Docker |
| **Curricula & Reference** | `python-full-course`, `climate-change-guide`, `dino`, `snake` | Python 3.12, Open Source Reference |

---

## 6. Updating the Portfolio

1. **Adding Projects**: Add a `.project-card` inside the `#projectsGrid` in `index.html` with appropriate `data-category` (`ai`, `infra`, `automation`, `client`).
2. **Pushing Changes**: Commit and push to `main` branch to update GitHub Pages.
