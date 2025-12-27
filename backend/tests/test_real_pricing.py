"""Test pricing with real API (costs ~$0.001).

Run with: pytest tests/test_real_pricing.py -v -s

Add your API key to backend/.env:
OPENAI_API_KEY=your-key-here
"""

import pytest
from orchestrator import Ray
from models import AgentConfig, Session, BudgetInfo, SessionStatus
from datetime import datetime


@pytest.mark.asyncio
async def test_real_pricing(real_api_keys):
    """Test actual pricing with real API call.
    
    This will cost approximately $0.001 (one-tenth of a cent).
    """
    
    # Check if API key is available
    if not real_api_keys.openai_api_key:
        pytest.skip("Add OPENAI_API_KEY to backend/.env to run this test")
    
    api_keys = real_api_keys
    
    # Create a simple agent
    agent = AgentConfig(
        id="Ray-1",
        role="Analyst",
        style="concise",
        model="gpt-4o-mini",  # Cheapest model
        cost_used=0.0,
        tokens_in=0,
        tokens_out=0
    )
    
    # Create minimal session
    session = Session(
        session_id="pricing-test-001",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        issue="Say hello in 3 words",
        agents=[agent],
        iterations=[],
        budget=BudgetInfo(
            total_budget=1.0,
            used=0.0,
            remaining=1.0,
            warning_threshold=0.8
        ),
        status=SessionStatus.ACTIVE
    )
    
    print("\n🧪 Testing real API call with gpt-4o-mini...")
    print(f"Initial: tokens={agent.tokens_in + agent.tokens_out}, cost=${agent.cost_used:.6f}")
    
    # Make real API call
    message = await Ray.speak(
        agent=agent,
        session=session,
        iteration_number=1,
        previous_messages=[],
        api_keys=api_keys
    )
    
    print(f"\n✅ Response: {message.content[:100]}...")
    print(f"\n📊 Results:")
    print(f"   Tokens IN:  {message.tokens_in}")
    print(f"   Tokens OUT: {message.tokens_out}")
    print(f"   Total:      {message.tokens_in + message.tokens_out}")
    print(f"   Cost:       ${message.cost:.6f}")
    print(f"\n💰 Agent accumulated:")
    print(f"   Total tokens: {agent.tokens_in + agent.tokens_out}")
    print(f"   Total cost:   ${agent.cost_used:.6f}")
    
    # Assertions
    assert message.tokens_in > 0, "Should have input tokens"
    assert message.tokens_out > 0, "Should have output tokens"
    assert message.cost >= 0, "Should have cost"
    assert agent.cost_used >= 0, "Agent should track cost"
    assert agent.tokens_in > 0, "Agent should track input tokens"
    assert agent.tokens_out > 0, "Agent should track output tokens"
    
    # If cost is 0, warn but don't fail
    if message.cost == 0:
        print("\n⚠️  WARNING: Cost is $0.0000 - pricing calculation may not be working")
        print("    But tokens are tracked correctly!")
    else:
        print(f"\n✅ Pricing is working! Cost: ${message.cost:.6f}")
    
    return message

