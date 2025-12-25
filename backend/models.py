"""Data models for Anjoman."""

from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from enum import Enum


class SessionStatus(str, Enum):
    """Session status enum."""
    ACTIVE = "active"
    COMPLETED = "completed"
    PAUSED = "paused"
    ERROR = "error"


class AgentConfig(BaseModel):
    """Configuration for a single Ray agent."""
    id: str = Field(..., description="Agent ID (e.g., ray-1)")
    role: str = Field(..., description="Agent role (e.g., Analyst, Critic)")
    style: Optional[str] = Field(None, description="Optional behavioral style")
    model: str = Field(..., description="LLM model identifier")
    cost_used: float = Field(0.0, description="Accumulated cost in USD")
    tokens_in: int = Field(0, description="Total input tokens")
    tokens_out: int = Field(0, description="Total output tokens")


class AgentMessage(BaseModel):
    """A message from an agent."""
    agent_id: str
    agent_role: str
    content: str
    timestamp: datetime
    tokens_in: int = 0
    tokens_out: int = 0
    cost: float = 0.0


class IterationSummary(BaseModel):
    """Summary after each iteration."""
    iteration_number: int
    summary: str
    key_disagreements: Optional[list[str]] = None
    suggested_direction: str
    total_cost: float
    timestamp: datetime


class Iteration(BaseModel):
    """A complete iteration of the discussion."""
    iteration_number: int
    messages: list[AgentMessage]
    summary: IterationSummary
    user_guidance: Optional[str] = None


class BudgetInfo(BaseModel):
    """Budget tracking information."""
    total_budget: float
    used: float
    remaining: float
    warning_threshold: float = 0.8  # Warn at 80%
    
    @property
    def is_warning(self) -> bool:
        """Check if budget is in warning zone."""
        return self.used >= (self.total_budget * self.warning_threshold)
    
    @property
    def is_exceeded(self) -> bool:
        """Check if budget is exceeded."""
        return self.used >= self.total_budget


class Session(BaseModel):
    """A complete Anjoman session."""
    session_id: str
    created_at: datetime
    updated_at: datetime
    issue: str
    agents: list[AgentConfig]
    iterations: list[Iteration] = []
    budget: BudgetInfo
    status: SessionStatus = SessionStatus.ACTIVE


class CreateSessionRequest(BaseModel):
    """Request to create a new session."""
    issue: str
    budget: float = 5.0
    suggested_agents: Optional[list[AgentConfig]] = None


class SessionProposal(BaseModel):
    """Dana's proposal for agent setup."""
    proposed_agents: list[AgentConfig]
    rationale: str


class ContinueSessionRequest(BaseModel):
    """Request to continue a session with user guidance."""
    session_id: str
    user_guidance: Optional[str] = None
    accept_suggestion: bool = True


class SessionListItem(BaseModel):
    """Lightweight session item for listing."""
    session_id: str
    created_at: datetime
    issue: str
    status: SessionStatus
    total_cost: float
    iteration_count: int

