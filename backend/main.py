"""Main FastAPI application for Anjoman backend."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import Optional

from config import get_settings
from models import (
    CreateSessionRequest, ContinueSessionRequest, Session,
    SessionStatus, BudgetInfo, Iteration, SessionListItem
)
from session_manager import SessionManager
from orchestrator import Dana, Ray

# Initialize FastAPI app
app = FastAPI(
    title="Anjoman API",
    description="Structured Multi-LLM Deliberation Tool",
    version="0.1.0"
)

# Configure CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize session manager
session_manager = SessionManager()


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Anjoman API",
        "status": "running",
        "version": "0.1.0"
    }


@app.post("/sessions/create", response_model=Session)
async def create_session(request: CreateSessionRequest):
    """Create a new session and get Dana's agent proposal."""
    
    # Generate session ID
    session_id = session_manager.generate_session_id()
    
    # Get Dana's proposal for agents
    if request.suggested_agents:
        # User provided agents
        agents = request.suggested_agents
    else:
        # Let Dana propose
        proposal = await Dana.propose_agents(request.issue, request.budget)
        agents = proposal.proposed_agents
    
    # Create session
    session = Session(
        session_id=session_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
        issue=request.issue,
        agents=agents,
        iterations=[],
        budget=BudgetInfo(
            total_budget=request.budget,
            used=0.0,
            remaining=request.budget
        ),
        status=SessionStatus.ACTIVE
    )
    
    # Save session
    session_manager.save_session(session)
    
    return session


@app.post("/sessions/{session_id}/iterate", response_model=Session)
async def iterate_session(session_id: str, request: ContinueSessionRequest):
    """Run one iteration of the discussion."""
    
    # Load session
    session = session_manager.load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check budget
    if session.budget.is_exceeded:
        session.status = SessionStatus.PAUSED
        session_manager.save_session(session)
        raise HTTPException(
            status_code=400,
            detail=f"Budget exceeded: ${session.budget.used:.2f} / ${session.budget.total_budget:.2f}"
        )
    
    # Determine iteration number
    iteration_number = len(session.iterations) + 1
    
    # Collect messages from each agent in sequence
    messages = []
    for agent in session.agents:
        # Check budget before each agent
        if session.budget.used >= session.budget.total_budget:
            break
        
        message = await Ray.speak(
            agent=agent,
            session=session,
            iteration_number=iteration_number,
            previous_messages=messages
        )
        messages.append(message)
        
        # Update budget
        session.budget.used += message.cost
        session.budget.remaining = session.budget.total_budget - session.budget.used
    
    # Create iteration object
    iteration = Iteration(
        iteration_number=iteration_number,
        messages=messages,
        summary=None,  # Will be filled by Dana
        user_guidance=request.user_guidance
    )
    
    # Have Dana summarize
    summary = await Dana.summarize_iteration(session, iteration)
    iteration.summary = summary
    
    # Add iteration to session
    session.iterations.append(iteration)
    session.updated_at = datetime.now()
    
    # Check if budget warning
    if session.budget.is_warning and not session.budget.is_exceeded:
        print(f"Budget warning: {session.budget.used:.2f} / {session.budget.total_budget:.2f}")
    
    # Save session
    session_manager.save_session(session)
    
    return session


@app.get("/sessions", response_model=list[SessionListItem])
async def list_sessions():
    """List all sessions."""
    return session_manager.list_sessions()


@app.get("/sessions/{session_id}", response_model=Session)
async def get_session(session_id: str):
    """Get a specific session."""
    session = session_manager.load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.delete("/sessions/{session_id}")
async def delete_session(session_id: str):
    """Delete a session."""
    success = session_manager.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"status": "deleted", "session_id": session_id}


@app.post("/sessions/{session_id}/complete")
async def complete_session(session_id: str):
    """Mark a session as completed."""
    session = session_manager.load_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.status = SessionStatus.COMPLETED
    session_manager.save_session(session)
    
    return {"status": "completed", "session_id": session_id}


@app.get("/models/pricing")
async def get_model_pricing():
    """Get approximate pricing information for models."""
    return {
        "pricing": [
            {
                "provider": "OpenAI",
                "model": "GPT-4 Turbo",
                "model_id": "gpt-4-turbo",
                "input_per_1m": 10.00,
                "output_per_1m": 30.00
            },
            {
                "provider": "OpenAI",
                "model": "GPT-3.5 Turbo",
                "model_id": "gpt-3.5-turbo",
                "input_per_1m": 0.50,
                "output_per_1m": 1.50
            },
            {
                "provider": "Anthropic",
                "model": "Claude 3 Opus",
                "model_id": "claude-3-opus",
                "input_per_1m": 15.00,
                "output_per_1m": 75.00
            },
            {
                "provider": "Anthropic",
                "model": "Claude 3 Sonnet",
                "model_id": "claude-3-sonnet",
                "input_per_1m": 3.00,
                "output_per_1m": 15.00
            },
            {
                "provider": "Anthropic",
                "model": "Claude 3 Haiku",
                "model_id": "claude-3-haiku",
                "input_per_1m": 0.25,
                "output_per_1m": 1.25
            },
            {
                "provider": "Mistral",
                "model": "Mistral Large",
                "model_id": "mistral-large",
                "input_per_1m": 2.00,
                "output_per_1m": 6.00
            },
            {
                "provider": "Mistral",
                "model": "Mistral Medium",
                "model_id": "mistral-medium",
                "input_per_1m": 2.70,
                "output_per_1m": 8.10
            }
        ],
        "note": "Prices are approximate and may vary. Actual costs tracked via LiteLLM."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

