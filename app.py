"""
Micro-SaaS Architect - Main Streamlit Application

An AI-powered application that generates comprehensive technical blueprints
for SaaS applications with real-time visualization.
"""
import streamlit as st
import asyncio
from typing import Optional

from src.models.input_models import UserInput
from src.models.blueprint_models import TechnicalBlueprint
from src.services.blueprint_generator import BlueprintGenerator
from src.ui.input_form import render_input_form, show_detail_level_info
from src.ui.layout import render_two_panel_layout, render_export_section


# Page configuration
st.set_page_config(
    page_title="Micro-SaaS Architect",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    h1 {
        color: #1f77b4;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if "blueprint" not in st.session_state:
    st.session_state.blueprint = None
if "is_generating" not in st.session_state:
    st.session_state.is_generating = False
if "current_phase" not in st.session_state:
    st.session_state.current_phase = ""
if "reasoning_text" not in st.session_state:
    st.session_state.reasoning_text = ""
if "progress" not in st.session_state:
    st.session_state.progress = 0.0
if "phase_timeline" not in st.session_state:
    st.session_state.phase_timeline = ""
if "diagrams" not in st.session_state:
    st.session_state.diagrams = {
        "db": None,
        "api": None,
        "frontend": None,
        "deployment": None,
    }


def generate_blueprint_with_progress(user_input: UserInput, status_container, progress_container):
    """
    Generate blueprint with real-time progress updates.

    Args:
        user_input: User's business idea and preferences
        status_container: Streamlit container for status messages
        progress_container: Streamlit container for progress bar
    """
    import asyncio

    # Get provider from session state (set by input form)
    provider = st.session_state.get("selected_provider", None)
    model_name = st.session_state.get("selected_model", None)

    # Create generator with selected provider
    generator = BlueprintGenerator(provider=provider, model_name=model_name)
    progress_bar = progress_container.progress(0.0)

    # Show which provider is being used
    if provider:
        provider_display = {
            "groq": "Groq - FREE & Ultra Fast",
            "openai": "OpenAI GPT-4",
            "deepseek": "DeepSeek (97% cheaper!)",
            "kimi": "Kimi K2",
        }
        provider_name = provider_display.get(provider.value, provider.value.upper())
        status_container.info(f"🤖 Using: {provider_name}")

    async def run_generation():
        """Inner async function to run generation."""
        try:
            async for update in generator.generate_blueprint_stream(user_input):
                # Update progress bar (convert 0-100 to 0.0-1.0)
                progress_value = min(1.0, max(0.0, update.progress / 100.0))
                progress_bar.progress(progress_value)

                # Update status message
                status_container.write(f"**{update.phase}**: {update.reasoning[:150]}...")

                # Update session state
                st.session_state.current_phase = update.phase
                st.session_state.reasoning_text = update.reasoning
                st.session_state.progress = update.progress
                st.session_state.phase_timeline = generator.streaming_handler.get_phase_timeline()

                # Update diagrams as they're generated
                if update.diagram:
                    phase_lower = update.phase.lower()
                    if "database" in phase_lower:
                        st.session_state.diagrams["db"] = update.diagram
                    elif "api" in phase_lower:
                        st.session_state.diagrams["api"] = update.diagram
                    elif "frontend" in phase_lower:
                        st.session_state.diagrams["frontend"] = update.diagram
                    elif "deployment" in phase_lower:
                        st.session_state.diagrams["deployment"] = update.diagram

                # Check if generation is complete
                if update.status == "completed" and update.phase == "Complete":
                    st.session_state.blueprint = update.data
                    st.session_state.is_generating = False
                    progress_bar.progress(1.0)
                    status_container.success("✅ Blueprint generation complete!")

        except Exception as e:
            st.session_state.is_generating = False
            st.session_state.current_phase = "Error"
            st.session_state.reasoning_text = f"Error: {str(e)}"
            import traceback
            st.session_state.error_details = traceback.format_exc()
            status_container.error(f"❌ Error: {str(e)}")

    # Run the async generator (blocks until complete)
    asyncio.run(run_generation())

    # Mark as not generating when done
    st.session_state.is_generating = False


def main():
    """Main application entry point."""

    # Header with info
    col1, col2 = st.columns([3, 1])
    with col1:
        pass  # Title is in the form
    with col2:
        show_detail_level_info()

    # Input Form
    user_input = render_input_form()

    # Handle form submission
    if user_input and not st.session_state.is_generating:
        # Reset state for new generation
        st.session_state.blueprint = None
        st.session_state.is_generating = True
        st.session_state.current_phase = "Initializing"
        st.session_state.reasoning_text = "Starting blueprint generation..."
        st.session_state.progress = 0.0
        st.session_state.diagrams = {
            "db": None,
            "api": None,
            "frontend": None,
            "deployment": None,
        }

        # Create containers for real-time updates
        st.markdown("### 🔄 Generating Your Blueprint")
        status_container = st.empty()
        progress_container = st.empty()

        # Start async generation with real-time progress
        generate_blueprint_with_progress(user_input, status_container, progress_container)

        # Rerun to show completed blueprint
        st.rerun()

    # Show errors if any
    if "error_details" in st.session_state and st.session_state.error_details:
        st.error("An error occurred during blueprint generation:")
        with st.expander("Error Details"):
            st.code(st.session_state.error_details)

    # Separator
    st.markdown("---")

    # Two-Panel Layout
    render_two_panel_layout(
        blueprint=st.session_state.blueprint,
        is_generating=st.session_state.is_generating,
        current_phase=st.session_state.current_phase,
        reasoning_text=st.session_state.reasoning_text,
        progress=st.session_state.progress,
        phase_timeline=st.session_state.phase_timeline,
        db_diagram=st.session_state.diagrams["db"],
        api_diagram=st.session_state.diagrams["api"],
        frontend_diagram=st.session_state.diagrams["frontend"],
        deployment_diagram=st.session_state.diagrams["deployment"],
    )

    # Export Section (only show if blueprint is complete)
    if st.session_state.blueprint:
        render_export_section(st.session_state.blueprint)

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Built with <a href='https://github.com/pydantic/pydantic-ai'>PydanticAI</a> and
        <a href='https://streamlit.io'>Streamlit</a></p>
        <p>🤖 Multi-Provider Support: Groq, OpenAI, DeepSeek, Kimi | 🎨 Visualized with Mermaid.js</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
