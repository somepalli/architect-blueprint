"""
Export functionality component for Streamlit.
"""
import streamlit as st
import json
from typing import Optional
from ..models.blueprint_models import TechnicalBlueprint


def render_export_panel(blueprint: Optional[TechnicalBlueprint] = None):
    """
    Render export options for the blueprint.

    Args:
        blueprint: Complete TechnicalBlueprint object
    """
    if not blueprint:
        st.info("Generate a blueprint to enable export options")
        return

    st.markdown("### Export Blueprint")

    col1, col2 = st.columns(2)

    with col1:
        # Export as JSON
        json_data = blueprint.model_dump_json(indent=2)
        st.download_button(
            label="📥 Download as JSON",
            data=json_data,
            file_name=f"blueprint_{blueprint.id[:8]}.json",
            mime="application/json",
            use_container_width=True,
        )

    with col2:
        # Export as Markdown
        markdown_data = generate_markdown_export(blueprint)
        st.download_button(
            label="📥 Download as Markdown",
            data=markdown_data,
            file_name=f"blueprint_{blueprint.id[:8]}.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # Copy to clipboard section
    with st.expander("📋 Copy Sections"):
        st.markdown("**Requirements**")
        st.code(
            f"""Core Features: {', '.join(blueprint.requirements.core_features)}
User Types: {', '.join(blueprint.requirements.user_types)}
Key Entities: {', '.join(blueprint.requirements.key_entities)}""",
            language="text",
        )

        st.markdown("**Technology Stack**")
        st.code(json.dumps(blueprint.technology_stack_summary, indent=2), language="json")


def generate_markdown_export(blueprint: TechnicalBlueprint) -> str:
    """
    Generate a comprehensive Markdown document from the blueprint.

    Args:
        blueprint: Complete TechnicalBlueprint object

    Returns:
        Markdown string
    """
    md = f"""# Technical Blueprint

**Generated**: {blueprint.created_at.strftime('%Y-%m-%d %H:%M:%S')} UTC
**Blueprint ID**: {blueprint.id}

---

## Business Idea

{blueprint.user_input.business_idea}

**Detail Level**: {blueprint.user_input.detail_level.value}
**Target Platform**: {blueprint.user_input.deployment_platform.value}

---

## Requirements Analysis

### Core Features
{chr(10).join(f'- {feature}' for feature in blueprint.requirements.core_features)}

### User Types
{chr(10).join(f'- {user_type}' for user_type in blueprint.requirements.user_types)}

### Key Entities
{chr(10).join(f'- {entity}' for entity in blueprint.requirements.key_entities)}

### Business Model
{blueprint.requirements.business_model}

### Complexity Assessment
{blueprint.requirements.complexity_assessment}

---

## Database Schema

### Tables ({len(blueprint.database_schema.tables)} total)

"""

    for table in blueprint.database_schema.tables:
        md += f"\n#### {table.name}\n"
        md += f"{table.description}\n\n"
        md += "| Field | Type | Constraints |\n"
        md += "|-------|------|-------------|\n"
        for field in table.fields:
            constraints = ", ".join([c.value for c in field.constraints])
            md += f"| {field.name} | {field.data_type.value} | {constraints} |\n"
        md += "\n"

    md += f"""
### Database Design Rationale
{blueprint.database_schema.reasoning}

---

## API Design

**Base URL**: {blueprint.api_design.base_url}

**Authentication**: {blueprint.api_design.authentication_strategy}

### Endpoints ({len(blueprint.api_design.endpoints)} total)

"""

    for endpoint in blueprint.api_design.endpoints:
        md += f"\n#### {endpoint.method.value} {endpoint.path}\n"
        md += f"**Name**: {endpoint.name}\n\n"
        md += f"**Description**: {endpoint.description}\n\n"
        md += f"**Auth Required**: {endpoint.auth_required}\n\n"

    md += f"""
### API Design Rationale
{blueprint.api_design.reasoning}

---

## Frontend Architecture

**Framework**: {blueprint.frontend_design.framework}

**State Management**: {blueprint.frontend_design.state_management.value}

**Styling**: {blueprint.frontend_design.styling_approach}

### Components ({len(blueprint.frontend_design.components)} total)

"""

    for component in blueprint.frontend_design.components:
        md += f"\n#### {component.name}\n"
        md += f"**Type**: {component.type.value}\n\n"
        md += f"**Path**: `{component.path}`\n\n"
        md += f"**Description**: {component.description}\n\n"

    md += f"""
### Frontend Design Rationale
{blueprint.frontend_design.reasoning}

---

## Deployment Plan

**Platform**: {blueprint.deployment_plan.platform}

**Database Service**: {blueprint.deployment_plan.database_service}

**Hosting Service**: {blueprint.deployment_plan.hosting_service}

**CI/CD Strategy**: {blueprint.deployment_plan.ci_cd_strategy}

**Monitoring Strategy**: {blueprint.deployment_plan.monitoring_strategy}

**Estimated Monthly Cost**: {blueprint.deployment_plan.estimated_monthly_cost or 'TBD'}

### Security Measures
{chr(10).join(f'- {measure}' for measure in blueprint.deployment_plan.security_measures)}

### Deployment Rationale
{blueprint.deployment_plan.reasoning}

---

## Technology Stack Summary

{chr(10).join(f'- **{key.title()}**: {value}' for key, value in blueprint.technology_stack_summary.items())}

---

## Implementation Recommendations

{chr(10).join(f'{i+1}. {rec}' for i, rec in enumerate(blueprint.implementation_recommendations))}

---

## Next Steps

{chr(10).join(f'{i+1}. {step}' for i, step in enumerate(blueprint.next_steps))}

---

## Estimated Timeline

{blueprint.estimated_timeline}

---

*Generated with Micro-SaaS Architect*
"""

    return md
