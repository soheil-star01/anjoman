"""Prompt for Ray agents to speak."""

from typing import Optional
from models import AgentConfig, Session, AgentMessage


def build_ray_agent_prompt(
    agent: AgentConfig,
    session: Session,
    iteration_number: int,
    previous_messages: list[AgentMessage],
    last_summary: Optional[str] = None
) -> str:
    """Build prompt for a Ray agent to speak.
    
    Args:
        agent: The agent configuration
        session: The current session
        iteration_number: Current iteration number
        previous_messages: Messages from this iteration so far
        last_summary: Optional summary from previous iteration (deprecated, now using session.iterations)
    
    Returns:
        The prompt string
    """
    
    style_note = f"\n\nYour style: {agent.style}" if agent.style else ""
    
    # Build conversation history for current iteration
    history = ""
    if previous_messages:
        history = "\n\nConversation so far in this iteration:\n"
        for msg in previous_messages:
            history += f"\n{msg.agent_role} ({msg.agent_id}):\n{msg.content}\n"
    
    # Build context from ALL previous iterations
    context = ""
    if session.iterations and len(session.iterations) > 0:
        context = "\n\n=== PREVIOUS ITERATIONS CONTEXT ===\n"
        
        for prev_iter in session.iterations:
            context += f"\n--- Iteration {prev_iter.iteration_number} ---\n"
            
            # Include user guidance if provided
            if prev_iter.user_guidance:
                context += f"User Guidance: {prev_iter.user_guidance}\n\n"
            
            # Include summary
            if prev_iter.summary:
                context += f"Summary: {prev_iter.summary.summary}\n"
                
                # Include key disagreements
                if prev_iter.summary.key_disagreements:
                    context += f"Key Disagreements: {', '.join(prev_iter.summary.key_disagreements)}\n"
                
                # Include suggested directions that were discussed
                if prev_iter.summary.suggested_directions:
                    directions = [d.option for d in prev_iter.summary.suggested_directions]
                    context += f"Directions Suggested: {', '.join(directions)}\n"
            
            context += "\n"
        
        context += "=== END PREVIOUS CONTEXT ===\n"
    
    return f"""You are {agent.id}, a {agent.role} in the Anjoman deliberation system.{style_note}

Issue under discussion:
{session.issue}

This is Iteration {iteration_number}.
{context}

Your task:
- IMPORTANT: Review the previous iterations context above to understand what has been discussed
- Build on insights from previous iterations - don't repeat what's already been covered
- Address any unresolved points or disagreements from earlier discussions
- Provide your unique perspective considering the discussion's progression
- Challenge assumptions where appropriate
- Contribute NEW insights or arguments that advance the discussion

Guidelines:
- Stay true to your role and style
- Be analytical and thoughtful
- Respectful of other perspectives
- Focused on moving the discussion forward
- Acknowledge and reference previous points when relevant

Length: 150-300 words (be concise but thorough).
{history}

Provide your analysis:"""

