"""
Database schema generation agent using PydanticAI.
"""
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from ..models.database_models import DatabaseSchema
from ..config.settings import settings
from ..config.model_factory import create_default_model
from ..config.model_providers import ProviderType
from .prompts import get_database_prompt


# Create the database agent with default model
# NOTE: This will be recreated dynamically when user selects a different provider
database_agent = Agent(
    model=create_default_model(),
    output_type=DatabaseSchema,
    system_prompt="You are an expert database architect. Generate complete database schemas with Mermaid ER diagrams.",
    retries=settings.SPECIALIST_CONFIG["retries"],
)


def create_database_agent(provider: ProviderType, model_name: str = None) -> Agent:
    """
    Create database agent instance with specified provider.

    This allows dynamic creation of agents with different LLM providers
    based on user selection in the UI.

    Args:
        provider: LLM provider to use (OPENAI, DEEPSEEK, or KIMI)
        model_name: Specific model name (optional, uses provider default)

    Returns:
        Configured Agent instance for database schema generation

    Example:
        >>> agent = create_database_agent(ProviderType.DEEPSEEK, "deepseek-chat")
        >>> result = await agent.run("Design database schema for...")
    """
    from ..config.model_factory import create_model

    return Agent(
        model=create_model(provider, model_name),
        output_type=DatabaseSchema,
        system_prompt="You are an expert database architect. Generate complete database schemas with Mermaid ER diagrams.",
        retries=settings.SPECIALIST_CONFIG["retries"],
    )


async def generate_database_schema(
    requirements: str,
    detail_config: dict,
) -> DatabaseSchema:
    """
    Generate a database schema based on requirements.

    Args:
        requirements: Requirements analysis from architect agent
        detail_config: Detail level configuration for database

    Returns:
        DatabaseSchema object with tables, relationships, and Mermaid diagram

    Raises:
        Exception: If schema generation fails after retries
    """
    # Build the prompt
    prompt = get_database_prompt(requirements, detail_config)

    # Run the agent with model settings for max_tokens
    result = await database_agent.run(
        prompt,
        model_settings=ModelSettings(max_tokens=settings.SPECIALIST_CONFIG["max_tokens"])
    )

    return result.output
