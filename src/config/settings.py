"""
Application settings and configuration.
"""
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application configuration settings."""

    # === Multi-Provider LLM Configuration ===

    # Default provider (can be overridden by UI)
    # Use string initially, will convert to ProviderType after class definition
    DEFAULT_PROVIDER_STR: str = os.getenv("DEFAULT_PROVIDER", "openai")

    # API Keys for each provider
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEEPSEEK_API_KEY: str = os.getenv("DEEPSEEK_API_KEY", "")
    MOONSHOT_API_KEY: str = os.getenv("MOONSHOT_API_KEY", "")  # Kimi
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")  # Groq

    # Model names (defaults per provider)
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo")
    DEEPSEEK_MODEL: str = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    KIMI_MODEL: str = os.getenv("KIMI_MODEL", "moonshot-v1-8k")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Legacy support (kept for backward compatibility)
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4-turbo")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "4096"))
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.3"))

    # Application Settings
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    CACHE_ENABLED: bool = os.getenv("CACHE_ENABLED", "false").lower() == "true"

    # Agent Configuration
    AGENT_CONFIG = {
        "model": MODEL_NAME,
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
        "retries": 2,
        "timeout": 300,  # 5 minutes
    }

    # Orchestrator Agent (needs more context)
    ORCHESTRATOR_CONFIG = {
        "model": MODEL_NAME,
        "max_tokens": 4096,
        "temperature": 0.7,  # Higher for creative analysis
        "retries": 2,
        "timeout": 300,
    }

    # Specialist Agents (structured output - needs high token limit for complex outputs)
    SPECIALIST_CONFIG = {
        "model": MODEL_NAME,
        "max_tokens": 4096,  # Increased for DeepSeek compatibility
        "temperature": 0.3,  # Lower for structured output
        "retries": 2,
        "timeout": 300,
    }

    @classmethod
    def get_api_key(cls, provider) -> str:
        """
        Get API key for a provider.

        Args:
            provider: ProviderType enum value

        Returns:
            API key string
        """
        # Import here to avoid circular dependency
        from .model_providers import ProviderType

        mapping = {
            ProviderType.OPENAI: cls.OPENAI_API_KEY,
            ProviderType.DEEPSEEK: cls.DEEPSEEK_API_KEY,
            ProviderType.KIMI: cls.MOONSHOT_API_KEY,
            ProviderType.GROQ: cls.GROQ_API_KEY,
        }
        return mapping.get(provider, "")

    @classmethod
    def get_default_model(cls, provider) -> str:
        """
        Get default model for a provider.

        Args:
            provider: ProviderType enum value

        Returns:
            Model name string
        """
        # Import here to avoid circular dependency
        from .model_providers import ProviderType

        mapping = {
            ProviderType.OPENAI: cls.OPENAI_MODEL,
            ProviderType.DEEPSEEK: cls.DEEPSEEK_MODEL,
            ProviderType.KIMI: cls.KIMI_MODEL,
            ProviderType.GROQ: cls.GROQ_MODEL,
        }
        return mapping.get(provider, cls.MODEL_NAME)

    @classmethod
    def get_default_provider(cls):
        """Get the default provider from environment or fallback."""
        from .model_providers import ProviderType

        try:
            return ProviderType(cls.DEFAULT_PROVIDER_STR)
        except ValueError:
            # Fallback to OpenAI if invalid provider specified
            return ProviderType.OPENAI

    @classmethod
    def validate_provider(cls, provider) -> bool:
        """
        Check if provider is properly configured.

        Args:
            provider: ProviderType enum value

        Returns:
            True if valid

        Raises:
            ValueError: If provider API key is not set
        """
        from .model_providers import get_provider_config

        api_key = cls.get_api_key(provider)
        if not api_key:
            config = get_provider_config(provider)
            raise ValueError(
                f"{provider.value.upper()} provider requires {config.api_key_env_var} to be set in .env file"
            )
        return True

    @classmethod
    def validate(cls) -> bool:
        """Validate required settings (legacy - checks OpenAI only)."""
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY is not set. Please create a .env file with your API key."
            )
        return True

    @classmethod
    def get_model_config(cls, agent_type: str = "specialist") -> dict:
        """Get configuration for a specific agent type."""
        if agent_type == "orchestrator":
            return cls.ORCHESTRATOR_CONFIG.copy()
        return cls.SPECIALIST_CONFIG.copy()


# Singleton instance
settings = Settings()

# Validate on import
try:
    settings.validate()
except ValueError as e:
    print(f"Warning: {e}")
