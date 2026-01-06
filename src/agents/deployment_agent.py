"""
Deployment plan generation agent using PydanticAI.
"""
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from ..models.deployment_models import DeploymentPlan
from ..config.settings import settings
from ..config.model_factory import create_default_model
from ..config.model_providers import ProviderType
from .prompts import get_deployment_prompt


# Create the deployment agent with default model
# NOTE: This will be recreated dynamically when user selects a different provider
deployment_agent = Agent(
    model=create_default_model(),
    output_type=DeploymentPlan,
    system_prompt="You are an expert DevOps architect. Generate comprehensive deployment plans with Mermaid infrastructure diagrams.",
    retries=settings.SPECIALIST_CONFIG["retries"],
)


def create_deployment_agent(provider: ProviderType, model_name: str = None) -> Agent:
    """
    Create deployment agent instance with specified provider.

    This allows dynamic creation of agents with different LLM providers
    based on user selection in the UI.

    Args:
        provider: LLM provider to use (OPENAI, DEEPSEEK, or KIMI)
        model_name: Specific model name (optional, uses provider default)

    Returns:
        Configured Agent instance for deployment plan generation

    Example:
        >>> agent = create_deployment_agent(ProviderType.DEEPSEEK, "deepseek-chat")
        >>> result = await agent.run("Create deployment plan for...")
    """
    from ..config.model_factory import create_model

    return Agent(
        model=create_model(provider, model_name),
        output_type=DeploymentPlan,
        system_prompt="You are an expert DevOps architect. Generate comprehensive deployment plans with Mermaid infrastructure diagrams.",
        retries=settings.SPECIALIST_CONFIG["retries"],
    )


async def generate_deployment_plan(
    requirements: str,
    database_schema: str,
    api_design: str,
    frontend_design: str,
    platform: str,
    detail_config: dict,
) -> DeploymentPlan:
    """
    Generate a deployment plan based on the complete application architecture.

    Args:
        requirements: Requirements analysis from architect agent
        database_schema: Database schema as string
        api_design: API design as string
        frontend_design: Frontend design as string
        platform: Target deployment platform
        detail_config: Detail level configuration for deployment

    Returns:
        DeploymentPlan object with infrastructure, services, and Mermaid diagram

    Raises:
        Exception: If deployment plan generation fails after retries
    """
    # Build the prompt
    prompt = get_deployment_prompt(
        requirements,
        database_schema,
        api_design,
        frontend_design,
        platform,
        detail_config,
    )

    # Run the agent with model settings for max_tokens
    result = await deployment_agent.run(
        prompt,
        model_settings=ModelSettings(max_tokens=settings.SPECIALIST_CONFIG["max_tokens"])
    )

    return result.output
