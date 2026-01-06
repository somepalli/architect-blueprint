"""
Database schema models for blueprint generation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class DataType(str, Enum):
    """Database field data types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    TEXT = "text"
    JSON = "json"
    UUID = "uuid"
    BINARY = "binary"


class FieldConstraint(str, Enum):
    """Database field constraints."""
    PRIMARY_KEY = "primary_key"
    FOREIGN_KEY = "foreign_key"
    UNIQUE = "unique"
    NOT_NULL = "not_null"
    INDEXED = "indexed"
    AUTO_INCREMENT = "auto_increment"


class DatabaseField(BaseModel):
    """Represents a single field in a database table."""
    name: str = Field(..., description="Field name")
    data_type: DataType = Field(..., description="Data type")
    constraints: List[FieldConstraint] = Field(
        default_factory=list,
        description="Field constraints"
    )
    foreign_key_reference: Optional[str] = Field(
        None,
        description="Referenced table.field for foreign keys (e.g., 'users.id')"
    )
    description: str = Field(..., description="Field purpose and usage")
    default_value: Optional[str] = Field(
        None,
        description="Default value for the field"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "user_id",
                "data_type": "uuid",
                "constraints": ["foreign_key", "not_null", "indexed"],
                "foreign_key_reference": "users.id",
                "description": "Reference to the user who created this record"
            }
        }


class DatabaseTable(BaseModel):
    """Represents a database table."""
    name: str = Field(..., description="Table name")
    fields: List[DatabaseField] = Field(
        ...,
        min_length=1,
        description="Table fields"
    )
    description: str = Field(..., description="Table purpose and usage")
    indexes: List[str] = Field(
        default_factory=list,
        description="Additional composite indexes (e.g., 'user_id,created_at')"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "users",
                "fields": [
                    {
                        "name": "id",
                        "data_type": "uuid",
                        "constraints": ["primary_key"],
                        "description": "Unique user identifier"
                    },
                    {
                        "name": "email",
                        "data_type": "string",
                        "constraints": ["unique", "not_null"],
                        "description": "User email address"
                    }
                ],
                "description": "Stores user account information",
                "indexes": ["email", "created_at"]
            }
        }


class DatabaseSchema(BaseModel):
    """Complete database schema for the application."""
    tables: List[DatabaseTable] = Field(
        ...,
        min_length=1,
        description="Database tables"
    )
    relationships: List[str] = Field(
        default_factory=list,
        description="Description of table relationships (e.g., 'users has many posts')"
    )
    reasoning: str = Field(
        ...,
        description="Design rationale and key decisions"
    )
    mermaid_diagram: str = Field(
        ...,
        description="Mermaid ER diagram syntax representing the schema"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "tables": [],
                "relationships": [
                    "users has many posts",
                    "users has many comments",
                    "posts has many comments"
                ],
                "reasoning": "Schema designed for a social platform with user-generated content",
                "mermaid_diagram": "erDiagram\\n    USERS ||--o{ POSTS : creates"
            }
        }
