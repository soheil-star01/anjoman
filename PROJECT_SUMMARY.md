# Anjoman Project Summary

## What Was Built

A complete, working implementation of the Anjoman structured multi-LLM deliberation tool, including:

### ✅ Backend (Python/FastAPI)
- **FastAPI REST API** with endpoints for session management and iteration
- **Dana orchestrator** that proposes agents and summarizes discussions
- **Ray agent system** with role-based LLM agents
- **File-based session persistence** using JSON
- **Cost tracking and budget enforcement** at multiple levels
- **LiteLLM integration** for unified multi-provider LLM access
- **Pydantic models** for type safety and validation

### ✅ Frontend (Next.js/React/TypeScript)
- **Modern UI** with Tailwind CSS
- **Session creation form** with budget configuration
- **Real-time discussion view** with agent cards
- **Iteration display** with markdown support
- **Budget monitoring** with visual progress bars
- **Session history** with load/resume capability
- **Cost breakdown** per agent and per iteration

### ✅ Documentation
- **README.md** - Project overview and philosophy
- **SETUP.md** - Step-by-step setup instructions
- **CONTRIBUTING.md** - Contribution guidelines
- **ARCHITECTURE.md** - Detailed technical architecture
- **LICENSE** - MIT License
- Shell scripts for easy startup

## Project Structure

```
anjoman/
├── backend/                    # Python FastAPI backend
│   ├── main.py                # API endpoints
│   ├── orchestrator.py        # Dana & Ray logic
│   ├── session_manager.py     # File persistence
│   ├── models.py              # Pydantic models
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
├── frontend/                  # Next.js React frontend
│   ├── app/                   # Next.js pages
│   │   ├── page.tsx          # Main app
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css       # Styles
│   ├── components/            # React components
│   │   ├── NewSessionForm.tsx
│   │   ├── SessionView.tsx
│   │   ├── IterationView.tsx
│   │   ├── AgentCard.tsx
│   │   ├── BudgetDisplay.tsx
│   │   └── SessionList.tsx
│   ├── lib/
│   │   └── api.ts            # API client
│   ├── types/
│   │   └── index.ts          # TypeScript types
│   ├── package.json          # Node dependencies
│   ├── tsconfig.json         # TypeScript config
│   └── tailwind.config.ts    # Tailwind config
│
├── data/
│   └── sessions/             # Session JSON files stored here
│
├── README.md                 # Main documentation
├── SETUP.md                  # Setup guide
├── CONTRIBUTING.md           # Contribution guide
├── ARCHITECTURE.md           # Technical architecture
├── LICENSE                   # MIT License
├── .gitignore               # Git ignore rules
├── start-backend.sh         # Backend startup script
└── start-frontend.sh        # Frontend startup script
```

## Key Features Implemented

### 1. Multi-Agent Orchestration
- Dana proposes 3-5 agents based on issue complexity
- Each Ray has a unique role, model, and optional style
- Sequential turn-based discussion
- Full conversation context for each agent

### 2. Session Management
- Create sessions with custom budgets
- Save/load sessions as JSON files
- Session history with quick resume
- Complete or delete sessions

### 3. Cost Tracking
- Real-time per-agent cost tracking
- Per-iteration cost summaries
- Global budget enforcement
- Visual budget indicators (green/yellow/red)
- Warning at 80% budget usage

### 4. Iteration Flow
- User provides optional guidance between iterations
- All agents respond in sequence
- Dana summarizes each iteration
- Key disagreements highlighted
- Suggested direction for next iteration

### 5. Modern UI
- Clean, professional interface
- Markdown rendering for agent responses
- Real-time budget visualization
- Session history with search/filter
- Responsive design

## Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI** - Modern web framework
- **LiteLLM** - Unified LLM API (OpenAI, Anthropic, Mistral, etc.)
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **react-markdown** - Markdown rendering
- **lucide-react** - Icons
- **date-fns** - Date formatting

## How to Use

### Quick Start with Docker (Recommended) 🐳

