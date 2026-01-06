"""
Factory for creating LLM model instances across different providers.

This module provides a unified interface for creating model instances
from different LLM providers (OpenAI, DeepSeek, Kimi, Groq) with consistent APIs.

Note: Groq has compatibility issues with PydanticAI's response validation
(service_tier='on_demand' not recognized). Use DeepSeek or OpenAI for production.
"""
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from .model_providers import ProviderType, ProviderConfig, get_provider_config
from .settings import settings


def create_model(provider: ProviderType, model_name: str = None):
    """
    Create a model instance for the specified provider.

    All supported providers are OpenAI-compatible, so we use OpenAIModel
    with custom base URLs via OpenAIProvider.

    Args:
        provider: The LLM provider to use (OPENAI, DEEPSEEK, KIMI, or GROQ)
        model_name: Specific model name (optional, uses provider default if None)

    Returns:
        OpenAIModel instance configured for the specified provider

    Raises:
        ValueError: If provider is not configured or model doesn't exist

    Example:
        >>> model = create_model(ProviderType.GROQ, "llama-3.1-70b-versatile")
        >>> agent = Agent(model=model, output_type=MyResponse)
    """
    # Validate provider configuration (checks API key exists)
    settings.validate_provider(provider)

    # Get provider configuration
    config: ProviderConfig = get_provider_config(provider)
    api_key = settings.get_api_key(provider)

    # Use default model if not specified
    if model_name is None:
        model_name = settings.get_default_model(provider)

    # Validate model exists for provider
    if model_name not in config.available_models:
        available = ", ".join(config.available_models.keys())
        raise ValueError(
            f"Model '{model_name}' not available for {provider.value}. "
            f"Available models: {available}"
        )

    # All supported providers are OpenAI-compatible
    if config.is_openai_compatible:
        # Create OpenAI-compatible provider with custom base URL and API key
        provider_instance = OpenAIProvider(
            base_url=config.base_url,
            api_key=api_key,
        )

        # Create model with the provider
        return OpenAIModel(
            model_name,
            provider=provider_instance,
        )
    else:
        raise ValueError(f"Provider {provider.value} is not yet supported")


def create_default_model():
    """
    Create model instance using default provider from settings.

    Reads DEFAULT_PROVIDER from environment variables and creates
    the corresponding model with its default configuration.

    Returns:
        OpenAIModel instance for the default provider

    Example:
        >>> # .env has DEFAULT_PROVIDER=groq
        >>> model = create_default_model()
        >>> # Returns Groq model instance
    """
    default_provider = settings.get_default_provider()
    return create_model(
        provider=default_provider,
        model_name=None  # Uses default model for provider
    )
