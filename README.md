# Anjoman — Structured Multi-LLM Deliberation Tool

Anjoman is an open-source, human-in-the-loop deliberation tool that orchestrates multiple Large Language Models (LLMs) into a structured discussion, similar to an expert council.

## Overview

**Anjoman is NOT:**
- A chatbot replacement
- An autonomous agent system

**Anjoman IS:**
- A thinking aid for complex problems
- A structured deliberation framework
- A transparent, human-guided process

## Core Concept

- Multiple LLM agents (Rays) participate in moderated discussions
- Each agent has a clear role, model, and turn order
- After each iteration, the system produces summaries and suggestions
- **You** review, adjust, and decide how to continue

## Naming Convention

- **System**: Anjoman (assembly/council)
- **Orchestrator**: Dana (moderator & summarizer)
- **Agents**: Ray-1, Ray-2, Ray-3... (differentiated by role and model)

## Architecture

### Backend
- **Python** with FastAPI
- **LangGraph** for deterministic agent orchestration
- **LiteLLM** for unified LLM provider interface
- File-based session storage (JSON)

### Frontend
- **Next.js** (React)
- **Tailwind CSS**
- Markdown-first rendering
- Real-time cost tracking

## Quick Start

### Option 1: Docker (Recommended) 🐳

**Prerequisites**: Docker and Docker Compose installed

```bash
# 1. Setup environment (interactive)
./setup-env.sh

# 2. Start everything
docker-compose up -d
# OR: make up

# 3. Open http://localhost:3000
```

See [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) or [DOCKER.md](DOCKER.md) for detailed Docker instructions.

### Option 2: Manual Setup

**Prerequisites**: Python 3.10+ and Node.js 18+

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your API keys
uvicorn main:app --reload --port 8000

# Frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

Visit `http://localhost:3000` to use Anjoman.

See [SETUP.md](SETUP.md) for detailed manual setup instructions.

## Features

### ✅ MVP (Current)
- Multi-agent orchestration with defined roles
- Turn-based sequential discussion
- Session persistence (JSON files)
- Per-agent cost tracking
- Global budget enforcement
- Summary generation after each iteration
- Session resume capability

### 🔮 Future
- Branching discussions
- Tool calling for agents
- Real-time collaboration
- Custom agent personalities
- Export to different formats

## Session Storage

Sessions are stored as simple JSON files in `data/sessions/`:

```
data/
  sessions/
    anj-2025-001.json
    anj-2025-002.json
```

Each session contains:
- Agent configurations
- Full discussion history
- Cost tracking
- Iteration summaries

## Cost Tracking

Anjoman tracks costs in real-time:
- Per-agent token usage and cost
- Global session budget
- Warning before budget limits
- Transparent pricing via LiteLLM

## Philosophy

Anjoman favors:
- **Clarity** over speed
- **Structure** over creativity
- **Transparency** over confidence

It's a thinking aid, not an answer generator.

## Contributing

This is an early-stage open-source project. Contributions, feedback, and ideas are welcome!

## License

MIT License - see LICENSE file for details

## Project Status

⚠️ **Early Development Phase** - APIs and features may change

- Local-first
- Open-source first
- No monetization plans
- Community-driven development

