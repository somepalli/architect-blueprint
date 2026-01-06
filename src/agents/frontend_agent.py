"""
Frontend architecture generation agent using PydanticAI.
"""
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from ..models.frontend_models import FrontendDesign
from ..config.settings import settings
from ..config.model_factory import create_default_model
from ..config.model_providers import ProviderType
from .prompts import get_frontend_prompt


# Create the frontend agent with default model
# NOTE: This will be recreated dynamically when user selects a different provider
frontend_agent = Agent(
    model=create_default_model(),
    output_type=FrontendDesign,
    system_prompt="You are an expert frontend architect. Generate modern frontend architectures with Mermaid component diagrams.",
    retries=settings.SPECIALIST_CONFIG["retries"],
)


def create_frontend_agent(provider: ProviderType, model_name: str = None) -> Agent:
    """
    Create frontend agent instance with specified provider.

    This allows dynamic creation of agents with different LLM providers
    based on user selection in the UI.

    Args:
        provider: LLM provider to use (OPENAI, DEEPSEEK, or KIMI)
        model_name: Specific model name (optional, uses provider default)

    Returns:
        Configured Agent instance for frontend design generation

    Example:
        >>> agent = create_frontend_agent(ProviderType.DEEPSEEK, "deepseek-chat")
        >>> result = await agent.run("Design frontend for...")
    """
    from ..config.model_factory import create_model

    return Agent(
        model=create_model(provider, model_name),
        output_type=FrontendDesign,
        system_prompt="You are an expert frontend architect. Generate modern frontend architectures with Mermaid component diagrams.",
        retries=settings.SPECIALIST_CONFIG["retries"],
    )


async def generate_frontend_design(
    requirements: str,
    api_design: str,
    detail_config: dict,
) -> FrontendDesign:
    """
    Generate a frontend design based on requirements and API design.

    Args:
        requirements: Requirements analysis from architect agent
        api_design: API design as string (for context)
        detail_config: Detail level configuration for frontend

    Returns:
        FrontendDesign object with components, routing, and Mermaid diagram

    Raises:
        Exception: If frontend design generation fails after retries
    """
    # Build the prompt
    prompt = get_frontend_prompt(requirements, api_design, detail_config)

    # Run the agent with model settings for max_tokens
    result = await frontend_agent.run(
        prompt,
        model_settings=ModelSettings(max_tokens=settings.SPECIALIST_CONFIG["max_tokens"])
    )

    return result.output
