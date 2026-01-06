"""
Frontend component models for blueprint generation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum


class ComponentType(str, Enum):
    """Types of frontend components."""
    PAGE = "page"
    LAYOUT = "layout"
    FEATURE = "feature"
    UI = "ui"
    UTILITY = "utility"
    HOOK = "hook"


class StateManagement(str, Enum):
    """State management approaches."""
    LOCAL = "local"
    CONTEXT = "context"
    GLOBAL_STORE = "global_store"
    SERVER = "server"
    PROPS = "props"


class ComponentDependency(BaseModel):
    """Represents a dependency between components."""
    component_name: str = Field(..., description="Name of the dependent component")
    dependency_type: str = Field(
        ...,
        description="Type of dependency: uses, contains, calls, imports"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "component_name": "Button",
                "dependency_type": "uses"
            }
        }


class FrontendComponent(BaseModel):
    """Represents a single frontend component."""
    name: str = Field(..., description="Component name")
    type: ComponentType = Field(..., description="Component type/category")
    path: str = Field(
        ...,
        description="File path relative to src (e.g., 'components/Button.tsx')"
    )
    description: str = Field(..., description="Component purpose and functionality")
    props: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Component props (e.g., [{'name': 'onClick', 'type': 'function'}])"
    )
    state: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Component state (e.g., [{'name': 'isOpen', 'type': 'boolean'}])"
    )
    api_calls: List[str] = Field(
        default_factory=list,
        description="API endpoints called by this component"
    )
    dependencies: List[ComponentDependency] = Field(
        default_factory=list,
        description="Component dependencies"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "UserProfile",
                "type": "page",
                "path": "pages/UserProfile.tsx",
                "description": "Displays and manages user profile information",
                "props": [
                    {"name": "userId", "type": "string"}
                ],
                "state": [
                    {"name": "isEditing", "type": "boolean"},
                    {"name": "userData", "type": "User"}
                ],
                "api_calls": ["/api/v1/users/{id}", "/api/v1/users/{id}"],
                "dependencies": [
                    {"component_name": "Button", "dependency_type": "uses"}
                ]
            }
        }


class FrontendDesign(BaseModel):
    """Complete frontend design for the application."""
    framework: str = Field(
        ...,
        description="Frontend framework (e.g., React, Vue, Svelte, Next.js)"
    )
    components: List[FrontendComponent] = Field(
        ...,
        min_length=1,
        description="Frontend components"
    )
    routing_structure: List[Dict[str, str]] = Field(
        default_factory=list,
        description="Route definitions (e.g., [{'path': '/users/:id', 'component': 'UserProfile'}])"
    )
    state_management: StateManagement = Field(
        ...,
        description="Primary state management approach"
    )
    state_management_library: Optional[str] = Field(
        None,
        description="State management library (e.g., Redux, Zustand, Jotai)"
    )
    styling_approach: str = Field(
        ...,
        description="Styling solution (e.g., Tailwind CSS, CSS Modules, styled-components)"
    )
    key_libraries: List[str] = Field(
        default_factory=list,
        description="Key third-party libraries used (e.g., ['react-query', 'axios'])"
    )
    reasoning: str = Field(
        ...,
        description="Design rationale and key decisions"
    )
    mermaid_diagram: str = Field(
        ...,
        description="Mermaid flowchart/graph showing component hierarchy"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "framework": "React with Next.js",
                "components": [],
                "routing_structure": [
                    {"path": "/", "component": "Home"},
                    {"path": "/users/:id", "component": "UserProfile"}
                ],
                "state_management": "global_store",
                "state_management_library": "Zustand",
                "styling_approach": "Tailwind CSS",
                "key_libraries": ["react-query", "axios", "zod"],
                "reasoning": "Modern React stack prioritizing developer experience and performance",
                "mermaid_diagram": "graph TD\\n    App --> Home\\n    App --> UserProfile"
            }
        }
