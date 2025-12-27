"""Prompt for Dana to propose agents."""

from typing import Optional


def build_agent_proposal_prompt(
    issue: str,
    budget: float,
    num_agents: Optional[int],
    model_preference: str,
    providers_str: str
) -> str:
    """Build prompt for Dana to propose agents.
    
    Args:
        issue: The issue to discuss
        budget: Budget in dollars
        num_agents: Number of agents to propose (None = Dana decides)
        model_preference: "budget", "balanced", or "performance"
        providers_str: Comma-separated list of available providers
    
    Returns:
        The prompt string
    """
    
    agent_count_instruction = (
        f"exactly {num_agents} agents (Rays)" 
        if num_agents 
        else "3-5 agents (Rays) - you decide the optimal number"
    )
    
    return f"""Given this issue, propose {agent_count_instruction} to discuss it.

Issue: {issue}

Budget: ${budget:.2f}
Model Preference: {model_preference} (budget-friendly / balanced / performance-focused)

Available providers: {providers_str}

Based on the model preference:
- If "budget": Choose economical models (e.g., gpt-3.5-turbo, claude-3-haiku, mistral-small)
- If "balanced": Choose mid-tier models (e.g., gpt-4o, claude-3-5-sonnet, mistral-medium)  
- If "performance": Choose most capable models (e.g., gpt-5.1, claude-opus-4.5, mistral-large)

For each Ray, specify:
- role (e.g., Analyst, Critic, Strategist, Domain Expert, Ethicist, Synthesizer)
- style (brief behavioral description, e.g., "data-driven", "skeptical", "creative")
- model (choose appropriate models from available providers based on the preference tier)

Consider:
- Complexity of the issue
- Need for diverse perspectives
- Budget constraints
- Model preference (use appropriate tier models)
- Diverse model selection across available providers when possible

Respond in JSON format:
{{
  "agents": [
    {{"role": "Analyst", "style": "data-driven", "model": "claude-sonnet-4.5"}},
    ...
  ],
  "rationale": "Brief explanation of your choices and agent count decision"
}}
"""

