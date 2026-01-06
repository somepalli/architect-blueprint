"""
Main orchestrator agent for requirements analysis using PydanticAI.
"""
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

from ..models.blueprint_models import RequirementsAnalysis
from ..config.settings import settings
from ..config.model_factory import create_default_model
from ..config.model_providers import ProviderType
from .prompts import ARCHITECT_SYSTEM_PROMPT, get_requirements_analysis_prompt


# Create the architect agent with default model
# NOTE: This will be recreated dynamically when user selects a different provider
architect_agent = Agent(
    model=create_default_model(),
    output_type=RequirementsAnalysis,
    system_prompt=ARCHITECT_SYSTEM_PROMPT,
    retries=settings.ORCHESTRATOR_CONFIG["retries"],
)


def create_architect_agent(provider: ProviderType, model_name: str = None) -> Agent:
    """
    Create architect agent instance with specified provider.

    This allows dynamic creation of agents with different LLM providers
    based on user selection in the UI.

    Args:
        provider: LLM provider to use (OPENAI, DEEPSEEK, or KIMI)
        model_name: Specific model name (optional, uses provider default)

    Returns:
        Configured Agent instance for requirements analysis

    Example:
        >>> agent = create_architect_agent(ProviderType.DEEPSEEK, "deepseek-chat")
        >>> result = await agent.run("Analyze this SaaS idea...")
    """
    from ..config.model_factory import create_model

    return Agent(
        model=create_model(provider, model_name),
        output_type=RequirementsAnalysis,
        system_prompt=ARCHITECT_SYSTEM_PROMPT,
        retries=settings.ORCHESTRATOR_CONFIG["retries"],
    )


async def analyze_requirements(
    business_idea: str,
    detail_level: str,
) -> RequirementsAnalysis:
    """
    Analyze a business idea and extract technical requirements.

    Args:
        business_idea: The SaaS business idea to analyze
        detail_level: Level of detail required (high_level, detailed, production_ready)

    Returns:
        RequirementsAnalysis object with features, user types, entities, etc.

    Raises:
        Exception: If requirements analysis fails after retries
    """
    # Build the prompt
    prompt = get_requirements_analysis_prompt(business_idea, detail_level)

    # Run the agent with model settings for max_tokens
    result = await architect_agent.run(
        prompt,
        model_settings=ModelSettings(max_tokens=settings.ORCHESTRATOR_CONFIG["max_tokens"])
    )

    return result.output
