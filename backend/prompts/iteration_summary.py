"""Prompt for Dana to summarize iterations."""

from models import Session, Iteration


def build_iteration_summary_prompt(
    session: Session,
    iteration: Iteration
) -> str:
    """Build prompt for Dana to summarize an iteration.
    
    Args:
        session: The session being summarized
        iteration: The iteration to summarize
    
    Returns:
        The prompt string
    """
    
    messages_text = "\n\n".join([
        f"{msg.agent_role} ({msg.agent_id}):\n{msg.content}"
        for msg in iteration.messages
    ])
    
    return f"""Summarize this iteration of the Anjoman discussion.

Original Issue: {session.issue}

Iteration {iteration.iteration_number} Discussion:
{messages_text}

Provide:
1. A concise summary (3-5 sentences)
2. Key disagreements or tensions (if any)
3. Multiple suggested directions for the next iteration (2-4 specific, actionable options)

Respond in JSON format:
{{
  "summary": "...",
  "key_disagreements": ["...", "..."],
  "suggested_directions": [
    {{"option": "Focus on clarifying key terms and definitions", "description": "Examine what each participant means by core concepts"}},
    {{"option": "Evaluate specific arguments in detail", "description": "Deep dive into one or two key arguments"}},
    {{"option": "Explore practical implications", "description": "Discuss how different views affect real-world decisions"}}
  ]
}}

Each suggested direction should be:
- Specific and actionable (not vague)
- Concise (the "option" should be 5-10 words)
- Different from the others
- Relevant to where the discussion is now
"""

