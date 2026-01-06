"""
Deployment plan models for blueprint generation.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class InfrastructureComponent(BaseModel):
    """Represents a single infrastructure component."""
    name: str = Field(..., description="Component name/identifier")
    service: str = Field(
        ...,
        description="Cloud service used (e.g., 'EC2', 'Cloud Run', 'App Service')"
    )
    purpose: str = Field(..., description="Purpose of this component")
    configuration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration details and specifications"
    )
    estimated_cost: Optional[str] = Field(
        None,
        description="Estimated monthly cost range"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "name": "web_server",
                "service": "AWS EC2 t3.small",
                "purpose": "Application server hosting",
                "configuration": {
                    "instance_type": "t3.small",
                    "os": "Ubuntu 22.04 LTS",
                    "auto_scaling": True,
                    "min_instances": 2,
                    "max_instances": 10
                },
                "estimated_cost": "$15-50/month"
            }
        }


class DeploymentPlan(BaseModel):
    """Complete deployment plan for the application."""
    platform: str = Field(..., description="Primary deployment platform")
    infrastructure: List[InfrastructureComponent] = Field(
        ...,
        min_length=1,
        description="Infrastructure components"
    )
    database_service: str = Field(
        ...,
        description="Database service/product (e.g., 'AWS RDS PostgreSQL', 'Cloud SQL')"
    )
    database_configuration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Database configuration details"
    )
    hosting_service: str = Field(
        ...,
        description="Application hosting service (e.g., 'AWS ECS', 'Google Cloud Run')"
    )
    hosting_configuration: Dict[str, Any] = Field(
        default_factory=dict,
        description="Hosting configuration details"
    )
    ci_cd_strategy: str = Field(
        ...,
        description="CI/CD pipeline approach and tools"
    )
    monitoring_strategy: str = Field(
        ...,
        description="Monitoring, logging, and observability approach"
    )
    monitoring_tools: List[str] = Field(
        default_factory=list,
        description="Monitoring and logging tools (e.g., ['CloudWatch', 'Datadog'])"
    )
    scaling_strategy: str = Field(
        ...,
        description="Horizontal and vertical scaling approach"
    )
    security_measures: List[str] = Field(
        ...,
        min_length=1,
        description="Security best practices and implementations"
    )
    backup_strategy: Optional[str] = Field(
        None,
        description="Backup and disaster recovery strategy"
    )
    estimated_monthly_cost: Optional[str] = Field(
        None,
        description="Total estimated monthly cost range"
    )
    deployment_steps: List[str] = Field(
        default_factory=list,
        description="High-level deployment steps"
    )
    reasoning: str = Field(
        ...,
        description="Design rationale and key decisions"
    )
    mermaid_diagram: str = Field(
        ...,
        description="Mermaid diagram showing deployment architecture"
    )

    class Config:
        """Pydantic configuration."""
        json_schema_extra = {
            "example": {
                "platform": "AWS",
                "infrastructure": [],
                "database_service": "AWS RDS PostgreSQL",
                "database_configuration": {
                    "instance_class": "db.t3.small",
                    "storage": "100GB",
                    "multi_az": True
                },
                "hosting_service": "AWS ECS with Fargate",
                "hosting_configuration": {
                    "cpu": "1 vCPU",
                    "memory": "2GB",
                    "auto_scaling": True
                },
                "ci_cd_strategy": "GitHub Actions with automated testing and deployment",
                "monitoring_strategy": "Comprehensive monitoring with CloudWatch and application-level tracking",
                "monitoring_tools": ["AWS CloudWatch", "AWS X-Ray"],
                "scaling_strategy": "Auto-scaling based on CPU and memory utilization",
                "security_measures": [
                    "VPC with private subnets",
                    "Security groups with least privilege",
                    "Secrets Manager for credentials"
                ],
                "backup_strategy": "Automated daily backups with 7-day retention",
                "estimated_monthly_cost": "$100-300/month",
                "deployment_steps": [
                    "Set up VPC and networking",
                    "Configure RDS instance",
                    "Deploy application to ECS",
                    "Set up CI/CD pipeline"
                ],
                "reasoning": "AWS chosen for comprehensive service ecosystem and ease of scaling",
                "mermaid_diagram": "graph TB\\n    Internet --> ALB\\n    ALB --> ECS"
            }
        }
