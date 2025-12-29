# Anjoman — Structured Multi-LLM Deliberation Tool

> **Anjoman** — Persian: انجمن • Turkish: encümen • Urdu: انجمن
> Meaning: "assembly", "gathering", "council"

A human-in-the-loop deliberation tool that orchestrates multiple LLMs into structured discussions — like convening a council of diverse minds to think through complex problems.

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

## Quick Start

### Local Development (Recommended for Development)

First time? See [Setup](#setup) below.

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
```

**Frontend:**
```bash
cd frontend
npm install
```

### API Keys

API keys are provided through the UI when creating a new session.

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


## License

MIT License

## Status

⚠️ Early development - APIs may change
