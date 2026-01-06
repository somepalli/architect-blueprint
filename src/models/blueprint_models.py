"""
Complete technical blueprint models aggregating all components.
"""
import uuid
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

from .input_models import UserInput
from .database_models import DatabaseSchema
from .api_models import APIDesign
from .frontend_models import FrontendDesign
from .deployment_models import DeploymentPlan


class RequirementsAnalysis(BaseModel):
    """Analysis of business requirements extracted from the idea."""
    core_features: List[str] = Field(
        ...,
        min_length=1,
        description="Core features of the application"
    )
    user_types: List[str] = Field(
        ...,
        min_length=1,
        description="Types of users who will use the application"
    )
    key_entities: List[str] = Field(
        ...,
        min_length=1,
        description="Key domain entities/concepts"
    )
    business_model: str = Field(
        ...,
        description="Business model and monetization approach"
    )
    complexity_assessment: str = Field(
        ...,
        description="Assessment of technical complexity (low, medium, high)"
    )
    key_technical_challenges: List[str] = Field(
        default_factory=list,
        description="Main technical challenges to address"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "core_features": [
                    "User authentication",
                    "Project creation and management",
                    "Real-time collaboration"
                ],
                "user_types": [
                    "Project Managers",
                    "Team Members",
                    "Clients"
                ],
                "key_entities": [
                    "User",
                    "Project",
                    "Task",
                    "Team"
                ],
                "business_model": "Freemium with tiered subscriptions",
                "complexity_assessment": "medium",
                "key_technical_challenges": [
                    "Real-time synchronization",
                    "Scalable notification system"
                ]
            }
        }


class TechnicalBlueprint(BaseModel):
    """Complete technical blueprint for a SaaS application."""
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique blueprint identifier"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Blueprint creation timestamp"
    )
    user_input: UserInput = Field(
        ...,
        description="Original user input and preferences"
    )
    requirements: RequirementsAnalysis = Field(
        ...,
        description="Analyzed requirements from business idea"
    )
    database_schema: DatabaseSchema = Field(
        ...,
        description="Database design and schema"
    )
    api_design: APIDesign = Field(
        ...,
        description="API endpoints and design"
    )
    frontend_design: FrontendDesign = Field(
        ...,
        description="Frontend architecture and components"
    )
    deployment_plan: DeploymentPlan = Field(
        ...,
        description="Deployment and infrastructure plan"
    )
    full_architecture_diagram: str = Field(
        ...,
        description="Complete Mermaid diagram showing full system architecture"
    )
    implementation_recommendations: List[str] = Field(
        ...,
        min_length=1,
        description="Implementation guidance and best practices"
    )
    next_steps: List[str] = Field(
        default_factory=list,
        description="Recommended next steps for implementation"
    )
    estimated_timeline: Optional[str] = Field(
        None,
        description="Rough timeline estimate for implementation"
    )
    technology_stack_summary: Dict[str, str] = Field(
        default_factory=dict,
        description="Summary of technology choices (e.g., {'frontend': 'React', 'backend': 'Node.js'})"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2024-01-01T00:00:00Z",
                "user_input": {},
                "requirements": {},
                "database_schema": {},
                "api_design": {},
                "frontend_design": {},
                "deployment_plan": {},
                "full_architecture_diagram": "graph TB\\n    Frontend --> Backend\\n    Backend --> Database",
                "implementation_recommendations": [
                    "Start with MVP features",
                    "Implement authentication first",
                    "Use feature flags for gradual rollout"
                ],
                "next_steps": [
                    "Set up development environment",
                    "Initialize git repository",
                    "Implement database schema"
                ],
                "estimated_timeline": "3-4 months for MVP",
                "technology_stack_summary": {
                    "frontend": "React with Next.js",
                    "backend": "Node.js with Express",
                    "database": "PostgreSQL",
                    "hosting": "AWS"
                }
            }
        }


# Import fix for circular dependency
from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from typing import Dict
