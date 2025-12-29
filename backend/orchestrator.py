"""Orchestration logic for Anjoman - Dana and Rays."""

from typing import Optional
import litellm
import os
from datetime import datetime
from models import (
    Session, AgentConfig, AgentMessage, Iteration,
    IterationSummary, SuggestedDirection, SessionStatus, SessionProposal, ApiKeys, ModelInfo
)
from prompts import (
    DANA_SYSTEM_PROMPT,
    build_agent_proposal_prompt,
    build_iteration_summary_prompt,
    build_ray_agent_prompt
)
from models_config import MODELS, get_model_tiers


class Dana:
    """The orchestrator - proposes agents, enforces turns, and summarizes."""
    
    @staticmethod
    def _set_api_keys(api_keys: Optional[ApiKeys] = None):
        """Set API keys from user or environment."""
        if api_keys:
            if api_keys.openai_api_key:
                os.environ['OPENAI_API_KEY'] = api_keys.openai_api_key
            if api_keys.anthropic_api_key:
                os.environ['ANTHROPIC_API_KEY'] = api_keys.anthropic_api_key
            if api_keys.mistral_api_key:
                os.environ['MISTRAL_API_KEY'] = api_keys.mistral_api_key
            if api_keys.google_api_key:
                os.environ['GOOGLE_API_KEY'] = api_keys.google_api_key
            if api_keys.cohere_api_key:
                os.environ['COHERE_API_KEY'] = api_keys.cohere_api_key
    
    @staticmethod
    def _get_model_tiers(api_keys: Optional[ApiKeys] = None) -> dict[str, dict]:
        """Get available models organized by tier (budget/balanced/performance)."""
        # Get model tiers from centralized config
        model_tiers = get_model_tiers()

        # Filter by available API keys
        if api_keys:
            available_providers = api_keys.get_available_providers()
            return {p: tiers for p, tiers in model_tiers.items() if p in available_providers}

        return model_tiers
    
    @staticmethod
    def _get_available_models(api_keys: Optional[ApiKeys] = None) -> list[ModelInfo]:
        """Get list of available models based on provided API keys."""
        # Convert centralized config to ModelInfo objects
        models = []

        for model_config in MODELS:
            models.append(ModelInfo(
                model_id=model_config.model_id,
                display_name=model_config.display_name,
                provider=model_config.provider,
                description=model_config.description
            ))

        # Filter by available API keys
        if api_keys:
            available_providers = api_keys.get_available_providers()
            models = [m for m in models if m.provider in available_providers]

        return models
    
    @staticmethod
    async def propose_agents(
        issue: str, 
        budget: float, 
        num_agents: Optional[int] = None,
        model_preference: str = "balanced",
        api_keys: Optional[ApiKeys] = None
    ) -> SessionProposal:
        """Propose agent configuration based on the issue."""
        
        Dana._set_api_keys(api_keys)
        
        # Get available models and model tiers
        available_models = Dana._get_available_models(api_keys)
        model_tiers = Dana._get_model_tiers(api_keys)
        
        # Build available providers string (not all model names to save tokens)
        available_providers = list(model_tiers.keys())
        providers_str = ", ".join(available_providers)
        
        # Build prompt
        prompt = build_agent_proposal_prompt(
            issue=issue,
            budget=budget,
            num_agents=num_agents,
            model_preference=model_preference,
            providers_str=providers_str
        )
        
        try:
            response = await litellm.acompletion(
                model="gpt-5.1",  # Use latest GPT-5.1 for Dana
                messages=[
                    {"role": "system", "content": DANA_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Convert to AgentConfig objects
            agents = []
            agent_list = result['agents']
            
            # If num_agents specified, limit to that; otherwise use Dana's decision
            if num_agents:
                agent_list = agent_list[:num_agents]
            
            for idx, agent_data in enumerate(agent_list, 1):
                agents.append(AgentConfig(
                    id=f"Ray-{idx}",  # Capital R
                    role=agent_data['role'],
                    style=agent_data.get('style'),
                    model=agent_data['model']
                ))
            
            return SessionProposal(
                proposed_agents=agents,
                rationale=result['rationale'],
                available_models=available_models
            )
            
        except Exception as e:
            print(f"Error proposing agents: {e}")
            # Fallback to default configuration
            return Dana._default_proposal(num_agents or 3, api_keys)
    
    @staticmethod
    def _default_proposal(num_agents: int = 3, api_keys: Optional[ApiKeys] = None) -> SessionProposal:
        """Fallback agent proposal."""
        available_models = Dana._get_available_models(api_keys)
        
        # Pick best available models
        default_model = available_models[0].model_id if available_models else "gpt-4o"
        
        # Default roles to cycle through
        default_roles = [
            ("Analyst", "data-driven"),
            ("Critic", "skeptical"),
            ("Strategist", "pragmatic"),
            ("Synthesizer", "integrative"),
            ("Domain Expert", "specialized"),
        ]
        
        # Create requested number of agents
        agents = []
        for i in range(num_agents):
            role, style = default_roles[i % len(default_roles)]
            agents.append(AgentConfig(
                id=f"Ray-{i+1}",  # Capital R
                role=role,
                style=style,
                model=default_model
            ))
        
        return SessionProposal(
            proposed_agents=agents,
            rationale=f"Default configuration with {num_agents} agents using available models for diverse perspectives.",
            available_models=available_models
        )
    
    @staticmethod
    async def summarize_iteration(
        session: Session,
        iteration: Iteration,
        api_keys: Optional[ApiKeys] = None
    ) -> IterationSummary:
        """Create a summary after an iteration."""
        
        Dana._set_api_keys(api_keys)
        
        # Build prompt
        prompt = build_iteration_summary_prompt(session, iteration)
        
        try:
            response = await litellm.acompletion(
                model="gpt-5.1",  # Use latest GPT-5.1 for summaries
                messages=[
                    {"role": "system", "content": DANA_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Parse suggested directions
            suggested_directions = []
            if 'suggested_directions' in result:
                for direction in result['suggested_directions']:
                    suggested_directions.append(SuggestedDirection(
                        option=direction['option'],
                        description=direction['description']
                    ))
            
            # Fallback for old format
            suggested_direction_text = result.get('suggested_direction', '')
            
            return IterationSummary(
                iteration_number=iteration.iteration_number,
                summary=result['summary'],
                key_disagreements=result.get('key_disagreements'),
                suggested_directions=suggested_directions,
                suggested_direction=suggested_direction_text,  # Keep for backwards compatibility
                total_cost=sum(msg.cost for msg in iteration.messages),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"Error summarizing iteration: {e}")
            return IterationSummary(
                iteration_number=iteration.iteration_number,
                summary="Error generating summary.",
                suggested_directions=[
                    SuggestedDirection(
                        option="Continue discussion",
                        description="Continue the current line of reasoning"
                    )
                ],
                suggested_direction="Continue discussion.",
                total_cost=sum(msg.cost for msg in iteration.messages),
                timestamp=datetime.now()
            )


class Ray:
    """An LLM agent with a specific role and model."""
    
    @staticmethod
    async def speak(
        agent: AgentConfig,
        session: Session,
        iteration_number: int,
        previous_messages: list[AgentMessage],
        api_keys: Optional[ApiKeys] = None
    ) -> AgentMessage:
        """Have an agent contribute to the discussion."""
        
        Dana._set_api_keys(api_keys)
        
        # Build prompt (now includes full context from session.iterations)
        prompt = build_ray_agent_prompt(
            agent=agent,
            session=session,
            iteration_number=iteration_number,
            previous_messages=previous_messages,
            last_summary=None  # No longer needed, using session.iterations instead
        )
        
        try:
            # Use max_completion_tokens for newer models (GPT-5+, Claude 4+)
            # Use max_tokens for older models
            params = {
                "model": agent.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7,
            }
            
            # Newer models use max_completion_tokens
            if any(x in agent.model.lower() for x in ['gpt-5', 'claude-opus-4-5', 'claude-4-5-sonnet']):
                params["max_completion_tokens"] = 500
            else:
                params["max_tokens"] = 500
            
            response = await litellm.acompletion(**params)
            
            # Extract usage information
            usage = response.usage
            tokens_in = usage.prompt_tokens
            tokens_out = usage.completion_tokens
            
            # Calculate cost using LiteLLM's completion_cost
            try:
                cost = litellm.completion_cost(completion_response=response)
            except Exception as e:
                print(f"Could not calculate cost: {e}")
                cost = 0.0
            
            # Update agent's accumulated stats
            agent.tokens_in += tokens_in
            agent.tokens_out += tokens_out
            agent.cost_used += cost
            
            content = response.choices[0].message.content
            
            return AgentMessage(
                agent_id=agent.id,
                agent_role=agent.role,
                content=content,
                timestamp=datetime.now(),
                tokens_in=tokens_in,
                tokens_out=tokens_out,
                cost=cost
            )
            
        except Exception as e:
            print(f"Error getting response from {agent.id}: {e}")
            # Return an error message
            return AgentMessage(
                agent_id=agent.id,
                agent_role=agent.role,
                content=f"[Error: Unable to get response from {agent.model}]",
                timestamp=datetime.now(),
                tokens_in=0,
                tokens_out=0,
                cost=0.0
            )