1. **Setup Environment**
   ```bash
   ./setup-env.sh
   # Or manually: cp .env.example .env and edit
   ```

2. **Start Everything**
   ```bash
   docker-compose up -d
   ```

3. **Use Anjoman**
   - Open http://localhost:3000
   - Create a new session
   - Watch the agents deliberate
   - Guide the discussion
   - Review summaries

4. **Stop Services**
   ```bash
   docker-compose down
   ```

### Alternative: Manual Setup

1. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   ```

2. **Setup Frontend**
   ```bash
   cd frontend
   npm install
   ```

3. **Start Both**
   ```bash
   # Terminal 1 - Backend
   ./start-backend.sh
   
   # Terminal 2 - Frontend  
   ./start-frontend.sh
   ```

### Example Session

**Issue**: "Should we migrate our monolith to microservices?"

**Dana proposes**:
- Ray-1 (Analyst) using GPT-4 Turbo
- Ray-2 (Critic) using Claude 3 Sonnet
- Ray-3 (Strategist) using GPT-3.5 Turbo
- Ray-4 (DevOps Expert) using Mistral Large

**Iteration 1**: Each agent provides their perspective
**Dana summarizes**: Key trade-offs, disagreements, suggested focus
**User guides**: "Focus on timeline and team impact"
**Iteration 2**: Agents respond with refined analysis
**Continue until satisfied**

## What Makes This Special

### 1. Human-in-the-Loop
Not autonomous - you control the flow and provide guidance.

### 2. Structured Process
Clear roles, turn order, and summaries make reasoning transparent.

### 3. Multi-Model Support
Mix and match different LLMs for diverse perspectives.

### 4. Cost Conscious
Built-in budget tracking prevents surprise bills.

### 5. Simple & Transparent
- No database required
- Sessions are readable JSON files
- Clear architecture
- Easy to understand and modify

### 6. Open Source First
- MIT licensed
- Well documented
- Contribution friendly
- No vendor lock-in

## Design Philosophy

**Clarity over speed**: The code is written to be readable and maintainable.

**Structure over creativity**: Follow established patterns and conventions.

**Transparency over confidence**: Make the reasoning process visible.

**Local-first**: Works entirely on your machine with your API keys.

## Limitations & Future Work

### Current Limitations
- Sequential agents only (no parallel)
- No branching discussions
- No tool calling for agents
- Local only (no collaboration)
- Basic cost estimates

### Planned Enhancements
- [ ] Parallel agent execution
- [ ] Discussion branching
- [ ] Tool calling (web search, calculators)
- [ ] Real-time streaming
- [ ] Agent templates
- [ ] Export to various formats
- [ ] Analytics dashboard
- [ ] User accounts (optional)

## Testing

Not yet implemented but recommended:
- Backend: pytest with mocked LLM calls
- Frontend: React Testing Library + Playwright
- Integration: End-to-end tests

## Deployment

### Development
- **Docker**: `docker-compose up -d` (recommended)
- **Manual**: Run backend and frontend locally

### Production Options
- **Docker Compose**: Ready for single-server deployment
- **Separate Services**: Vercel (frontend) + Railway/Fly.io (backend)
- **Container Orchestration**: Kubernetes, Docker Swarm
- **Cloud Platforms**: AWS ECS, Google Cloud Run, Azure Container Instances

See [DOCKER.md](DOCKER.md) for detailed deployment instructions.

## Getting Help

1. Check [SETUP.md](SETUP.md) for setup issues
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
3. See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
4. Open GitHub issues for bugs or questions

## License

MIT License - use it, modify it, share it!

## Final Notes

Anjoman is ready to use! You have a fully functional structured multi-LLM deliberation tool that:
- Works with multiple LLM providers
- Tracks costs transparently
- Saves sessions persistently
- Provides a clean UI
- Is easy to extend

Start with a simple issue and a small budget ($1-2) to get familiar with the flow. Then tackle more complex problems with larger budgets and more iterations.

**Happy deliberating! 🎯**

