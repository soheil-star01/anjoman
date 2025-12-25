# Anjoman Architecture

Detailed technical architecture and design decisions.

## System Overview

Anjoman is a full-stack application with clear separation between orchestration logic (backend) and user interface (frontend).

```
┌─────────────────────────────────────────────┐
│           Frontend (Next.js)                │
│  ┌────────────────────────────────────┐    │
│  │  UI Components                      │    │
│  │  - NewSessionForm                   │    │
│  │  - SessionView                      │    │
│  │  - IterationView                    │    │
│  │  - AgentCard                        │    │
│  │  - BudgetDisplay                    │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │ HTTP/REST
               │
┌──────────────▼──────────────────────────────┐
│         Backend (FastAPI)                   │
│  ┌────────────────────────────────────┐    │
│  │  API Endpoints                      │    │
│  │  - /sessions/create                 │    │
│  │  - /sessions/{id}/iterate           │    │
│  │  - /sessions/{id}                   │    │
│  └────────────────────────────────────┘    │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Orchestrator (orchestrator.py)     │    │
│  │  - Dana (moderator/summarizer)      │    │
│  │  - Ray (agent logic)                │    │
│  └────────────────────────────────────┘    │
│                                             │
│  ┌────────────────────────────────────┐    │
│  │  Session Manager                    │    │
│  │  - File-based JSON persistence      │    │
│  └────────────────────────────────────┘    │
└──────────────┬──────────────────────────────┘
               │
               │ LiteLLM
               │
┌──────────────▼──────────────────────────────┐
│       LLM Providers                         │
│  - OpenAI (GPT-4, GPT-3.5)                  │
│  - Anthropic (Claude)                       │
│  - Mistral                                  │
│  - Others via LiteLLM                       │
└─────────────────────────────────────────────┘
```

## Backend Architecture

### Core Components

#### 1. FastAPI Application (`main.py`)

Entry point for all API requests. Handles:
- Session creation and management
- Iteration orchestration
- Budget tracking
- CORS configuration

Key endpoints:
- `POST /sessions/create` - Initialize new session
- `POST /sessions/{id}/iterate` - Run one iteration
- `GET /sessions` - List all sessions
- `GET /sessions/{id}` - Get session details

#### 2. Orchestrator (`orchestrator.py`)

Contains the core deliberation logic:

**Dana (The Moderator)**
- Proposes agent configurations based on issue complexity
- Summarizes each iteration
- Identifies disagreements
- Suggests next directions
- Uses JSON mode for structured outputs

**Ray (The Agent)**
- Each Ray has a role, model, and optional style
- Agents speak sequentially in each iteration
- Context includes: issue, previous messages, iteration history
- Token usage and cost tracked per message

#### 3. Session Manager (`session_manager.py`)

File-based persistence layer:
- Saves sessions as JSON files in `data/sessions/`
- One file per session
- Explicit save after each iteration
- Supports loading, listing, and deleting sessions

Benefits:
- No database setup required
- Human-readable session format
- Easy to debug and export
- Version control friendly

#### 4. Models (`models.py`)

Pydantic models for type safety and validation:
- `Session` - Complete session state
- `AgentConfig` - Agent configuration and stats
- `Iteration` - One round of discussion
- `AgentMessage` - Individual agent response
- `IterationSummary` - Dana's summary
- `BudgetInfo` - Budget tracking

#### 5. Configuration (`config.py`)

Environment-based configuration using Pydantic Settings:
- API keys for LLM providers
- Session storage directory
- CORS origins
- Default budget

### LiteLLM Integration

LiteLLM provides a unified interface to multiple LLM providers:

```python
response = await litellm.acompletion(
    model="gpt-4-turbo",  # or claude-3-sonnet, mistral-large, etc.
    messages=[...],
    temperature=0.7
)
```

Benefits:
- Single API for all providers
- Automatic retry logic
- Cost tracking built-in
- Easy to add new providers

### Cost Tracking

Multi-level cost tracking:
1. **Per-message**: Each agent message tracks its own cost
2. **Per-agent**: Accumulated cost per agent across iterations
3. **Per-iteration**: Total cost for one round
4. **Per-session**: Global budget enforcement

Budget checks:
- Before each iteration
- Before each agent speaks
- Warning at 80% threshold
- Stop at 100%

## Frontend Architecture

### Technology Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Utility-first styling
- **Axios** - HTTP client
- **react-markdown** - Markdown rendering
- **lucide-react** - Icon library
- **date-fns** - Date formatting

### Component Structure

```
app/
├── layout.tsx          # Root layout
├── page.tsx            # Main page (view router)
└── globals.css         # Global styles + markdown

components/
├── NewSessionForm.tsx  # Create new session
├── SessionView.tsx     # Main session interface
├── IterationView.tsx   # Single iteration display
├── AgentCard.tsx       # Agent info card
├── BudgetDisplay.tsx   # Budget tracker
└── SessionList.tsx     # Session history

lib/
└── api.ts              # API client

types/
└── index.ts            # TypeScript types
```

### State Management

Simple, prop-based state management:
- Main app state in `app/page.tsx`
- Props passed down to components
- State updates via callbacks
- No global state library needed (for MVP)

