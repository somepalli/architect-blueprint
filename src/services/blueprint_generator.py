"""
Main blueprint generation service that orchestrates all agents.
"""
from typing import AsyncGenerator, Optional
import json

from ..models.input_models import UserInput
from ..models.blueprint_models import TechnicalBlueprint
from ..config.detail_levels import get_detail_config, get_component_config
from ..config.settings import settings
from ..config.model_providers import ProviderType
from .streaming_handler import StreamingHandler, StreamingUpdate
from .diagram_builder import DiagramBuilder


class BlueprintGenerator:
    """Orchestrates the generation of complete technical blueprints."""

    def __init__(self, provider: Optional[ProviderType] = None, model_name: Optional[str] = None):
        """
        Initialize blueprint generator with optional provider override.

        Args:
            provider: LLM provider (defaults to settings.DEFAULT_PROVIDER)
            model_name: Specific model name (defaults to provider's default)
        """
        self.provider = provider or settings.get_default_provider()
        self.model_name = model_name
        self.streaming_handler = StreamingHandler()
        self.diagram_builder = DiagramBuilder()

    async def generate_blueprint_stream(
        self, user_input: UserInput
    ) -> AsyncGenerator[StreamingUpdate, None]:
        """
        Generate a complete blueprint with streaming updates.

        Args:
            user_input: User's business idea and preferences

        Yields:
            StreamingUpdate objects for real-time UI updates

        Returns:
            Complete TechnicalBlueprint (via final update)
        """
        # Reset streaming handler
        self.streaming_handler.reset()

        # Get detail configurations
        detail_level = user_input.detail_level.value
        detail_config = get_detail_config(detail_level)

        try:
            # Import agent creation functions
            from ..agents.architect_agent import create_architect_agent
            from ..agents.database_agent import create_database_agent
            from ..agents.api_agent import create_api_agent
            from ..agents.frontend_agent import create_frontend_agent
            from ..agents.deployment_agent import create_deployment_agent
            from ..agents.prompts import get_requirements_analysis_prompt

            # Phase 1: Requirements Analysis
            yield self.streaming_handler.create_update(
                phase="Requirements Analysis",
                reasoning=f"Analyzing your business idea with {self.provider.value.upper()}...",
                status="in_progress",
            )

            # Create architect agent with selected provider
            architect_agent = create_architect_agent(self.provider, self.model_name)
            prompt = get_requirements_analysis_prompt(user_input.business_idea, detail_level)
            result = await architect_agent.run(prompt)
            requirements = result.output

            requirements_text = f"""
**Core Features**: {', '.join(requirements.core_features)}

**User Types**: {', '.join(requirements.user_types)}

**Key Entities**: {', '.join(requirements.key_entities)}

**Business Model**: {requirements.business_model}

**Complexity**: {requirements.complexity_assessment}
"""

            yield self.streaming_handler.create_update(
                phase="Requirements Analysis",
                reasoning=requirements_text,
                data=requirements,
                status="completed",
            )

            # Phase 2: Database Schema
            yield self.streaming_handler.create_update(
                phase="Database Schema",
                reasoning="Designing a normalized database schema with tables, relationships, and indexes...",
                status="in_progress",
            )

            # Create database agent with selected provider
            database_agent = create_database_agent(self.provider, self.model_name)
            db_config = get_component_config(detail_level, "database")
            from ..agents.prompts import get_database_prompt
            db_prompt = get_database_prompt(requirements.model_dump_json(indent=2), db_config)
            db_result = await database_agent.run(db_prompt)
            database_schema = db_result.output

            db_summary = f"""
**Tables**: {len(database_schema.tables)}

**Key Tables**: {', '.join([t.name for t in database_schema.tables[:5]])}

**Design Rationale**: {database_schema.reasoning}
"""

            yield self.streaming_handler.create_update(
                phase="Database Schema",
                reasoning=db_summary,
                diagram=database_schema.mermaid_diagram,
                data=database_schema,
                status="completed",
            )

            # Phase 3: API Design
            yield self.streaming_handler.create_update(
                phase="API Design",
                reasoning="Creating RESTful API endpoints based on the database schema and business requirements...",
                status="in_progress",
            )

            # Create API agent with selected provider
            api_agent = create_api_agent(self.provider, self.model_name)
            api_config = get_component_config(detail_level, "api")
            from ..agents.prompts import get_api_prompt
            api_prompt = get_api_prompt(
                requirements.model_dump_json(indent=2),
                database_schema.model_dump_json(indent=2),
                api_config,
            )
            api_result = await api_agent.run(api_prompt)
            api_design = api_result.output

            api_summary = f"""
**Base URL**: {api_design.base_url}

**Endpoints**: {len(api_design.endpoints)}

**Authentication**: {api_design.authentication_strategy}

**Key Endpoints**: {', '.join([f"{e.method.value} {e.path}" for e in api_design.endpoints[:5]])}

**Design Rationale**: {api_design.reasoning}
"""

            yield self.streaming_handler.create_update(
                phase="API Design",
                reasoning=api_summary,
                diagram=api_design.mermaid_diagram,
                data=api_design,
                status="completed",
            )

            # Phase 4: Frontend Architecture
            yield self.streaming_handler.create_update(
                phase="Frontend Architecture",
                reasoning="Designing frontend component hierarchy and state management strategy...",
                status="in_progress",
            )

            # Create frontend agent with selected provider
            frontend_agent = create_frontend_agent(self.provider, self.model_name)
            frontend_config = get_component_config(detail_level, "frontend")
            from ..agents.prompts import get_frontend_prompt
            frontend_prompt = get_frontend_prompt(
                requirements.model_dump_json(indent=2),
                api_design.model_dump_json(indent=2),
                frontend_config,
            )
            frontend_result = await frontend_agent.run(frontend_prompt)
            frontend_design = frontend_result.output

            frontend_summary = f"""
**Framework**: {frontend_design.framework}

**Components**: {len(frontend_design.components)}

**State Management**: {frontend_design.state_management.value} ({frontend_design.state_management_library or 'built-in'})

**Styling**: {frontend_design.styling_approach}

**Key Components**: {', '.join([c.name for c in frontend_design.components[:5]])}

**Design Rationale**: {frontend_design.reasoning}
"""

            yield self.streaming_handler.create_update(
                phase="Frontend Architecture",
                reasoning=frontend_summary,
                diagram=frontend_design.mermaid_diagram,
                data=frontend_design,
                status="completed",
            )

            # Phase 5: Deployment Plan
            yield self.streaming_handler.create_update(
                phase="Deployment Plan",
                reasoning=f"Creating infrastructure and deployment plan for {user_input.deployment_platform.value.upper()}...",
                status="in_progress",
            )

            # Create deployment agent with selected provider
            deployment_agent = create_deployment_agent(self.provider, self.model_name)
            deployment_config = get_component_config(detail_level, "deployment")
            from ..agents.prompts import get_deployment_prompt
            deployment_prompt = get_deployment_prompt(
                requirements.model_dump_json(indent=2),
                database_schema.model_dump_json(indent=2),
                api_design.model_dump_json(indent=2),
                frontend_design.model_dump_json(indent=2),
                user_input.deployment_platform.value,
                deployment_config,
            )
            deployment_result = await deployment_agent.run(deployment_prompt)
            deployment_plan = deployment_result.output

            deployment_summary = f"""
**Platform**: {deployment_plan.platform}

**Database Service**: {deployment_plan.database_service}

**Hosting Service**: {deployment_plan.hosting_service}

**CI/CD**: {deployment_plan.ci_cd_strategy}

**Monitoring**: {deployment_plan.monitoring_strategy}

**Estimated Cost**: {deployment_plan.estimated_monthly_cost or 'TBD'}

**Design Rationale**: {deployment_plan.reasoning}
"""

            yield self.streaming_handler.create_update(
                phase="Deployment Plan",
                reasoning=deployment_summary,
                diagram=deployment_plan.mermaid_diagram,
                data=deployment_plan,
                status="completed",
            )

            # Build Complete Blueprint
            blueprint = TechnicalBlueprint(
                user_input=user_input,
                requirements=requirements,
                database_schema=database_schema,
                api_design=api_design,
                frontend_design=frontend_design,
                deployment_plan=deployment_plan,
                full_architecture_diagram=self.diagram_builder.build_full_architecture_diagram(
                    TechnicalBlueprint(
                        user_input=user_input,
                        requirements=requirements,
                        database_schema=database_schema,
                        api_design=api_design,
                        frontend_design=frontend_design,
                        deployment_plan=deployment_plan,
                        full_architecture_diagram="",  # Temporary
                        implementation_recommendations=[
                            "Start with MVP features to validate core functionality",
                            "Implement authentication and user management first",
                            "Set up CI/CD pipeline early in the development process",
                            "Use feature flags for gradual rollout of new features",
                            "Implement comprehensive logging and monitoring from day one",
                        ],
                        next_steps=[
                            "Set up development environment and version control",
                            "Initialize project with chosen technology stack",
                            "Implement database schema and migrations",
                            "Build authentication system",
                            "Develop core API endpoints",
                            "Create basic frontend components",
                            "Set up deployment pipeline",
                            "Configure monitoring and logging",
                        ],
                        estimated_timeline=self._estimate_timeline(requirements.complexity_assessment),
                        technology_stack_summary={
                            "frontend": frontend_design.framework,
                            "backend": "Node.js/Python (to be determined)",
                            "database": deployment_plan.database_service,
                            "hosting": deployment_plan.platform,
                            "monitoring": ", ".join(deployment_plan.monitoring_tools[:2])
                            if deployment_plan.monitoring_tools
                            else "TBD",
                        },
                    )
                ),
                implementation_recommendations=[
                    "Start with MVP features to validate core functionality",
                    "Implement authentication and user management first",
                    "Set up CI/CD pipeline early in the development process",
                    "Use feature flags for gradual rollout of new features",
                    "Implement comprehensive logging and monitoring from day one",
                ],
                next_steps=[
                    "Set up development environment and version control",
                    "Initialize project with chosen technology stack",
                    "Implement database schema and migrations",
                    "Build authentication system",
                    "Develop core API endpoints",
                    "Create basic frontend components",
                    "Set up deployment pipeline",
                    "Configure monitoring and logging",
                ],
                estimated_timeline=self._estimate_timeline(requirements.complexity_assessment),
                technology_stack_summary={
                    "frontend": frontend_design.framework,
                    "backend": "Node.js/Python (to be determined)",
                    "database": deployment_plan.database_service,
                    "hosting": deployment_plan.platform,
                    "monitoring": ", ".join(deployment_plan.monitoring_tools[:2])
                    if deployment_plan.monitoring_tools
                    else "TBD",
                },
            )

            # Final update with complete blueprint
            yield self.streaming_handler.create_update(
                phase="Complete",
                reasoning="Blueprint generation complete! Your technical architecture is ready.",
                data=blueprint,
                status="completed",
            )

        except Exception as e:
            # Enhanced error handling with provider information
            yield self.streaming_handler.create_update(
                phase="Error",
                reasoning=f"An error occurred with {self.provider.value.upper()} provider: {str(e)}",
                status="error",
            )
            raise

    def _estimate_timeline(self, complexity: str) -> str:
        """Estimate implementation timeline based on complexity."""
        timelines = {
            "low": "6-8 weeks for MVP",
            "medium": "3-4 months for MVP",
            "high": "4-6 months for MVP",
        }
        return timelines.get(complexity.lower(), "3-4 months for MVP")

    async def generate_blueprint(self, user_input: UserInput) -> TechnicalBlueprint:
        """
        Generate a complete blueprint without streaming (for batch processing).

        Args:
            user_input: User's business idea and preferences

        Returns:
            Complete TechnicalBlueprint
        """
        blueprint = None
        async for update in self.generate_blueprint_stream(user_input):
            if update.status == "completed" and update.phase == "Complete":
                blueprint = update.data

        if blueprint is None:
            raise Exception("Blueprint generation failed")

        return blueprint
