"""Test Claude API integration to verify model naming and response format."""

import pytest
import os
from dotenv import load_dotenv
import litellm

# Load environment variables from backend/.env
load_dotenv()


@pytest.mark.asyncio
async def test_claude_3_opus_api():
    """Test that Claude 3 Opus API works with correct model ID."""
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        pytest.skip("Add ANTHROPIC_API_KEY to backend/.env to run this test")

    # Set the API key
    os.environ['ANTHROPIC_API_KEY'] = api_key

    # Test with Claude 3 Opus
    model_id = "claude-3-opus-20240229"

    try:
        response = await litellm.acompletion(
            model=model_id,
            messages=[
                {"role": "user", "content": "Say 'Hello from Claude 3 Opus' and nothing else."}
            ],
            max_tokens=50
        )

        # Verify response structure
        assert response is not None
        assert hasattr(response, 'choices')
        assert len(response.choices) > 0
        assert hasattr(response.choices[0], 'message')

        # Get the response content
        content = response.choices[0].message.content
        print(f"\n✅ Claude 3 Opus Response: {content}")

        # Verify it's not an error
        assert not content.startswith('[Error:')
        assert 'Hello' in content or 'hello' in content

        # Verify usage tracking
        assert hasattr(response, 'usage')
        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0
        print(f"   Tokens: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")

        # Verify cost calculation
        cost = litellm.completion_cost(completion_response=response)
        assert cost > 0
        print(f"   Cost: ${cost:.6f}")

        print(f"✅ Claude 3 Opus ({model_id}) works correctly!\n")

    except Exception as e:
        pytest.fail(f"Claude 3 Opus API failed: {str(e)}")


@pytest.mark.asyncio
async def test_claude_3_haiku_api():
    """Test that Claude 3 Haiku API works with correct model ID."""
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        pytest.skip("Add ANTHROPIC_API_KEY to backend/.env to run this test")

    # Set the API key
    os.environ['ANTHROPIC_API_KEY'] = api_key

    # Test with Claude 3 Haiku
    model_id = "claude-3-haiku-20240307"

    try:
        response = await litellm.acompletion(
            model=model_id,
            messages=[
                {"role": "user", "content": "Say 'Hello from Claude 3 Haiku' and nothing else."}
            ],
            max_tokens=50
        )

        # Verify response structure
        assert response is not None
        assert hasattr(response, 'choices')
        assert len(response.choices) > 0
        assert hasattr(response.choices[0], 'message')

        # Get the response content
        content = response.choices[0].message.content
        print(f"\n✅ Claude 3 Haiku Response: {content}")

        # Verify it's not an error
        assert not content.startswith('[Error:')
        assert 'Hello' in content or 'hello' in content

        # Verify usage tracking
        assert hasattr(response, 'usage')
        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0
        print(f"   Tokens: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")

        # Verify cost calculation
        cost = litellm.completion_cost(completion_response=response)
        assert cost > 0
        print(f"   Cost: ${cost:.6f}")

        print(f"✅ Claude 3 Haiku ({model_id}) works correctly!\n")

    except Exception as e:
        pytest.fail(f"Claude 3 Haiku API failed: {str(e)}")


@pytest.mark.asyncio
async def test_claude_sonnet_4_5_api():
    """Test that Claude Sonnet 4.5 API works with correct model ID."""
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        pytest.skip("Add ANTHROPIC_API_KEY to backend/.env to run this test")

    # Set the API key
    os.environ['ANTHROPIC_API_KEY'] = api_key

    # Test with Claude Sonnet 4.5
    model_id = "claude-sonnet-4-5-20250929"

    try:
        response = await litellm.acompletion(
            model=model_id,
            messages=[
                {"role": "user", "content": "Say 'Hello from Claude Sonnet 4.5' and nothing else."}
            ],
            max_tokens=50
        )

        # Verify response structure
        assert response is not None
        assert hasattr(response, 'choices')
        assert len(response.choices) > 0
        assert hasattr(response.choices[0], 'message')

        # Get the response content
        content = response.choices[0].message.content
        print(f"\n✅ Claude Sonnet 4.5 Response: {content}")

        # Verify it's not an error
        assert not content.startswith('[Error:')
        assert 'Hello' in content or 'hello' in content

        # Verify usage tracking
        assert hasattr(response, 'usage')
        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0
        print(f"   Tokens: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")

        # Verify cost calculation
        cost = litellm.completion_cost(completion_response=response)
        assert cost > 0
        print(f"   Cost: ${cost:.6f}")

        print(f"✅ Claude Sonnet 4.5 ({model_id}) works correctly!\n")

    except Exception as e:
        pytest.fail(f"Claude Sonnet 4.5 API failed: {str(e)}")


@pytest.mark.asyncio
async def test_claude_opus_4_5_api():
    """Test that Claude Opus 4.5 API works with correct model ID."""
    api_key = os.getenv('ANTHROPIC_API_KEY')

    if not api_key:
        pytest.skip("Add ANTHROPIC_API_KEY to backend/.env to run this test")

    # Set the API key
    os.environ['ANTHROPIC_API_KEY'] = api_key

    # Test with Claude Opus 4.5
    model_id = "claude-opus-4-5-20251101"

    try:
        response = await litellm.acompletion(
            model=model_id,
            messages=[
                {"role": "user", "content": "Say 'Hello from Claude Opus 4.5' and nothing else."}
            ],
            max_tokens=50
        )

        # Verify response structure
        assert response is not None
        assert hasattr(response, 'choices')
        assert len(response.choices) > 0
        assert hasattr(response.choices[0], 'message')

        # Get the response content
        content = response.choices[0].message.content
        print(f"\n✅ Claude Opus 4.5 Response: {content}")

        # Verify it's not an error
        assert not content.startswith('[Error:')
        assert 'Hello' in content or 'hello' in content

        # Verify usage tracking
        assert hasattr(response, 'usage')
        assert response.usage.prompt_tokens > 0
        assert response.usage.completion_tokens > 0
        print(f"   Tokens: {response.usage.prompt_tokens} in, {response.usage.completion_tokens} out")

        # Verify cost calculation
        cost = litellm.completion_cost(completion_response=response)
        assert cost > 0
        print(f"   Cost: ${cost:.6f}")

        print(f"✅ Claude Opus 4.5 ({model_id}) works correctly!\n")

    except Exception as e:
        pytest.fail(f"Claude Opus 4.5 API failed: {str(e)}")


if __name__ == "__main__":
    # Allow running directly for quick testing
    import asyncio
    
    print("=" * 60)
    print("Testing Claude API Models")
    print("=" * 60)
    
    asyncio.run(test_claude_3_opus_api())
    asyncio.run(test_claude_3_haiku_api())
    asyncio.run(test_claude_sonnet_4_5_api())
    asyncio.run(test_claude_opus_4_5_api())
    
    print("=" * 60)
    print("All Claude API tests passed!")
    print("=" * 60)

