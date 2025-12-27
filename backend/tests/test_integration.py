"""Integration tests for complete workflows."""

import pytest
from unittest.mock import AsyncMock, patch
from orchestrator import Dana, Ray
from models import ApiKeys, Iteration


class TestIntegration:
    """Test complete workflows."""
    
    @pytest.mark.asyncio
    async def test_complete_iteration_workflow(self, sample_api_keys, mock_litellm_response, mock_litellm_agent_response):
        """Test a complete iteration: propose -> agents speak -> summarize."""
        
        with patch('orchestrator.litellm.acompletion') as mock_completion:
            # Setup mock to return different responses
            mock_completion.side_effect = [
                mock_litellm_response,  # For Dana propose
                mock_litellm_agent_response,  # For Ray-1 speak
                mock_litellm_agent_response,  # For Ray-2 speak
                mock_litellm_response,  # For Dana summarize
            ]
            
            with patch('orchestrator.litellm.completion_cost', return_value=0.001):
                # Step 1: Dana proposes agents
                proposal = await Dana.propose_agents(
                    issue="Should we adopt microservices?",
                    budget=5.0,
                    num_agents=2,
                    model_preference="balanced",
                    api_keys=sample_api_keys
                )
                
                assert len(proposal.proposed_agents) > 0
                
                # Step 2: Create session
                from models import Session, BudgetInfo, SessionStatus
                from datetime import datetime
                
                session = Session(
                    session_id="test-integration-001",
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    issue="Should we adopt microservices?",
                    agents=proposal.proposed_agents[:2],
                    iterations=[],
                    budget=BudgetInfo(
                        total_budget=5.0,
                        used=0.0,
                        remaining=5.0,
                        warning_threshold=0.8
                    ),
                    status=SessionStatus.ACTIVE
                )
                
                # Step 3: Agents speak
                messages = []
                total_tokens = 0
                total_cost = 0.0
                
                for agent in session.agents:
                    message = await Ray.speak(
                        agent=agent,
                        session=session,
                        iteration_number=1,
                        previous_messages=messages
                    )
                    messages.append(message)
                    total_tokens += message.tokens_in + message.tokens_out
                    total_cost += message.cost
                
                # Verify agents spoke
                assert len(messages) == 2
                assert total_tokens > 0
                
                # Step 4: Dana summarizes
                iteration = Iteration(
                    iteration_number=1,
                    messages=messages,
                    summary=None
                )
                
                summary = await Dana.summarize_iteration(session, iteration)
                
                # Verify summary
                assert summary is not None
                assert summary.iteration_number == 1
                assert summary.total_cost >= 0
    
    @pytest.mark.asyncio
    async def test_token_accumulation(self, sample_api_keys, mock_litellm_agent_response):
        """Test that tokens accumulate correctly across multiple calls."""
        
        from models import AgentConfig, Session, BudgetInfo, SessionStatus
        from datetime import datetime
        
        agent = AgentConfig(
            id="Ray-1",
            role="Analyst",
            model="gpt-4o",
            cost_used=0.0,
            tokens_in=0,
            tokens_out=0
        )
        
        session = Session(
            session_id="test-token-001",
            created_at=datetime.now(),
            updated_at=datetime.now(),
            issue="Test issue",
            agents=[agent],
            iterations=[],
            budget=BudgetInfo(total_budget=5.0, used=0.0, remaining=5.0, warning_threshold=0.8),
            status=SessionStatus.ACTIVE
        )
        
        with patch('orchestrator.litellm.acompletion', new=AsyncMock(return_value=mock_litellm_agent_response)):
            with patch('orchestrator.litellm.completion_cost', return_value=0.001):
                # First call
                message1 = await Ray.speak(agent, session, 1, [])
                tokens_after_first = agent.tokens_in + agent.tokens_out
                cost_after_first = agent.cost_used
                
                # Second call
                message2 = await Ray.speak(agent, session, 2, [message1])
                tokens_after_second = agent.tokens_in + agent.tokens_out
                cost_after_second = agent.cost_used
                
                # Verify accumulation
                assert tokens_after_second > tokens_after_first
                assert cost_after_second >= cost_after_first
                assert tokens_after_second == (message1.tokens_in + message1.tokens_out + 
                                              message2.tokens_in + message2.tokens_out)

