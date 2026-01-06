"""
Input models for user requests and preferences.
"""
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional


class DetailLevel(str, Enum):
    """Level of detail for the generated blueprint."""
    HIGH_LEVEL = "high_level"
    DETAILED = "detailed"
    PRODUCTION_READY = "production_ready"


class DeploymentPlatform(str, Enum):
    """Supported deployment platforms."""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"
    DIGITAL_OCEAN = "digital_ocean"
    HEROKU = "heroku"
    VERCEL = "vercel"
    RENDER = "render"
    RAILWAY = "railway"
    FLY_IO = "fly_io"
    OTHER = "other"


class UserInput(BaseModel):
    """User input for blueprint generation."""
    business_idea: str = Field(
        ...,
        min_length=10,
        description="Description of the SaaS business idea"
    )
    detail_level: DetailLevel = Field(
        default=DetailLevel.DETAILED,
        description="Level of detail for the blueprint"
    )
    deployment_platform: DeploymentPlatform = Field(
        default=DeploymentPlatform.AWS,
        description="Preferred deployment platform"
    )
    custom_platform: Optional[str] = Field(
        None,
        description="Custom platform name if 'other' is selected"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "business_idea": "A project management tool for remote teams with real-time collaboration",
                "detail_level": "detailed",
                "deployment_platform": "aws",
                "custom_platform": None
            }
        }
