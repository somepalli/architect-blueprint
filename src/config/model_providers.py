"""
Model provider configurations and metadata.
"""
from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel, Field


class ProviderType(str, Enum):
    """Supported LLM providers."""
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    KIMI = "kimi"
    GROQ = "groq"


class ModelConfig(BaseModel):
    """Configuration for a specific model."""
    name: str
    display_name: str
    input_cost_per_1m: float  # USD per 1M tokens
    output_cost_per_1m: float
    max_tokens: int
    supports_structured_output: bool = True
    recommended_temperature: float = 0.3


class ProviderConfig(BaseModel):
    """Configuration for an LLM provider."""
    type: ProviderType
    display_name: str
    base_url: str
    api_key_env_var: str
    available_models: Dict[str, ModelConfig]
    is_openai_compatible: bool = True


# Provider Definitions
PROVIDER_CONFIGS: Dict[ProviderType, ProviderConfig] = {
    ProviderType.OPENAI: ProviderConfig(
        type=ProviderType.OPENAI,
        display_name="OpenAI",
        base_url="https://api.openai.com/v1",
        api_key_env_var="OPENAI_API_KEY",
        is_openai_compatible=True,
        available_models={
            "gpt-4-turbo": ModelConfig(
                name="gpt-4-turbo",
                display_name="GPT-4 Turbo",
                input_cost_per_1m=10.0,
                output_cost_per_1m=30.0,
                max_tokens=4096,
                recommended_temperature=0.3,
            ),
            "gpt-4o": ModelConfig(
                name="gpt-4o",
                display_name="GPT-4o",
                input_cost_per_1m=2.5,
                output_cost_per_1m=10.0,
                max_tokens=4096,
                recommended_temperature=0.3,
            ),
        }
    ),
    ProviderType.DEEPSEEK: ProviderConfig(
        type=ProviderType.DEEPSEEK,
        display_name="DeepSeek",
        base_url="https://api.deepseek.com/v1",
        api_key_env_var="DEEPSEEK_API_KEY",
        is_openai_compatible=True,
        available_models={
            "deepseek-chat": ModelConfig(
                name="deepseek-chat",
                display_name="DeepSeek Chat",
                input_cost_per_1m=0.27,
                output_cost_per_1m=1.10,
                max_tokens=4096,
                recommended_temperature=0.3,
            ),
            "deepseek-reasoner": ModelConfig(
                name="deepseek-reasoner",
                display_name="DeepSeek Reasoner",
                input_cost_per_1m=0.55,
                output_cost_per_1m=2.19,
                max_tokens=8192,
                recommended_temperature=0.5,
            ),
        }
    ),
    ProviderType.KIMI: ProviderConfig(
        type=ProviderType.KIMI,
        display_name="Kimi (MoonshotAI)",
        base_url="https://api.moonshot.cn/v1",
        api_key_env_var="MOONSHOT_API_KEY",
        is_openai_compatible=True,
        available_models={
            "moonshot-v1-8k": ModelConfig(
                name="moonshot-v1-8k",
                display_name="Kimi K2 8K",
                input_cost_per_1m=2.0,
                output_cost_per_1m=6.0,
                max_tokens=8192,
                recommended_temperature=0.3,
            ),
        }
    ),
    ProviderType.GROQ: ProviderConfig(
        type=ProviderType.GROQ,
        display_name="Groq",
        base_url="https://api.groq.com/openai/v1",
        api_key_env_var="GROQ_API_KEY",
        is_openai_compatible=True,
        available_models={
            "llama-3.3-70b-versatile": ModelConfig(
                name="llama-3.3-70b-versatile",
                display_name="Llama 3.3 70B",
                input_cost_per_1m=0.0,
                output_cost_per_1m=0.0,
                max_tokens=8192,
                recommended_temperature=0.3,
            ),
            "openai/gpt-oss-120b": ModelConfig(
                name="openai/gpt-oss-120b",
                display_name="GPT OSS 120B",
                input_cost_per_1m=0.0,
                output_cost_per_1m=0.0,
                max_tokens=8192,
                recommended_temperature=0.3,
            ),
            "moonshotai/kimi-k2-instruct-0905": ModelConfig(
                name="moonshotai/kimi-k2-instruct-0905",
                display_name="Kimi K2 Instruct",
                input_cost_per_1m=0.0,
                output_cost_per_1m=0.0,
                max_tokens=32768,
                recommended_temperature=0.3,
            ),
        }
    ),
}


def get_provider_config(provider: ProviderType) -> ProviderConfig:
    """Get configuration for a provider."""
    return PROVIDER_CONFIGS[provider]


def get_available_providers() -> list[str]:
    """Get list of available provider names for UI."""
    return [p.value for p in ProviderType]


def get_available_models(provider: ProviderType) -> list[str]:
    """Get available models for a provider."""
    config = PROVIDER_CONFIGS[provider]
    return list(config.available_models.keys())


def estimate_cost(provider: ProviderType, model_name: str, input_tokens: int, output_tokens: int) -> float:
    """Estimate cost for a request."""
    config = PROVIDER_CONFIGS[provider]
    model_config = config.available_models[model_name]

    input_cost = (input_tokens / 1_000_000) * model_config.input_cost_per_1m
    output_cost = (output_tokens / 1_000_000) * model_config.output_cost_per_1m

    return input_cost + output_cost
