# Anjoman — Structured Multi-LLM Deliberation Tool

Human-in-the-loop deliberation tool that orchestrates multiple LLMs into structured discussions.

## Quick Start

### Local Development (Recommended for Development)

**Backend (Terminal 1):**
```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

Open http://localhost:3000

### Docker (Recommended for Deployment)

```bash
docker-compose up -d
```

## Setup

### First Time Setup

**Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Add your API keys to .env
cp .env.example .env
# Edit .env and add: OPENAI_API_KEY=sk-...
```

**Frontend:**
```bash
cd frontend
npm install
```

### API Keys

Add at least one API key to `backend/.env`:
- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/
- **Mistral**: https://console.mistral.ai/

## What is Anjoman?

Anjoman is **not** a chatbot or autonomous agent system. It's a structured thinking tool.

**Core concept:**
- Multiple LLM agents (Rays) with distinct roles and models
- Dana (orchestrator) moderates and summarizes
- You guide the discussion at each iteration
- Sessions saved as JSON files

**Philosophy:**
- Clarity over speed
- Structure over creativity
- Transparency over confidence

## Features

- ✅ Multi-agent orchestration (GPT-4, Claude, Mistral, etc.)
- ✅ Turn-based sequential discussion
- ✅ Real-time cost tracking and budget limits
- ✅ Session persistence (JSON files)
- ✅ Resume and review past sessions
- ✅ No database required

## Tech Stack

- **Backend**: Python, FastAPI, LiteLLM
- **Frontend**: Next.js, React, TypeScript, Tailwind
- **Storage**: File-based JSON

## Project Structure

```
anjoman/
├── backend/           # Python FastAPI backend
├── frontend/          # Next.js frontend
├── data/sessions/     # Session storage
└── README.md
```

## Development

Hot reload is enabled for both services. Just edit and save.

**Useful commands:**
```bash
# Backend with different port
uvicorn main:app --reload --port 8001

# Frontend with different port
npm run dev -- -p 3001

# Build frontend for production
npm run build

# Run tests
cd backend
pytest

# Run tests with coverage
pytest --cov=. --cov-report=html
```

## Docker

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# View logs
docker-compose logs -f

# Development mode (hot reload)
docker-compose -f docker-compose.dev.yml up
```

## Make Commands

```bash
make up       # Start with Docker
make dev      # Dev mode with hot reload
make down     # Stop services
make logs     # View logs
make help     # See all commands
```

## License

MIT License

## Status

⚠️ Early development - APIs may change
