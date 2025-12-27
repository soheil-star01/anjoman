"""Tests for data models."""

import pytest
from datetime import datetime
from models import (
    ApiKeys, AgentConfig, AgentMessage, BudgetInfo, 
    Session, SessionStatus, Iteration, IterationSummary
)


class TestModels:
    """Test Pydantic models."""
    
    def test_api_keys_get_available_providers(self):
        """Test ApiKeys.get_available_providers method."""
        
        # With multiple keys
        keys = ApiKeys(
            openai_api_key="test-key",
            anthropic_api_key="test-key"
        )
        providers = keys.get_available_providers()
        assert "openai" in providers
        assert "anthropic" in providers
        assert len(providers) == 2
        
        # With single key
        keys_single = ApiKeys(openai_api_key="test-key")
        providers_single = keys_single.get_available_providers()
        assert providers_single == ["openai"]
        
        # With no keys
        keys_none = ApiKeys()
        providers_none = keys_none.get_available_providers()
        assert len(providers_none) == 0
    
    def test_budget_info_properties(self):
        """Test BudgetInfo calculated properties."""
        
        # Under budget
        budget = BudgetInfo(
            total_budget=10.0,
            used=2.0,
            remaining=8.0,
            warning_threshold=0.8
        )
        assert not budget.is_warning
        assert not budget.is_exceeded
        
        # Warning zone
        budget_warning = BudgetInfo(
            total_budget=10.0,
            used=8.5,
            remaining=1.5,
            warning_threshold=0.8
        )
        assert budget_warning.is_warning
        assert not budget_warning.is_exceeded
        
        # Exceeded
        budget_exceeded = BudgetInfo(
            total_budget=10.0,
            used=10.5,
            remaining=-0.5,
            warning_threshold=0.8
        )
        assert budget_exceeded.is_warning
        assert budget_exceeded.is_exceeded
    
    def test_agent_config_creation(self):
        """Test AgentConfig model creation."""
        
        agent = AgentConfig(
            id="Ray-1",
            role="Analyst",
            style="data-driven",
            model="gpt-4o",
            cost_used=0.0,
            tokens_in=100,
            tokens_out=50
        )
        
        assert agent.id == "Ray-1"
        assert agent.role == "Analyst"
        assert agent.model == "gpt-4o"
        assert agent.tokens_in == 100
        assert agent.tokens_out == 50
    
    def test_session_creation(self):
        """Test Session model creation."""
        
        agent = AgentConfig(
            id="Ray-1",
            role="Analyst",
            model="gpt-4o"
        )
        
        session = Session(
            session_id="test-001",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            issue="Test issue",
            agents=[agent],
            iterations=[],
            budget=BudgetInfo(
                total_budget=5.0,
                used=0.0,
                remaining=5.0,
                warning_threshold=0.8
            ),
            status=SessionStatus.ACTIVE
        )
        
        assert session.session_id == "test-001"
        assert len(session.agents) == 1
        assert session.status == SessionStatus.ACTIVE
    
    def test_iteration_with_optional_summary(self):
        """Test that Iteration allows optional summary."""
        
        message = AgentMessage(
            agent_id="Ray-1",
            agent_role="Analyst",
            content="Test content",
            timestamp=datetime.now(),
            tokens_in=100,
            tokens_out=50,
            cost=0.001
        )
        
        # Should work without summary
        iteration = Iteration(
            iteration_number=1,
            messages=[message],
            summary=None
        )
        
        assert iteration.iteration_number == 1
        assert len(iteration.messages) == 1
        assert iteration.summary is None

