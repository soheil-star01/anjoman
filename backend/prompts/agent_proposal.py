"""Prompt for Dana to propose agents."""

from typing import Optional
from models_config import get_example_models_by_tier


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

    # Get example models from centralized config
    examples = get_example_models_by_tier()
    budget_examples = ", ".join(examples["budget"])
    balanced_examples = ", ".join(examples["balanced"])
    performance_examples = ", ".join(examples["performance"])

    # Pick one example for the JSON demo
    demo_model = examples[model_preference][0] if examples[model_preference] else "claude-sonnet-4-5-20250929"

    return f"""Given this issue, propose {agent_count_instruction} to discuss it.

Issue: {issue}

Budget: ${budget:.2f}
Model Preference: {model_preference} (budget-friendly / balanced / performance-focused)

Available providers: {providers_str}

Based on the model preference:
- If "budget": Choose economical models (e.g., {budget_examples})
- If "balanced": Choose mid-tier models (e.g., {balanced_examples})
- If "performance": Choose most capable models (e.g., {performance_examples})

IMPORTANT: Use EXACT model IDs as shown above. Do not use shortcuts like "claude-3-5-sonnet" or add "-latest" suffix.

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
    {{"role": "Analyst", "style": "data-driven", "model": "{demo_model}"}},
    ...
  ],
  "rationale": "Brief explanation of your choices and agent count decision"
}}

Remember: Use exact model IDs from the lists above, not shortcuts.
"""

