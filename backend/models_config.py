"""Centralized model configuration for all LLM providers.

This is the single source of truth for all model definitions.
Update this file to add/remove/modify models across the entire application.
"""

from typing import Literal
from pydantic import BaseModel


class ModelConfig(BaseModel):
    """Configuration for a single LLM model."""
    model_id: str
    display_name: str
    provider: Literal["openai", "anthropic", "mistral", "google", "cohere"]
    tier: Literal["budget", "balanced", "performance"]
    description: str
    input_per_1m: float  # Input cost per 1M tokens
    output_per_1m: float  # Output cost per 1M tokens
    note: str = ""


# Central model registry
MODELS = [
    # OpenAI Models
    ModelConfig(
        model_id="gpt-5.1",
        display_name="GPT-5.1",
        provider="openai",
        tier="performance",
        description="Latest with customizable personalities",
        input_per_1m=20.00,
        output_per_1m=100.00,
        note="Latest with customizable personalities"
    ),
    ModelConfig(
        model_id="gpt-5",
        display_name="GPT-5",
        provider="openai",
        tier="performance",
        description="Advanced reasoning capabilities",
        input_per_1m=15.00,
        output_per_1m=75.00,
        note="Advanced reasoning capabilities"
    ),
    ModelConfig(
        model_id="gpt-4o",
        display_name="GPT-4o",
        provider="openai",
        tier="balanced",
        description="Optimized multimodal model",
        input_per_1m=5.00,
        output_per_1m=15.00,
        note="Optimized multimodal model"
    ),
    ModelConfig(
        model_id="gpt-4-turbo",
        display_name="GPT-4 Turbo",
        provider="openai",
        tier="balanced",
        description="Fast and capable",
        input_per_1m=10.00,
        output_per_1m=30.00,
        note="Fast and capable"
    ),
    ModelConfig(
        model_id="gpt-4o-mini",
        display_name="GPT-4o Mini",
        provider="openai",
        tier="budget",
        description="Affordable intelligence",
        input_per_1m=0.15,
        output_per_1m=0.60,
        note="Affordable intelligence"
    ),
    ModelConfig(
        model_id="gpt-3.5-turbo",
        display_name="GPT-3.5 Turbo",
        provider="openai",
        tier="budget",
        description="Fast and economical",
        input_per_1m=0.50,
        output_per_1m=1.50,
        note="Fast and economical"
    ),

    # Anthropic Models
    ModelConfig(
        model_id="claude-opus-4-5-20251101",
        display_name="Claude Opus 4.5",
        provider="anthropic",
        tier="performance",
        description="Best for complex workflows",
        input_per_1m=5.00,
        output_per_1m=25.00,
        note="Best for complex workflows (Nov 2025)"
    ),
    ModelConfig(
        model_id="claude-sonnet-4-5-20250929",
        display_name="Claude Sonnet 4.5",
        provider="anthropic",
        tier="balanced",
        description="Superior coding, 1M context",
        input_per_1m=4.00,
        output_per_1m=20.00,
        note="Superior coding, 1M context (Sept 2025)"
    ),
    ModelConfig(
        model_id="claude-3-opus-20240229",
        display_name="Claude 3 Opus",
        provider="anthropic",
        tier="performance",
        description="Most capable Claude 3",
        input_per_1m=15.00,
        output_per_1m=75.00,
        note="Most capable Claude 3"
    ),
    ModelConfig(
        model_id="claude-3-haiku-20240307",
        display_name="Claude 3 Haiku",
        provider="anthropic",
        tier="budget",
        description="Fast and economical",
        input_per_1m=0.25,
        output_per_1m=1.25,
        note="Fast and economical"
    ),

    # Mistral Models
    ModelConfig(
        model_id="mistral-large-latest",
        display_name="Mistral Large",
        provider="mistral",
        tier="performance",
        description="Most capable Mistral",
        input_per_1m=4.00,
        output_per_1m=12.00,
        note="Most capable Mistral"
    ),
    ModelConfig(
        model_id="mistral-medium-latest",
        display_name="Mistral Medium",
        provider="mistral",
        tier="balanced",
        description="Balanced performance",
        input_per_1m=2.70,
        output_per_1m=8.10,
        note="Balanced performance"
    ),
    ModelConfig(
        model_id="mistral-small-latest",
        display_name="Mistral Small",
        provider="mistral",
        tier="budget",
        description="Fast and economical",
        input_per_1m=1.00,
        output_per_1m=3.00,
        note="Fast and economical"
    ),

    # Google Models
    ModelConfig(
        model_id="gemini-2.0-flash-exp",
        display_name="Gemini 2.0 Flash",
        provider="google",
        tier="performance",
        description="Latest Gemini, very fast",
        input_per_1m=0.00,
        output_per_1m=0.00,
        note="Latest Gemini, very fast (experimental)"
    ),
    ModelConfig(
        model_id="gemini-1.5-pro",
        display_name="Gemini 1.5 Pro",
        provider="google",
        tier="balanced",
        description="Advanced capabilities",
        input_per_1m=1.25,
        output_per_1m=5.00,
        note="Advanced capabilities"
    ),
    ModelConfig(
        model_id="gemini-1.5-flash",
        display_name="Gemini 1.5 Flash",
        provider="google",
        tier="budget",
        description="Fast responses",
        input_per_1m=0.075,
        output_per_1m=0.30,
        note="Fast responses"
    ),

    # Cohere Models
    ModelConfig(
        model_id="command-r-plus",
        display_name="Command R+",
        provider="cohere",
        tier="performance",
        description="Most capable Cohere",
        input_per_1m=3.00,
        output_per_1m=15.00,
        note="Most capable Cohere"
    ),
    ModelConfig(
        model_id="command-r",
        display_name="Command R",
        provider="cohere",
        tier="balanced",
        description="Balanced performance",
        input_per_1m=0.50,
        output_per_1m=1.50,
        note="Balanced performance"
    ),
]


def get_models_by_provider(provider: str) -> list[ModelConfig]:
    """Get all models for a specific provider."""
    return [m for m in MODELS if m.provider == provider]


def get_models_by_tier(tier: str) -> list[ModelConfig]:
    """Get all models for a specific tier."""
    return [m for m in MODELS if m.tier == tier]


def get_model_tiers() -> dict[str, dict[str, list[str]]]:
    """Get model IDs organized by provider and tier."""
    tiers = {}
    for provider in ["openai", "anthropic", "mistral", "google", "cohere"]:
        tiers[provider] = {
            "budget": [m.model_id for m in MODELS if m.provider == provider and m.tier == "budget"],
            "balanced": [m.model_id for m in MODELS if m.provider == provider and m.tier == "balanced"],
            "performance": [m.model_id for m in MODELS if m.provider == provider and m.tier == "performance"],
        }
    return tiers


def get_example_models_by_tier() -> dict[str, list[str]]:
    """Get example model IDs for each tier (used in prompts)."""
    examples = {}
    for tier in ["budget", "balanced", "performance"]:
        # Get 1-2 examples from different providers for each tier
        tier_models = get_models_by_tier(tier)
        # Prefer diverse providers
        examples[tier] = []
        seen_providers = set()
        for model in tier_models:
            if model.provider not in seen_providers and len(examples[tier]) < 3:
                examples[tier].append(model.model_id)
                seen_providers.add(model.provider)
    return examples


def get_model_by_id(model_id: str) -> ModelConfig | None:
    """Get a specific model by its ID."""
    for model in MODELS:
        if model.model_id == model_id:
            return model
    return None
