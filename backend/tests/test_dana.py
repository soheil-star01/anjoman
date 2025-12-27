"""Tests for Dana orchestrator functionality."""

import pytest
from unittest.mock import AsyncMock, patch
from orchestrator import Dana
from models import ApiKeys


class TestDana:
    """Test Dana orchestrator functions."""
    
    @pytest.mark.asyncio
    async def test_dana_proposes_agents(self, sample_api_keys, mock_litellm_response):
        """Test that Dana can propose agents for a given issue."""
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_response)):
            proposal = await Dana.propose_agents(
                issue="Should we migrate to microservices?",
                budget=5.0,
                num_agents=3,
                model_preference="balanced",
                api_keys=sample_api_keys
            )
            
            # Verify proposal structure
            assert proposal is not None
            assert len(proposal.proposed_agents) > 0
            assert proposal.rationale is not None
            assert len(proposal.available_models) > 0
            
            # Verify agent properties
            for agent in proposal.proposed_agents:
                assert agent.id.startswith("Ray-")
                assert agent.role is not None
                assert agent.model is not None
    
    @pytest.mark.asyncio
    async def test_dana_respects_agent_count(self, sample_api_keys, mock_litellm_response):
        """Test that Dana respects the requested number of agents."""
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_response)):
            # Request specific number
            proposal = await Dana.propose_agents(
                issue="Test issue",
                budget=5.0,
                num_agents=3,
                model_preference="balanced",
                api_keys=sample_api_keys
            )
            
            # Should limit to requested number
            assert len(proposal.proposed_agents) <= 3
    
    @pytest.mark.asyncio
    async def test_dana_handles_no_agent_count(self, sample_api_keys, mock_litellm_response):
        """Test that Dana decides agent count when not specified."""
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_response)):
            proposal = await Dana.propose_agents(
                issue="Test issue",
                budget=5.0,
                num_agents=None,  # Let Dana decide
                model_preference="balanced",
                api_keys=sample_api_keys
            )
            
            # Should propose some agents (Dana's decision)
            assert len(proposal.proposed_agents) > 0
    
    def test_dana_filters_models_by_api_keys(self, sample_api_keys):
        """Test that Dana only returns models for available API keys."""
        
        available_models = Dana._get_available_models(sample_api_keys)
        
        # Should have models
        assert len(available_models) > 0
        
        # Should only include OpenAI and Anthropic (from sample_api_keys)
        providers = set(model.provider for model in available_models)
        assert "openai" in providers
        assert "anthropic" in providers
    
    def test_dana_model_tiers(self, sample_api_keys):
        """Test that Dana organizes models by tiers correctly."""
        
        model_tiers = Dana._get_model_tiers(sample_api_keys)
        
        # Should have tiers for available providers
        assert "openai" in model_tiers
        assert "anthropic" in model_tiers
        
        # Each provider should have budget/balanced/performance tiers
        for provider, tiers in model_tiers.items():
            assert "budget" in tiers
            assert "balanced" in tiers
            assert "performance" in tiers
            assert len(tiers["budget"]) > 0
            assert len(tiers["balanced"]) > 0
            assert len(tiers["performance"]) > 0
    
    @pytest.mark.asyncio
    async def test_dana_summarize_iteration(self, sample_session, mock_litellm_response):
        """Test that Dana can summarize an iteration."""
        
        from models import Iteration, AgentMessage
        from datetime import datetime
        
        # Create a mock iteration
        iteration = Iteration(
            iteration_number=1,
            messages=[
                AgentMessage(
                    agent_id="Ray-1",
                    agent_role="Analyst",
                    content="Test analysis content",
                    timestamp=datetime.now(),
                    tokens_in=100,
                    tokens_out=50,
                    cost=0.001
                )
            ],
            summary=None
        )
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_response)):
            summary = await Dana.summarize_iteration(sample_session, iteration)
            
            # Verify summary structure
            assert summary is not None
            assert summary.iteration_number == 1
            assert summary.summary is not None
            assert summary.suggested_direction is not None
            assert summary.total_cost >= 0

