"""
Configuration for different blueprint detail levels.
"""
from typing import Dict, Any


DETAIL_LEVEL_CONFIGS: Dict[str, Dict[str, Any]] = {
    "high_level": {
        "description": "High-level overview with key components",
        "database": {
            "max_tables": 10,  # Minimum 5-10 core tables
            "include_indexes": False,
            "include_constraints": "primary_key_only",
            "field_descriptions": "brief",
        },
        "api": {
            "max_endpoints": 10,
            "include_request_body_schema": False,
            "include_error_responses": False,
            "include_parameters": "path_only",
        },
        "frontend": {
            "max_components": 8,
            "component_detail": "high_level",
            "include_props": False,
            "include_state": False,
            "include_dependencies": False,
        },
        "deployment": {
            "detail": "minimal",
            "include_cost_estimate": False,
            "include_security_measures": "basic",
            "include_monitoring": "basic",
        },
    },
    "detailed": {
        "description": "Detailed specification with comprehensive information",
        "database": {
            "max_tables": 20,  # Comprehensive: 15-20 tables covering all features
            "include_indexes": True,
            "include_constraints": "all",
            "field_descriptions": "detailed",
        },
        "api": {
            "max_endpoints": 30,
            "include_request_body_schema": True,
            "include_error_responses": True,
            "include_parameters": "all",
        },
        "frontend": {
            "max_components": 20,
            "component_detail": "detailed",
            "include_props": True,
            "include_state": True,
            "include_dependencies": True,
        },
        "deployment": {
            "detail": "detailed",
            "include_cost_estimate": True,
            "include_security_measures": "comprehensive",
            "include_monitoring": "detailed",
        },
    },
    "production_ready": {
        "description": "Production-ready with security, monitoring, and scalability",
        "database": {
            "max_tables": 30,  # Enterprise-grade: 25-30+ tables with all supporting features
            "include_indexes": True,
            "include_constraints": "all",
            "field_descriptions": "comprehensive",
            "include_partitioning": True,
            "include_replication": True,
        },
        "api": {
            "max_endpoints": 50,
            "include_request_body_schema": True,
            "include_error_responses": True,
            "include_parameters": "all",
            "include_rate_limiting": True,
            "include_caching_strategy": True,
            "include_versioning": True,
        },
        "frontend": {
            "max_components": 35,
            "component_detail": "comprehensive",
            "include_props": True,
            "include_state": True,
            "include_dependencies": True,
            "include_performance_optimization": True,
            "include_error_boundaries": True,
            "include_testing_strategy": True,
        },
        "deployment": {
            "detail": "production_grade",
            "include_cost_estimate": True,
            "include_security_measures": "enterprise",
            "include_monitoring": "comprehensive",
            "include_disaster_recovery": True,
            "include_compliance": True,
            "include_scalability_plan": True,
            "include_ci_cd_pipeline": True,
        },
    },
}


def get_detail_config(detail_level: str) -> Dict[str, Any]:
    """
    Get configuration for a specific detail level.

    Args:
        detail_level: Detail level identifier (high_level, detailed, production_ready)

    Returns:
        Configuration dictionary for the specified detail level

    Raises:
        ValueError: If detail level is not recognized
    """
    if detail_level not in DETAIL_LEVEL_CONFIGS:
        raise ValueError(
            f"Unknown detail level: {detail_level}. "
            f"Must be one of {list(DETAIL_LEVEL_CONFIGS.keys())}"
        )
    return DETAIL_LEVEL_CONFIGS[detail_level]


def get_component_config(detail_level: str, component: str) -> Dict[str, Any]:
    """
    Get configuration for a specific component at a given detail level.

    Args:
        detail_level: Detail level identifier
        component: Component name (database, api, frontend, deployment)

    Returns:
        Configuration dictionary for the component

    Raises:
        ValueError: If detail level or component is not recognized
    """
    config = get_detail_config(detail_level)
    if component not in config:
        raise ValueError(
            f"Unknown component: {component}. "
            f"Must be one of {list(config.keys())}"
        )
    return config[component]
