"""Pytest configuration and fixtures."""

import sys
import pytest
import os
from pathlib import Path
from datetime import datetime

# Add parent directory to path so we can import modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Load .env file
from dotenv import load_dotenv
env_path = backend_dir / '.env'
load_dotenv(env_path)

from models import ApiKeys, AgentConfig, Session, BudgetInfo, SessionStatus


@pytest.fixture
def sample_api_keys():
    """Sample API keys for testing."""
    return ApiKeys(
        openai_api_key="sk-test-openai-key",
        anthropic_api_key="sk-ant-test-anthropic-key"
    )


@pytest.fixture
def real_api_keys():
    """Real API keys from .env file for integration tests."""
    return ApiKeys(
        openai_api_key=os.environ.get('OPENAI_API_KEY'),
        anthropic_api_key=os.environ.get('ANTHROPIC_API_KEY'),
        google_api_key=os.environ.get('GOOGLE_API_KEY'),
        mistral_api_key=os.environ.get('MISTRAL_API_KEY'),
        cohere_api_key=os.environ.get('COHERE_API_KEY')
    )


@pytest.fixture
def sample_agent_config():
    """Sample agent configuration."""
    return AgentConfig(
        id="Ray-1",
        role="Analyst",
        style="data-driven",
        model="gpt-4o",
        cost_used=0.0,
        tokens_in=0,
        tokens_out=0
    )


@pytest.fixture
def sample_session(sample_agent_config):
    """Sample session for testing."""
    return Session(
        session_id="test-session-001",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        issue="Should we adopt microservices architecture?",
        agents=[sample_agent_config],
        iterations=[],
        budget=BudgetInfo(
            total_budget=5.0,
            used=0.0,
            remaining=5.0,
            warning_threshold=0.8
        ),
        status=SessionStatus.ACTIVE
    )


@pytest.fixture
def mock_litellm_response():
    """Mock LiteLLM API response."""
    class MockChoice:
        def __init__(self):
            self.message = type('obj', (object,), {
                'content': '{"agents": [{"role": "Analyst", "style": "data-driven", "model": "gpt-4o"}], "rationale": "Test rationale"}'
            })()
    
    class MockUsage:
        def __init__(self):
            self.prompt_tokens = 100
            self.completion_tokens = 50
            self.total_tokens = 150
    
    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]
            self.usage = MockUsage()
            self.model = "gpt-4o"
            self._hidden_params = {}
    
    return MockResponse()


@pytest.fixture
def mock_litellm_agent_response():
    """Mock LiteLLM response for agent speaking."""
    class MockChoice:
        def __init__(self):
            self.message = type('obj', (object,), {
                'content': 'This is a thoughtful analysis of the microservices architecture question. Based on the complexity and team size, I recommend a careful evaluation of the trade-offs.'
            })()
    
    class MockUsage:
        def __init__(self):
            self.prompt_tokens = 200
            self.completion_tokens = 50
            self.total_tokens = 250
    
    class MockResponse:
        def __init__(self):
            self.choices = [MockChoice()]
            self.usage = MockUsage()
            self.model = "gpt-4o"
    
    return MockResponse()

