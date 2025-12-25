"""Orchestration logic for Anjoman - Dana and Rays."""

from typing import Optional
import litellm
from datetime import datetime
from models import (
    Session, AgentConfig, AgentMessage, Iteration, 
    IterationSummary, SessionStatus, SessionProposal
)


class Dana:
    """The orchestrator - proposes agents, enforces turns, and summarizes."""
    
    DANA_SYSTEM_PROMPT = """You are Dana, the moderator of Anjoman - a structured multi-LLM deliberation system.

Your responsibilities:
1. Propose agent setups (number, roles, models) based on the user's issue
2. Summarize discussions after each iteration
3. Identify key disagreements
4. Suggest directions for the next iteration

You are NOT a decision maker. You facilitate structured thinking.

When proposing agents:
- Suggest 3-5 agents with diverse perspectives
- Assign clear, distinct roles
- Consider the complexity of the issue
- Recommend appropriate models for each role

When summarizing:
- Be concise (3-5 sentences)
- Highlight key insights and disagreements
- Suggest a concrete direction forward
"""
    
    @staticmethod
    async def propose_agents(issue: str, budget: float) -> SessionProposal:
        """Propose agent configuration based on the issue."""
        
        prompt = f"""Given this issue, propose 3-5 agents (Rays) to discuss it.

Issue: {issue}

Budget: ${budget:.2f}

For each agent, specify:
- role (e.g., Analyst, Critic, Strategist, Domain Expert, Ethicist)
- style (optional, brief behavioral note)
- model (choose from: gpt-4-turbo, gpt-3.5-turbo, claude-3-sonnet, claude-3-haiku, mistral-large, mistral-medium)

Consider:
- Complexity of the issue
- Need for diverse perspectives
- Budget constraints (more expensive models for key roles)

Respond in JSON format:
{{
  "agents": [
    {{"role": "Analyst", "style": "data-driven", "model": "gpt-4-turbo"}},
    ...
  ],
  "rationale": "Brief explanation of your choices"
}}
"""
        
        try:
            response = await litellm.acompletion(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": Dana.DANA_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            # Convert to AgentConfig objects
            agents = []
            for idx, agent_data in enumerate(result['agents'], 1):
                agents.append(AgentConfig(
                    id=f"ray-{idx}",
                    role=agent_data['role'],
                    style=agent_data.get('style'),
                    model=agent_data['model']
                ))
            
            return SessionProposal(
                proposed_agents=agents,
                rationale=result['rationale']
            )
            
        except Exception as e:
            print(f"Error proposing agents: {e}")
            # Fallback to default configuration
            return Dana._default_proposal()
    
    @staticmethod
    def _default_proposal() -> SessionProposal:
        """Fallback agent proposal."""
        return SessionProposal(
            proposed_agents=[
                AgentConfig(id="ray-1", role="Analyst", model="gpt-4-turbo"),
                AgentConfig(id="ray-2", role="Critic", model="claude-3-sonnet"),
                AgentConfig(id="ray-3", role="Strategist", model="gpt-3.5-turbo")
            ],
            rationale="Default balanced configuration with diverse perspectives."
        )
    
    @staticmethod
    async def summarize_iteration(
        session: Session,
        iteration: Iteration
    ) -> IterationSummary:
        """Create a summary after an iteration."""
        
        # Build conversation context
        messages_text = "\n\n".join([
            f"{msg.agent_role} ({msg.agent_id}):\n{msg.content}"
            for msg in iteration.messages
        ])
        
        prompt = f"""Summarize this iteration of the Anjoman discussion.

Original Issue: {session.issue}

Iteration {iteration.iteration_number} Discussion:
{messages_text}

Provide:
1. A concise summary (3-5 sentences)
2. Key disagreements or tensions (if any)
3. A suggested direction for the next iteration

Respond in JSON format:
{{
  "summary": "...",
  "key_disagreements": ["...", "..."],
  "suggested_direction": "..."
}}
"""
        
        try:
            response = await litellm.acompletion(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": Dana.DANA_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return IterationSummary(
                iteration_number=iteration.iteration_number,
                summary=result['summary'],
                key_disagreements=result.get('key_disagreements'),
                suggested_direction=result['suggested_direction'],
                total_cost=sum(msg.cost for msg in iteration.messages),
                timestamp=datetime.now()
            )
            
        except Exception as e:
            print(f"Error summarizing iteration: {e}")
            return IterationSummary(
                iteration_number=iteration.iteration_number,
                summary="Error generating summary.",
                suggested_direction="Continue discussion.",
                total_cost=sum(msg.cost for msg in iteration.messages),
                timestamp=datetime.now()
            )


class Ray:
    """An LLM agent with a specific role and model."""
    
    @staticmethod
    def _build_agent_prompt(
        agent: AgentConfig,
        session: Session,
        iteration_number: int,
        previous_messages: list[AgentMessage]
    ) -> str:
        """Build the system prompt for an agent."""
        
        style_note = f"\nYour style: {agent.style}" if agent.style else ""
        
        # Build context from previous messages in this iteration
        context = ""
        if previous_messages:
            context = "\n\nPrevious responses in this iteration:\n"
            for msg in previous_messages:
                context += f"\n{msg.agent_role}: {msg.content}\n"
        
        # Build history from previous iterations
        history = ""
        if session.iterations:
            history = "\n\nPrevious iterations:\n"
            for prev_iter in session.iterations[-3:]:  # Last 3 iterations
                history += f"\nIteration {prev_iter.iteration_number} Summary:\n"
                history += prev_iter.summary.summary + "\n"
        
        prompt = f"""You are {agent.id}, a {agent.role} in the Anjoman deliberation system.{style_note}

Original Issue: {session.issue}

Current Iteration: {iteration_number}

Your role is to provide thoughtful analysis from your perspective. Be:
- Specific and concrete
- Evidence-based when possible
- Respectful of other perspectives
- Focused on the issue at hand

Length: 150-300 words (be concise but thorough).
{history}{context}

Provide your analysis:"""
        
        return prompt
    
    @staticmethod
    async def speak(
        agent: AgentConfig,
        session: Session,
        iteration_number: int,
        previous_messages: list[AgentMessage]
    ) -> AgentMessage:
        """Have an agent contribute to the discussion."""
        
        prompt = Ray._build_agent_prompt(
            agent, session, iteration_number, previous_messages
        )
        
        try:
            response = await litellm.acompletion(
                model=agent.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract usage information
            usage = response.usage
            tokens_in = usage.prompt_tokens
            tokens_out = usage.completion_tokens
            
            # Calculate cost (LiteLLM provides this)
            cost = 0.0
            if hasattr(response, '_hidden_params') and 'response_cost' in response._hidden_params:
                cost = response._hidden_params['response_cost']
            
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

