"""
API design models for blueprint generation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


class HTTPMethod(str, Enum):
    """HTTP methods for API endpoints."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


class AuthType(str, Enum):
    """Authentication types for API endpoints."""
    NONE = "none"
    JWT = "jwt"
    OAUTH2 = "oauth2"
    API_KEY = "api_key"
    SESSION = "session"
    BASIC = "basic"


class APIParameter(BaseModel):
    """Represents a single API parameter."""
    name: str = Field(..., description="Parameter name")
    param_type: str = Field(
        ...,
        description="Parameter type: path, query, body, header"
    )
    data_type: str = Field(..., description="Data type of the parameter")
    required: bool = Field(default=True, description="Whether the parameter is required")
    description: str = Field(..., description="Parameter description")
    example: Optional[str] = Field(None, description="Example value")

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "user_id",
                "param_type": "path",
                "data_type": "string",
                "required": True,
                "description": "Unique identifier of the user",
                "example": "123e4567-e89b-12d3-a456-426614174000"
            }
        }


class APIResponse(BaseModel):
    """Represents an API response."""
    status_code: int = Field(..., description="HTTP status code")
    description: str = Field(..., description="Response description")
    schema: Optional[Dict[str, Any]] = Field(
        None,
        description="Response schema/structure"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "status_code": 200,
                "description": "Successfully retrieved user",
                "schema": {
                    "id": "string",
                    "email": "string",
                    "name": "string"
                }
            }
        }


class APIEndpoint(BaseModel):
    """Represents a single API endpoint."""
    path: str = Field(..., description="API endpoint path (e.g., /api/v1/users/{id})")
    method: HTTPMethod = Field(..., description="HTTP method")
    name: str = Field(..., description="Endpoint name/identifier")
    description: str = Field(..., description="Endpoint purpose and functionality")
    auth_required: bool = Field(
        default=True,
        description="Whether authentication is required"
    )
    auth_type: Optional[AuthType] = Field(
        None,
        description="Type of authentication required"
    )
    parameters: List[APIParameter] = Field(
        default_factory=list,
        description="Endpoint parameters"
    )
    responses: List[APIResponse] = Field(
        ...,
        min_length=1,
        description="Possible responses"
    )
    database_operations: List[str] = Field(
        default_factory=list,
        description="Database tables accessed (e.g., ['users', 'posts'])"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "path": "/api/v1/users/{id}",
                "method": "GET",
                "name": "get_user",
                "description": "Retrieve user information by ID",
                "auth_required": True,
                "auth_type": "jwt",
                "parameters": [],
                "responses": [
                    {
                        "status_code": 200,
                        "description": "Successfully retrieved user"
                    }
                ],
                "database_operations": ["users"]
            }
        }


class APIDesign(BaseModel):
    """Complete API design for the application."""
    base_url: str = Field(
        default="/api/v1",
        description="API base URL/prefix"
    )
    endpoints: List[APIEndpoint] = Field(
        ...,
        min_length=1,
        description="API endpoints"
    )
    authentication_strategy: str = Field(
        ...,
        description="Overall authentication strategy and implementation approach"
    )
    rate_limiting: Optional[str] = Field(
        None,
        description="Rate limiting strategy (e.g., '100 requests per minute per user')"
    )
    versioning_strategy: str = Field(
        default="URL path versioning (e.g., /api/v1/)",
        description="API versioning approach"
    )
    reasoning: str = Field(
        ...,
        description="Design rationale and key decisions"
    )
    mermaid_diagram: str = Field(
        ...,
        description="Mermaid sequence diagram showing API flows"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "base_url": "/api/v1",
                "endpoints": [],
                "authentication_strategy": "JWT-based authentication with refresh tokens",
                "rate_limiting": "100 requests per minute per authenticated user",
                "versioning_strategy": "URL path versioning (e.g., /api/v1/)",
                "reasoning": "RESTful API design prioritizing security and scalability",
                "mermaid_diagram": "sequenceDiagram\\n    Client->>API: POST /login"
            }
        }
