"""Main FastAPI application for Anjoman backend."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from datetime import datetime
from typing import Optional
import json
import asyncio

from config import get_settings
from models import (
    CreateSessionRequest, ContinueSessionRequest, Session,
    SessionStatus, BudgetInfo, Iteration, SessionListItem, SessionProposal
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


@app.post("/sessions/propose", response_model=SessionProposal)
async def propose_session(request: CreateSessionRequest):
    """Get Dana's proposal for agent configuration."""
    return await Dana.propose_agents(
        request.issue, 
        request.budget, 
        request.num_agents,
        request.model_preference,
        request.api_keys
    )


@app.post("/sessions/create", response_model=Session)
async def create_session(request: CreateSessionRequest):
    """Create a new session with confirmed agent configuration."""
    
    # Generate session ID
    session_id = session_manager.generate_session_id()
    
    # Use the agents provided by user (after review)
    if not request.suggested_agents:
        raise HTTPException(status_code=400, detail="No agents provided. Use /sessions/propose first.")
    
    agents = request.suggested_agents
    
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
    """Run one iteration of the discussion (non-streaming)."""
    
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
            previous_messages=messages,
            api_keys=request.api_keys
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
    summary = await Dana.summarize_iteration(session, iteration, request.api_keys)
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


@app.post("/sessions/{session_id}/iterate/stream")
async def iterate_session_stream(session_id: str, request: ContinueSessionRequest):
    """Run one iteration with streaming updates (Server-Sent Events)."""
    
    async def event_generator():
        try:
            # Load session
            session = session_manager.load_session(session_id)
            if not session:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Session not found'})}\n\n"
                return
            
            # Check budget
            if session.budget.is_exceeded:
                yield f"data: {json.dumps({'type': 'error', 'message': 'Budget exceeded'})}\n\n"
                return
            
            # Send start event
            iteration_number = len(session.iterations) + 1
            yield f"data: {json.dumps({'type': 'start', 'iteration': iteration_number, 'total_agents': len(session.agents)})}\n\n"
            
            # Collect messages from each agent in sequence
            messages = []
            for idx, agent in enumerate(session.agents):
                # Check budget before each agent
                if session.budget.used >= session.budget.total_budget:
                    yield f"data: {json.dumps({'type': 'budget_exceeded'})}\n\n"
                    break
                
                # Send agent start event
                yield f"data: {json.dumps({'type': 'agent_start', 'agent_id': agent.id, 'agent_role': agent.role, 'index': idx})}\n\n"
                await asyncio.sleep(0.1)  # Small delay for UI
                
                # Get agent response
                message = await Ray.speak(
                    agent=agent,
                    session=session,
                    iteration_number=iteration_number,
                    previous_messages=messages,
                    api_keys=request.api_keys
                )
                messages.append(message)
                
                # Update budget
                session.budget.used += message.cost
                session.budget.remaining = session.budget.total_budget - session.budget.used
                
                # Send agent response event (use mode='json' to serialize dates)
                yield f"data: {json.dumps({'type': 'agent_response', 'message': message.model_dump(mode='json'), 'budget': session.budget.model_dump(mode='json')})}\n\n"
                await asyncio.sleep(0.1)
            
            # Create iteration object
            iteration = Iteration(
                iteration_number=iteration_number,
                messages=messages,
                summary=None,
                user_guidance=request.user_guidance
            )
            
            # Send summarizing event
            yield f"data: {json.dumps({'type': 'summarizing'})}\n\n"
            await asyncio.sleep(0.1)
            
            # Have Dana summarize
            summary = await Dana.summarize_iteration(session, iteration, request.api_keys)
            iteration.summary = summary
            
            # Add iteration to session
            session.iterations.append(iteration)
            session.updated_at = datetime.now()
            
            # Save session
            session_manager.save_session(session)
            
            # Send complete event with full session (use mode='json' to serialize dates)
            yield f"data: {json.dumps({'type': 'complete', 'session': session.model_dump(mode='json')})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


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
    """Get approximate pricing information for models.
    
    Note: Pricing is approximate and may change. 
    LiteLLM attempts to track actual costs automatically.
    Focus on token usage as the primary metric.
    """
    return {
        "pricing": [
            {
                "provider": "OpenAI",
                "model": "GPT-5.1",
                "model_id": "gpt-5.1",
                "input_per_1m": 20.00,
                "output_per_1m": 60.00,
                "note": "Latest model with customizable personalities (Nov 2025)"
            },
            {
                "provider": "OpenAI",
                "model": "GPT-5",
                "model_id": "gpt-5",
                "input_per_1m": 15.00,
                "output_per_1m": 45.00,
                "note": "Advanced reasoning capabilities (Aug 2025)"
            },
            {
                "provider": "OpenAI",
                "model": "GPT-4o",
                "model_id": "gpt-4o",
                "input_per_1m": 5.00,
                "output_per_1m": 15.00,
                "note": "Optimized multimodal model"
            },
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
                "model": "Claude Opus 4.5",
                "model_id": "claude-opus-4.5",
                "input_per_1m": 18.00,
                "output_per_1m": 90.00,
                "note": "Best for complex workflows and long-context (Nov 2025)"
            },
            {
                "provider": "Anthropic",
                "model": "Claude Sonnet 4.5",
                "model_id": "claude-sonnet-4.5",
                "input_per_1m": 4.00,
                "output_per_1m": 20.00,
                "note": "Superior coding, 1M token context (Sept 2025)"
            },
            {
                "provider": "Anthropic",
                "model": "Claude 3.5 Sonnet",
                "model_id": "claude-3-5-sonnet-20241022",
                "input_per_1m": 3.00,
                "output_per_1m": 15.00
            },
            {
                "provider": "Anthropic",
                "model": "Claude 3 Opus",
                "model_id": "claude-3-opus-20240229",
                "input_per_1m": 15.00,
                "output_per_1m": 75.00
            },
            {
                "provider": "Mistral",
                "model": "Mistral Large",
                "model_id": "mistral-large-latest",
                "input_per_1m": 2.00,
                "output_per_1m": 6.00
            },
            {
                "provider": "Mistral",
                "model": "Mistral Medium",
                "model_id": "mistral-medium-latest",
                "input_per_1m": 2.70,
                "output_per_1m": 8.10
            },
            {
                "provider": "Mistral",
                "model": "Mistral Small",
                "model_id": "mistral-small-latest",
                "input_per_1m": 1.00,
                "output_per_1m": 3.00
            }
        ],
        "note": "Prices are approximate and may vary. Actual costs tracked via LiteLLM. LiteLLM supports 100+ models."
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

