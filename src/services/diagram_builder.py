"""
Service for building and validating Mermaid diagrams.
"""
from typing import Optional
from ..models.blueprint_models import TechnicalBlueprint


class DiagramBuilder:
    """Builds and validates Mermaid diagrams from blueprint components."""

    @staticmethod
    def validate_mermaid(diagram: str) -> bool:
        """
        Validate basic Mermaid syntax.

        Args:
            diagram: Mermaid diagram string

        Returns:
            True if diagram appears valid, False otherwise
        """
        if not diagram or not diagram.strip():
            return False

        # Check for basic Mermaid keywords
        diagram_lower = diagram.lower()
        valid_types = [
            "graph",
            "erdiagram",
            "sequencediagram",
            "flowchart",
            "classDiagram",
            "stateDiagram",
        ]

        return any(keyword in diagram_lower for keyword in valid_types)

    @staticmethod
    def build_full_architecture_diagram(blueprint: TechnicalBlueprint) -> str:
        """
        Build a comprehensive architecture diagram combining all layers.

        Args:
            blueprint: Complete technical blueprint

        Returns:
            Mermaid diagram string showing full system architecture
        """
        diagram = """graph TB
    subgraph "Frontend Layer"
        FE["{framework}"]
        FE_STATE["{state_mgmt}"]
    end

    subgraph "API Layer"
        API["{api_base}"]
        AUTH["{auth_strategy}"]
    end

    subgraph "Data Layer"
        DB["{database}"]
    end

    subgraph "Infrastructure"
        DEPLOY["{platform}"]
        MONITOR["{monitoring}"]
    end

    FE --> API
    FE_STATE -.manages.-> FE
    API --> AUTH
    API --> DB
    DEPLOY -.hosts.-> API
    DEPLOY -.hosts.-> FE
    DEPLOY -.hosts.-> DB
    MONITOR -.observes.-> API
    MONITOR -.observes.-> DB

    style FE fill:#e1f5ff
    style API fill:#fff3e0
    style DB fill:#f3e5f5
    style DEPLOY fill:#e8f5e9
"""

        # Fill in the template with actual values
        diagram = diagram.format(
            framework=blueprint.frontend_design.framework,
            state_mgmt=blueprint.frontend_design.state_management.value,
            api_base=blueprint.api_design.base_url,
            auth_strategy=blueprint.api_design.authentication_strategy[:30] + "...",
            database=f"{len(blueprint.database_schema.tables)} tables",
            platform=blueprint.deployment_plan.platform.upper(),
            monitoring=blueprint.deployment_plan.monitoring_strategy[:30] + "...",
        )

        return diagram

    @staticmethod
    def get_diagram_with_fallback(
        diagram: Optional[str], fallback_text: str = "Diagram generation pending..."
    ) -> str:
        """
        Get diagram if valid, otherwise return fallback.

        Args:
            diagram: Mermaid diagram string
            fallback_text: Fallback text if diagram is invalid

        Returns:
            Valid diagram or fallback text
        """
        if diagram and DiagramBuilder.validate_mermaid(diagram):
            return diagram
        return f"```\n{fallback_text}\n```"

    @staticmethod
    def format_for_streamlit(diagram: str) -> str:
        """
        Format Mermaid diagram for Streamlit display.

        Args:
            diagram: Mermaid diagram string

        Returns:
            Formatted diagram string
        """
        # Remove any existing code fence markers
        diagram = diagram.strip()
        if diagram.startswith("```"):
            # Find the end of the opening fence
            first_newline = diagram.find("\n")
            if first_newline != -1:
                diagram = diagram[first_newline + 1 :]
        if diagram.endswith("```"):
            diagram = diagram[:-3]

        return diagram.strip()