### Key Features

**1. Session Creation**
- User inputs issue and budget
- Dana proposes agents automatically
- Backend creates session and returns full state

**2. Iteration Flow**
- User provides optional guidance
- Click "Next Iteration" to proceed
- Backend runs all agents sequentially
- Dana summarizes
- UI updates with new state

**3. Budget Monitoring**
- Real-time budget display
- Visual progress bar
- Warning states (yellow/red)
- Per-agent cost breakdown

**4. Session History**
- List all past sessions
- Quick load and resume
- Delete unwanted sessions
- View stats (cost, iterations, status)

## Data Flow

### Creating a Session

```
User Input (issue, budget)
  ↓
Frontend: api.createSession()
  ↓
Backend: POST /sessions/create
  ↓
Dana.propose_agents()
  ↓
Create Session object
  ↓
SessionManager.save_session()
  ↓
Return Session to frontend
  ↓
Display agents and wait for user
```

### Running an Iteration

```
User clicks "Next Iteration"
  ↓
Frontend: api.iterateSession()
  ↓
Backend: POST /sessions/{id}/iterate
  ↓
Load session from file
  ↓
Check budget
  ↓
For each agent:
  - Build prompt with context
  - Call LLM via LiteLLM
  - Track cost and tokens
  - Add message to iteration
  ↓
Dana.summarize_iteration()
  ↓
Add iteration to session
  ↓
SessionManager.save_session()
  ↓
Return updated Session
  ↓
Frontend updates UI
```

## Design Decisions

### Why File-Based Storage?

**Pros:**
- No database setup or maintenance
- Human-readable (JSON)
- Easy to debug and inspect
- Version control friendly
- Export/import trivial
- OSS-friendly

**Cons:**
- Not suitable for high concurrency
- No complex queries
- Manual file management

**Decision**: For MVP and small-scale use, benefits outweigh drawbacks.

### Why Sequential Agents?

**Pros:**
- Simple to implement and reason about
- Agents can build on previous responses
- Clear turn order
- Easier to debug

**Cons:**
- Not parallel (slower)
- Later agents have advantage

**Decision**: Clarity and simplicity for MVP. Can add parallel modes later.

### Why LiteLLM?

**Pros:**
- Single API for all providers
- Built-in cost tracking
- Retry logic
- Active maintenance
- Easy provider switching

**Cons:**
- Extra dependency
- Abstraction layer

**Decision**: The unified interface is worth the dependency.

### Why No LangGraph State Persistence?

**Decision**: LangGraph is used for orchestration logic, NOT persistence. 

**Rationale**:
- Session state is explicitly saved as JSON
- LangGraph's in-memory state is short-lived
- Simpler to reason about
- Avoids mixing concerns

## Future Architecture Considerations

### Potential Enhancements

1. **Branching Discussions**
   - Fork sessions at any iteration
   - Explore multiple paths
   - Compare outcomes

2. **Parallel Agents**
   - All agents respond simultaneously
   - Dana synthesizes after

3. **Tool Calling**
   - Agents can use external tools
   - Web search, calculators, etc.

4. **Streaming Responses**
   - Real-time agent output
   - Better UX for long responses

5. **Database Backend**
   - Optional PostgreSQL/SQLite
   - Better querying and analytics
   - Keep file export

6. **Custom Agent Templates**
   - Save and reuse agent configs
   - Share templates

## Security Considerations

### Current (MVP)

- API keys in `.env` (server-side only)
- CORS configured for localhost
- No authentication (local use)
- Session files readable by anyone with file access

### Production Considerations

- User authentication
- Per-user API keys or quota
- Rate limiting
- Input validation and sanitization
- Encrypted session storage
- Audit logging

## Performance

### Current Bottlenecks

1. **Sequential API calls**: Each agent waits for previous
2. **LLM latency**: 2-10 seconds per agent
3. **File I/O**: Minimal impact for MVP scale

### Optimization Opportunities

1. Parallel agent execution
2. Response streaming
3. Caching for summaries
4. Database for large session counts

## Testing Strategy

### Backend

- Unit tests for models and validation
- Integration tests for API endpoints
- Mock LLM calls for reproducibility

### Frontend

- Component tests with React Testing Library
- E2E tests with Playwright
- Visual regression tests

## Deployment

### Development

- Backend: `uvicorn main:app --reload`
- Frontend: `npm run dev`
- Both run locally

### Production Options

**Backend:**
- Docker container
- Railway, Fly.io, or similar
- Cloud Run (GCP)

**Frontend:**
- Vercel (native Next.js)
- Netlify
- Static export + CDN

**Full Stack:**
- Docker Compose
- Kubernetes
- Single VPS

## Monitoring and Observability

### Metrics to Track

- API response times
- LLM call costs
- Session creation rate
- Iteration completion rate
- Error rates
- Token usage per model

### Logging

- Structured JSON logs
- LLM call traces
- User actions
- Error stack traces

## Conclusion

Anjoman's architecture prioritizes simplicity, clarity, and extensibility. The file-based approach and clear separation of concerns make it easy to understand, debug, and extend.

As the project grows, the architecture can evolve to support more sophisticated features while maintaining its core philosophy of transparency and structure.

