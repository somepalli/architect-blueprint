"""
Main layout component for the Streamlit application.
"""
import streamlit as st
from typing import Optional
from ..models.blueprint_models import TechnicalBlueprint
from .reasoning_panel import render_reasoning_panel, render_completion_state, render_loading_state
from .diagram_panel import render_diagram_tabs
from .export_panel import render_export_panel


def render_two_panel_layout(
    blueprint: Optional[TechnicalBlueprint] = None,
    is_generating: bool = False,
    current_phase: str = "",
    reasoning_text: str = "",
    progress: float = 0.0,
    phase_timeline: str = "",
    db_diagram: Optional[str] = None,
    api_diagram: Optional[str] = None,
    frontend_diagram: Optional[str] = None,
    deployment_diagram: Optional[str] = None,
):
    """
    Render the main two-panel layout with reasoning and diagrams.

    Args:
        blueprint: Complete blueprint (if generation is done)
        is_generating: Whether blueprint is currently being generated
        current_phase: Current phase name
        reasoning_text: Agent reasoning text
        progress: Progress percentage
        phase_timeline: Phase timeline string
        db_diagram: Database diagram
        api_diagram: API diagram
        frontend_diagram: Frontend diagram
        deployment_diagram: Deployment diagram
    """
    # Create two columns for the layout
    col_reasoning, col_diagrams = st.columns([4, 6])

    # Left Panel: Agent Reasoning
    with col_reasoning:
        st.markdown("## 🤖 Agent Reasoning")

        if blueprint:
            # Generation complete
            render_completion_state(blueprint)
        elif is_generating:
            # Currently generating
            render_reasoning_panel(
                current_phase=current_phase,
                reasoning_text=reasoning_text,
                progress=progress,
                phase_timeline=phase_timeline,
            )
        else:
            # Initial state
            st.info("Fill out the form above and click 'Generate Blueprint' to get started!")
            st.markdown("""
            ### What to Expect:

            1. **Requirements Analysis** - AI analyzes your idea
            2. **Database Design** - Schema with ER diagram
            3. **API Design** - RESTful endpoints
            4. **Frontend Architecture** - Component structure
            5. **Deployment Plan** - Infrastructure design

            **Estimated Time**: 2-5 minutes
            """)

    # Right Panel: Architecture Diagrams
    with col_diagrams:
        st.markdown("## 🏗️ Architecture Diagrams")

        if blueprint:
            # Show all diagrams
            render_diagram_tabs(
                db_diagram=blueprint.database_schema.mermaid_diagram,
                api_diagram=blueprint.api_design.mermaid_diagram,
                frontend_diagram=blueprint.frontend_design.mermaid_diagram,
                deployment_diagram=blueprint.deployment_plan.mermaid_diagram,
                full_diagram=blueprint.full_architecture_diagram,
            )
        elif is_generating:
            # Show diagrams as they're generated
            render_diagram_tabs(
                db_diagram=db_diagram,
                api_diagram=api_diagram,
                frontend_diagram=frontend_diagram,
                deployment_diagram=deployment_diagram,
                full_diagram=None,  # Only available when complete
            )
        else:
            # Initial state
            st.info("Diagrams will appear here as the blueprint is generated")
            st.markdown("""
            You'll see live updates for:
            - 📊 **Database Schema** (ER Diagram)
            - 🔌 **API Endpoints** (Sequence Diagram)
            - 🎨 **Frontend Components** (Component Hierarchy)
            - 🚀 **Deployment** (Infrastructure Diagram)
            - 🏗️ **Full Architecture** (System Overview)
            """)


def render_export_section(blueprint: Optional[TechnicalBlueprint] = None):
    """
    Render the export section below the main layout.

    Args:
        blueprint: Complete blueprint to export
    """
    st.markdown("---")
    render_export_panel(blueprint)
