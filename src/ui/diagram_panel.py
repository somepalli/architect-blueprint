"""
Mermaid diagram rendering component for Streamlit.
"""
import streamlit as st
from typing import Optional


def render_mermaid_diagram(diagram: Optional[str], title: str = "Diagram"):
    """
    Render a Mermaid diagram using HTML.

    Args:
        diagram: Mermaid diagram string
        title: Title for the diagram section
    """
    if not diagram or not diagram.strip():
        st.info("Diagram will appear here once generated...")
        return

    # Clean up diagram string
    diagram = diagram.strip()

    # Remove markdown code fences
    if diagram.startswith("```mermaid"):
        diagram = diagram[len("```mermaid"):].strip()
    elif diagram.startswith("```"):
        diagram = diagram[3:].strip()

    if diagram.endswith("```"):
        diagram = diagram[:-3].strip()

    # Remove any remaining code fence markers from individual lines
    lines = diagram.split("\n")
    cleaned_lines = [line for line in lines if not line.strip() in ["```", "```mermaid"]]
    diagram = "\n".join(cleaned_lines).strip()

    # Show raw diagram for debugging if there's an issue
    with st.expander("🔍 View Raw Diagram Code"):
        st.code(diagram, language="mermaid")

    # Create HTML with Mermaid CDN and error handling
    html_code = f"""
    <div class="mermaid-container">
        <div class="mermaid" id="mermaid-diagram">
{diagram}
        </div>
        <div id="error-container" style="display: none; color: red; padding: 10px; background: #fee; border-radius: 5px; margin-top: 10px;">
            <strong>Diagram Syntax Error:</strong>
            <pre id="error-message"></pre>
        </div>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

        mermaid.initialize({{
            startOnLoad: false,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {{
                useMaxWidth: true,
                htmlLabels: true
            }},
            er: {{
                useMaxWidth: true
            }},
            sequence: {{
                useMaxWidth: true
            }}
        }});

        try {{
            await mermaid.run({{
                nodes: [document.getElementById('mermaid-diagram')]
            }});
        }} catch (error) {{
            console.error('Mermaid error:', error);
            document.getElementById('error-container').style.display = 'block';
            document.getElementById('error-message').textContent = error.message || error.toString();
        }}
    </script>
    <style>
        .mermaid-container {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin: 10px 0;
        }}
        .mermaid {{
            text-align: center;
        }}
    </style>
    """

    st.components.v1.html(html_code, height=650, scrolling=True)


def render_diagram_tabs(
    db_diagram: Optional[str] = None,
    api_diagram: Optional[str] = None,
    frontend_diagram: Optional[str] = None,
    deployment_diagram: Optional[str] = None,
    full_diagram: Optional[str] = None,
):
    """
    Render tabs with different architecture diagrams.

    Args:
        db_diagram: Database ER diagram
        api_diagram: API sequence diagram
        frontend_diagram: Frontend component diagram
        deployment_diagram: Deployment infrastructure diagram
        full_diagram: Full architecture diagram
    """
    tabs = st.tabs([
        "📊 Database Schema",
        "🔌 API Endpoints",
        "🎨 Frontend Components",
        "🚀 Deployment",
        "🏗️ Full Architecture",
    ])

    with tabs[0]:
        st.subheader("Database Schema (ER Diagram)")
        render_mermaid_diagram(db_diagram, "Database Schema")

    with tabs[1]:
        st.subheader("API Design (Sequence Diagram)")
        render_mermaid_diagram(api_diagram, "API Flows")

    with tabs[2]:
        st.subheader("Frontend Architecture (Component Hierarchy)")
        render_mermaid_diagram(frontend_diagram, "Frontend Components")

    with tabs[3]:
        st.subheader("Deployment Architecture (Infrastructure Diagram)")
        render_mermaid_diagram(deployment_diagram, "Deployment Infrastructure")

    with tabs[4]:
        st.subheader("Complete System Architecture")
        render_mermaid_diagram(full_diagram, "Full Architecture")
