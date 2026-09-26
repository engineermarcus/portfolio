# Neiman Marcus — Portfolio

Modern developer portfolio highlighting autonomous AI agents, cloud dev environments, headless automation, and client platforms pulled from [github.com/engineermarcus](https://github.com/engineermarcus).

- **Live Site**: [https://engineermarcus.github.io/portfolio](https://engineermarcus.github.io/portfolio)
- **Hugging Face Space Backend**: [https://huggingface.co/spaces/jarvisandfriend/agent](https://huggingface.co/spaces/jarvisandfriend/agent)
- **Architecture Documentation**: See [PORTFOLIO_DOCS.md](PORTFOLIO_DOCS.md)

## Highlights

- ⚡ **Interactive Engineering Demos Hub**: Directly embedded on the site:
  1. **Marcus AI Portfolio Agent** — Conversational knowledge assistant backed by Qwen 2.5.
  2. **Cloud Terminal (`cybernetics`)** — Live browser-based Linux shell emulator.
  3. **Autonomous Agent Pipeline** — Interactive multi-agent step-by-step workflow simulator.
  4. **Multi-Source Synthesizer (`cyberlink`)** — Real-time research aggregation demo.
- 🏆 **Verified GitHub Achievements**: Displays Quickdraw, Pull Shark, and YOLO badges.
- 📂 **32+ Public Repositories**: Filterable by AI & Agents, Infrastructure, Automation, and Client Work.
- 🖥️ **Backend & Container**: Standalone FastAPI + Docker backend in `backend/` deployed to Hugging Face Spaces.

## Repository Structure

```
portfolio/
├── index.html            # Complete website: UI, demos, animations, and scripts
├── PORTFOLIO_DOCS.md     # In-depth architectural & deployment guide
├── backend/              # Standalone Python backend (FastAPI + Qwen 2.5)
│   ├── server.py
│   ├── requirements.txt
│   └── Dockerfile
└── hf_space/             # Deployment payload for Hugging Face Spaces
```

## Running the Backend Locally

```bash
cd backend
pip install -r requirements.txt
python server.py
```

Runs on `http://localhost:7860` with `/api/chat`, `/api/status`, and `/api/projects`.

## License

MIT
