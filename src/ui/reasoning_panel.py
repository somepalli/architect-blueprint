"""
Agent reasoning display component for Streamlit.
"""
import streamlit as st
from typing import Optional


def render_reasoning_panel(
    current_phase: str = "Initializing",
    reasoning_text: str = "",
    progress: float = 0.0,
    phase_timeline: str = "",
):
    """
    Render the agent reasoning panel showing current progress.

    Args:
        current_phase: Name of current phase
        reasoning_text: Agent's reasoning/explanation text
        progress: Progress percentage (0-100)
        phase_timeline: Formatted phase timeline string
    """
    # Current Phase
    st.subheader(f"🤖 Current Phase: {current_phase}")

    # Progress Bar
    st.progress(progress / 100.0)
    st.caption(f"Progress: {progress:.0f}%")

    # Phase Timeline
    if phase_timeline:
        st.markdown("### Phase Timeline")
        st.markdown(phase_timeline)

    # Reasoning Text
    if reasoning_text:
        st.markdown("### Agent Reasoning")
        st.markdown(reasoning_text)


def render_loading_state():
    """Render a loading state for the reasoning panel."""
    st.subheader("🤖 Generating Blueprint...")
    st.info("The AI agents are analyzing your idea and designing the architecture. This may take 2-5 minutes.")

    with st.spinner("Working..."):
        st.markdown("""
        **What's Happening:**
        1. Analyzing business requirements
        2. Designing database schema
        3. Creating API endpoints
        4. Planning frontend architecture
        5. Designing deployment infrastructure
        """)


def render_completion_state(blueprint):
    """
    Render completion state with summary.

    Args:
        blueprint: Complete TechnicalBlueprint object
    """
    st.success("✅ Blueprint Generation Complete!")

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Database Tables", len(blueprint.database_schema.tables))

    with col2:
        st.metric("API Endpoints", len(blueprint.api_design.endpoints))

    with col3:
        st.metric("Frontend Components", len(blueprint.frontend_design.components))

    with col4:
        st.metric("Infrastructure Components", len(blueprint.deployment_plan.infrastructure))

    # Technology Stack Summary
    st.markdown("### Technology Stack")
    tech_stack = blueprint.technology_stack_summary
    cols = st.columns(len(tech_stack))
    for idx, (key, value) in enumerate(tech_stack.items()):
        with cols[idx]:
            st.markdown(f"**{key.title()}**")
            st.write(value)

    # Implementation Recommendations
    with st.expander("💡 Implementation Recommendations", expanded=True):
        for rec in blueprint.implementation_recommendations:
            st.markdown(f"- {rec}")

    # Next Steps
    with st.expander("📋 Next Steps"):
        for step in blueprint.next_steps:
            st.markdown(f"- {step}")

    # Timeline
    if blueprint.estimated_timeline:
        st.info(f"⏱️ Estimated Timeline: **{blueprint.estimated_timeline}**")
