"""
User input form component for Streamlit.
"""
import streamlit as st
from ..models.input_models import UserInput, DetailLevel, DeploymentPlatform
from ..config.model_providers import (
    ProviderType,
    get_available_providers,
    get_available_models,
    get_provider_config,
    estimate_cost,
)


def render_input_form() -> UserInput | None:
    """
    Render the user input form.

    Returns:
        UserInput object if form is submitted, None otherwise
    """
    st.header("Micro-SaaS Architect")
    st.markdown("Transform your business idea into a comprehensive technical blueprint")

    # === LLM Provider Selection (OUTSIDE FORM for interactivity) ===
    st.markdown("### AI Model Selection")

    provider_col1, provider_col2 = st.columns([1, 1])

    with provider_col1:
        # Provider dropdown with cost indicators
        provider_options = {
            "deepseek": "💎 DeepSeek (Recommended - 97% cheaper)",
            "openai": "OpenAI GPT-4 (Premium quality)",
            "groq": "⚠️ Groq (Compatibility issues)",
            "kimi": "Kimi K2 (60% cheaper)",
        }

        selected_provider_str = st.selectbox(
            "LLM Provider",
            options=list(provider_options.keys()),
            format_func=lambda x: provider_options[x],
            index=0,  # DeepSeek by default (works reliably + cheap)
            help="DeepSeek recommended: 97% cheaper than OpenAI with excellent quality. Groq has known compatibility issues with PydanticAI.",
        )

        selected_provider = ProviderType(selected_provider_str)

    with provider_col2:
        # Model dropdown (changes based on provider)
        available_models = get_available_models(selected_provider)
        provider_config = get_provider_config(selected_provider)

        model_display_names = {
            model_name: provider_config.available_models[model_name].display_name
            for model_name in available_models
        }

        selected_model = st.selectbox(
            "Model",
            options=available_models,
            format_func=lambda x: model_display_names[x],
            help="Select the specific model to use",
        )

    # Show cost estimate
    model_config = provider_config.available_models[selected_model]
    estimated_cost = estimate_cost(
        selected_provider,
        selected_model,
        input_tokens=5000,  # Rough estimate for a detailed blueprint
        output_tokens=3000
    )

    # Show compatibility warning for Groq
    if selected_provider == ProviderType.GROQ:
        st.warning(
            "⚠️ **Groq Compatibility Issue**: Groq's API returns `service_tier='on_demand'` which PydanticAI doesn't recognize. "
            "This may cause errors. **Recommend using DeepSeek or OpenAI instead.**"
        )
    else:
        st.info(
            f"💰 **Estimated Cost**: ${estimated_cost:.4f} per blueprint | "
            f"Input: ${model_config.input_cost_per_1m:.2f}/1M tokens | "
            f"Output: ${model_config.output_cost_per_1m:.2f}/1M tokens"
        )

    st.markdown("---")

    # === Main Form (Business Idea and Config) ===
    with st.form("blueprint_form"):
        # Business Idea Input
        business_idea = st.text_area(
            "Describe Your SaaS Idea",
            height=150,
            placeholder="Example: A project management tool for remote teams with real-time collaboration, task tracking, file sharing, and video conferencing integration. Users can create projects, assign tasks, track progress, and communicate with team members.",
            help="Be as specific as possible. Include key features, target users, and any unique aspects of your idea.",
        )

        # Detail Level Selection
        col1, col2 = st.columns(2)

        with col1:
            detail_level = st.selectbox(
                "Detail Level",
                options=[
                    ("High-Level Overview", DetailLevel.HIGH_LEVEL),
                    ("Detailed Specification", DetailLevel.DETAILED),
                    ("Production-Ready", DetailLevel.PRODUCTION_READY),
                ],
                format_func=lambda x: x[0],
                index=1,  # Default to "Detailed"
                help="Choose how comprehensive the blueprint should be",
            )

        with col2:
            deployment_platform = st.selectbox(
                "Deployment Platform",
                options=[
                    ("AWS (Amazon Web Services)", DeploymentPlatform.AWS),
                    ("GCP (Google Cloud Platform)", DeploymentPlatform.GCP),
                    ("Azure (Microsoft Azure)", DeploymentPlatform.AZURE),
                    ("DigitalOcean", DeploymentPlatform.DIGITAL_OCEAN),
                    ("Heroku", DeploymentPlatform.HEROKU),
                    ("Vercel", DeploymentPlatform.VERCEL),
                    ("Render", DeploymentPlatform.RENDER),
                    ("Railway", DeploymentPlatform.RAILWAY),
                    ("Fly.io", DeploymentPlatform.FLY_IO),
                ],
                format_func=lambda x: x[0],
                index=0,  # Default to AWS
                help="Choose your preferred cloud platform for deployment",
            )

        # Submit Button
        submitted = st.form_submit_button(
            "Generate Blueprint",
            type="primary",
            use_container_width=True,
        )

        if submitted:
            # Validate inputs
            if not business_idea or len(business_idea.strip()) < 10:
                st.error("Please provide a detailed description of your SaaS idea (at least 10 characters)")
                return None

            # Store provider selection in session state
            st.session_state.selected_provider = selected_provider
            st.session_state.selected_model = selected_model

            # Create UserInput object
            user_input = UserInput(
                business_idea=business_idea.strip(),
                detail_level=detail_level[1],  # Extract enum value
                deployment_platform=deployment_platform[1],  # Extract enum value
            )

            return user_input

    return None


def show_detail_level_info():
    """Display information about detail levels."""
    with st.expander("ℹ️ About Detail Levels"):
        st.markdown("""
        ### High-Level Overview
        - Core components and architecture
        - 5-10 main database tables
        - 10-15 key API endpoints
        - Basic frontend structure
        - Simple deployment plan
        - **Best for:** Quick conceptual overview

        ### Detailed Specification
        - Comprehensive component design
        - 15-20 database tables with full schemas
        - 30+ API endpoints with request/response details
        - Detailed frontend component hierarchy
        - Complete deployment architecture with cost estimates
        - **Best for:** Planning and architecture review

        ### Production-Ready
        - Enterprise-grade specifications
        - Full database design with partitioning and replication
        - Extensive API documentation with rate limiting and caching
        - Optimized frontend with performance considerations
        - Production deployment with monitoring, security, and disaster recovery
        - **Best for:** Implementation-ready documentation
        """)
