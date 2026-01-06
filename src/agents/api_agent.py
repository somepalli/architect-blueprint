"""
API design generation agent using PydanticAI.
"""
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from ..models.api_models import APIDesign
from ..config.settings import settings
from ..config.model_factory import create_default_model
from ..config.model_providers import ProviderType
from .prompts import get_api_prompt


# Create the API agent with default model
# NOTE: This will be recreated dynamically when user selects a different provider
api_agent = Agent(
    model=create_default_model(),
    output_type=APIDesign,
    system_prompt="You are an expert API architect. Generate comprehensive API designs with Mermaid sequence diagrams.",
    retries=settings.SPECIALIST_CONFIG["retries"],
)


def create_api_agent(provider: ProviderType, model_name: str = None) -> Agent:
    """
    Create API agent instance with specified provider.

    This allows dynamic creation of agents with different LLM providers
    based on user selection in the UI.

    Args:
        provider: LLM provider to use (OPENAI, DEEPSEEK, or KIMI)
        model_name: Specific model name (optional, uses provider default)

    Returns:
        Configured Agent instance for API design generation

    Example:
        >>> agent = create_api_agent(ProviderType.DEEPSEEK, "deepseek-chat")
        >>> result = await agent.run("Design API for...")
    """
    from ..config.model_factory import create_model

    return Agent(
        model=create_model(provider, model_name),
        output_type=APIDesign,
        system_prompt="You are an expert API architect. Generate comprehensive API designs with Mermaid sequence diagrams.",
        retries=settings.SPECIALIST_CONFIG["retries"],
    )


async def generate_api_design(
    requirements: str,
    database_schema: str,
    detail_config: dict,
) -> APIDesign:
    """
    Generate an API design based on requirements and database schema.

    Args:
        requirements: Requirements analysis from architect agent
        database_schema: Database schema as string (for context)
        detail_config: Detail level configuration for API

    Returns:
        APIDesign object with endpoints, authentication strategy, and Mermaid diagram

    Raises:
        Exception: If API design generation fails after retries
    """
    # Build the prompt
    prompt = get_api_prompt(requirements, database_schema, detail_config)

    # Run the agent with model settings for max_tokens
    result = await api_agent.run(
        prompt,
        model_settings=ModelSettings(max_tokens=settings.SPECIALIST_CONFIG["max_tokens"])
    )

    return result.output
