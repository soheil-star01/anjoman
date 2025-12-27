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
        model_tiers = {
            "openai": {
                "budget": ["gpt-3.5-turbo", "gpt-4o-mini"],
                "balanced": ["gpt-4o", "gpt-4-turbo"],
                "performance": ["gpt-5", "gpt-5.1"],
            },
            "anthropic": {
                "budget": ["claude-3-haiku-20240307"],
                "balanced": ["claude-3-5-sonnet-20241022", "claude-sonnet-4.5"],
                "performance": ["claude-opus-4.5", "claude-3-opus-20240229"],
            },
            "mistral": {
                "budget": ["mistral-small-latest"],
                "balanced": ["mistral-medium-latest"],
                "performance": ["mistral-large-latest"],
            },
            "google": {
                "budget": ["gemini-1.5-flash"],
                "balanced": ["gemini-1.5-pro"],
                "performance": ["gemini-2.0-flash-exp"],
            },
            "cohere": {
                "budget": ["command-r"],
                "balanced": ["command-r"],
                "performance": ["command-r-plus"],
            }
        }
        
        # Filter by available API keys
        if api_keys:
            available_providers = api_keys.get_available_providers()
            return {p: tiers for p, tiers in model_tiers.items() if p in available_providers}
        
        return model_tiers
    
    @staticmethod
    def _get_available_models(api_keys: Optional[ApiKeys] = None) -> list[ModelInfo]:
        """Get list of available models based on provided API keys."""
        models = []
        
        # Define all supported models by provider
        all_models = {
            "openai": [
                ModelInfo(model_id="gpt-5.1", display_name="GPT-5.1", provider="openai", 
                         description="Latest with customizable personalities"),
                ModelInfo(model_id="gpt-5", display_name="GPT-5", provider="openai",
                         description="Advanced reasoning capabilities"),
                ModelInfo(model_id="gpt-4o", display_name="GPT-4o", provider="openai",
                         description="Optimized multimodal model"),
                ModelInfo(model_id="gpt-4-turbo", display_name="GPT-4 Turbo", provider="openai",
                         description="Fast and capable"),
                ModelInfo(model_id="gpt-3.5-turbo", display_name="GPT-3.5 Turbo", provider="openai",
                         description="Fast and economical"),
            ],
            "anthropic": [
                ModelInfo(model_id="claude-opus-4.5", display_name="Claude Opus 4.5", provider="anthropic",
                         description="Best for complex workflows"),
                ModelInfo(model_id="claude-sonnet-4.5", display_name="Claude Sonnet 4.5", provider="anthropic",
                         description="Superior coding, 1M context"),
                ModelInfo(model_id="claude-3-5-sonnet-20241022", display_name="Claude 3.5 Sonnet", provider="anthropic",
                         description="Balanced performance"),
                ModelInfo(model_id="claude-3-opus-20240229", display_name="Claude 3 Opus", provider="anthropic",
                         description="Most capable Claude 3"),
                ModelInfo(model_id="claude-3-haiku-20240307", display_name="Claude 3 Haiku", provider="anthropic",
                         description="Fast and economical"),
            ],
            "mistral": [
                ModelInfo(model_id="mistral-large-latest", display_name="Mistral Large", provider="mistral",
                         description="Most capable Mistral"),
                ModelInfo(model_id="mistral-medium-latest", display_name="Mistral Medium", provider="mistral",
                         description="Balanced performance"),
                ModelInfo(model_id="mistral-small-latest", display_name="Mistral Small", provider="mistral",
                         description="Fast and economical"),
            ],
            "google": [
                ModelInfo(model_id="gemini-2.0-flash-exp", display_name="Gemini 2.0 Flash", provider="google",
                         description="Latest Gemini, very fast"),
                ModelInfo(model_id="gemini-1.5-pro", display_name="Gemini 1.5 Pro", provider="google",
                         description="Advanced capabilities"),
                ModelInfo(model_id="gemini-1.5-flash", display_name="Gemini 1.5 Flash", provider="google",
                         description="Fast and efficient"),
            ],
            "cohere": [
                ModelInfo(model_id="command-r-plus", display_name="Command R+", provider="cohere",
                         description="Advanced reasoning"),
                ModelInfo(model_id="command-r", display_name="Command R", provider="cohere",
                         description="Balanced performance"),
            ]
        }
        
        # If no API keys provided, return all models
        if not api_keys:
            for provider_models in all_models.values():
                models.extend(provider_models)
            return models
        
        # Return only models for which we have API keys
        available_providers = api_keys.get_available_providers()
        for provider in available_providers:
            if provider in all_models:
                models.extend(all_models[provider])
        
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
            if any(x in agent.model.lower() for x in ['gpt-5', 'claude-opus-4', 'claude-sonnet-4']):
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

