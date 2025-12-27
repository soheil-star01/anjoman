# Anjoman Backend Tests

Comprehensive test suite for Anjoman backend functionality.

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
```

### Run Specific Test Files

```bash
# Test Dana functionality
pytest tests/test_dana.py

# Test Ray functionality
pytest tests/test_ray.py

# Test integration
pytest tests/test_integration.py

# Test data models
pytest tests/test_models.py
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Specific Test

```bash
pytest tests/test_dana.py::TestDana::test_dana_proposes_agents -v
```

## Test Coverage

The test suite covers:

### Dana Orchestrator (`test_dana.py`)
- ✅ Agent proposal generation
- ✅ Respecting agent count preferences
- ✅ Model filtering by API keys
- ✅ Model tier organization
- ✅ Iteration summarization

### Ray Agents (`test_ray.py`)
- ✅ Agent response generation
- ✅ Token tracking
- ✅ Cost calculation
- ✅ Error handling
- ✅ Model parameter handling
- ✅ Prompt building with context

### Integration (`test_integration.py`)
- ✅ Complete iteration workflow
- ✅ Token accumulation across iterations
- ✅ End-to-end deliberation process

### Data Models (`test_models.py`)
- ✅ API key provider detection
- ✅ Budget tracking calculations
- ✅ Model validation
- ✅ Optional fields handling

## Mocking Strategy

Tests use mocked LLM API calls to:
- Avoid actual API costs
- Ensure consistent test results
- Run tests quickly
- Test error scenarios

## Continuous Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pip install -r requirements-dev.txt
    pytest
```

## Test Data

Test fixtures are defined in `conftest.py`:
- `sample_api_keys` - Mock API keys
- `sample_agent_config` - Mock agent configuration
- `sample_session` - Mock session
- `mock_litellm_response` - Mock LLM API responses

## Best Practices

1. **Run tests before committing**: `pytest`
2. **Check coverage**: `pytest --cov=.`
3. **Test new features**: Add tests when adding functionality
4. **Mock external calls**: Never hit real APIs in tests
5. **Keep tests fast**: Current suite runs in < 5 seconds

## Debugging Failed Tests

```bash
# Run with detailed output
pytest -vv

# Run with print statements visible
pytest -s

# Run just failed tests
pytest --lf

# Run with debugger on failure
pytest --pdb
```

