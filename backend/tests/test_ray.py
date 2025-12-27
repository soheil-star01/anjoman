"""Tests for Ray agent functionality."""

import pytest
from unittest.mock import AsyncMock, patch
from orchestrator import Ray
from models import AgentMessage


class TestRay:
    """Test Ray agent functions."""
    
    @pytest.mark.asyncio
    async def test_ray_can_speak(self, sample_agent_config, sample_session, mock_litellm_agent_response):
        """Test that a Ray agent can generate a response."""
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_agent_response)):
            message = await Ray.speak(
                agent=sample_agent_config,
                session=sample_session,
                iteration_number=1,
                previous_messages=[]
            )
            
            # Verify message structure
            assert isinstance(message, AgentMessage)
            assert message.agent_id == sample_agent_config.id
            assert message.agent_role == sample_agent_config.role
            assert message.content is not None
            assert len(message.content) > 0
    
    @pytest.mark.asyncio
    async def test_ray_tracks_tokens(self, sample_agent_config, sample_session, mock_litellm_agent_response):
        """Test that Ray correctly tracks token usage."""
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_agent_response)):
            message = await Ray.speak(
                agent=sample_agent_config,
                session=sample_session,
                iteration_number=1,
                previous_messages=[]
            )
            
            # Verify token tracking
            assert message.tokens_in > 0
            assert message.tokens_out > 0
            assert message.tokens_in + message.tokens_out > 0
            
            # Verify agent's accumulated tokens
            assert sample_agent_config.tokens_in > 0
            assert sample_agent_config.tokens_out > 0
    
    @pytest.mark.asyncio
    async def test_ray_tracks_cost(self, sample_agent_config, sample_session, mock_litellm_agent_response):
        """Test that Ray tracks cost (even if approximate)."""
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_agent_response)):
            with patch('orchestrator.litellm.completion_cost', return_value=0.0025):
                message = await Ray.speak(
                    agent=sample_agent_config,
                    session=sample_session,
                    iteration_number=1,
                    previous_messages=[]
                )
                
                # Verify cost tracking
                assert message.cost >= 0
                assert sample_agent_config.cost_used >= 0
    
    @pytest.mark.asyncio
    async def test_ray_handles_api_error_gracefully(self, sample_agent_config, sample_session):
        """Test that Ray handles API errors gracefully."""
        
        with patch('orchestrator.litellm.acompletion', side_effect=Exception("API Error")):
            message = await Ray.speak(
                agent=sample_agent_config,
                session=sample_session,
                iteration_number=1,
                previous_messages=[]
            )
            
            # Should return error message instead of crashing
            assert isinstance(message, AgentMessage)
            assert "[Error:" in message.content
    
    @pytest.mark.asyncio
    async def test_ray_uses_correct_model_params(self, sample_agent_config, sample_session, mock_litellm_agent_response):
        """Test that Ray uses correct parameters for different models."""
        
        # Test with GPT-5 (should use max_completion_tokens)
        sample_agent_config.model = "gpt-5"
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_agent_response)) as mock_call:
            await Ray.speak(
                agent=sample_agent_config,
                session=sample_session,
                iteration_number=1,
                previous_messages=[]
            )
            
            # Verify the call was made with correct params
            call_kwargs = mock_call.call_args[1]
            assert "model" in call_kwargs
            assert "messages" in call_kwargs
            
            # For GPT-5, should use max_completion_tokens
            assert "max_completion_tokens" in call_kwargs or "max_tokens" in call_kwargs
    
    def test_ray_builds_prompt_with_context(self, sample_agent_config, sample_session):
        """Test that Ray builds prompts with proper context."""
        
        prompt = Ray._build_agent_prompt(
            agent=sample_agent_config,
            session=sample_session,
            iteration_number=1,
            previous_messages=[]
        )
        
        # Verify prompt contains key elements
        assert sample_agent_config.id in prompt
        assert sample_agent_config.role in prompt
        assert sample_session.issue in prompt
        assert "Iteration" in prompt or "iteration" in prompt

