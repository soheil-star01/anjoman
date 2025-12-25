"""Configuration management for Anjoman backend."""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    mistral_api_key: str = ""
    cohere_api_key: str = ""
    together_api_key: str = ""
    
    # Application
    sessions_dir: str = "../data/sessions"
    default_budget: float = 5.00
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

