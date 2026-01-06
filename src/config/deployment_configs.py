"""
Platform-specific deployment configurations and service mappings.
"""
from typing import Dict, List, Any


PLATFORM_SERVICES: Dict[str, Dict[str, Any]] = {
    "aws": {
        "name": "Amazon Web Services (AWS)",
        "compute": [
            "EC2 (Elastic Compute Cloud)",
            "ECS (Elastic Container Service)",
            "EKS (Elastic Kubernetes Service)",
            "Lambda (Serverless Functions)",
            "Elastic Beanstalk",
            "App Runner",
        ],
        "database": [
            "RDS (Relational Database Service) - PostgreSQL/MySQL",
            "Aurora (MySQL/PostgreSQL compatible)",
            "DynamoDB (NoSQL)",
            "DocumentDB (MongoDB compatible)",
        ],
        "storage": ["S3 (Simple Storage Service)"],
        "cdn": ["CloudFront"],
        "load_balancer": ["Application Load Balancer (ALB)", "Network Load Balancer (NLB)"],
        "cache": ["ElastiCache (Redis/Memcached)"],
        "monitoring": ["CloudWatch", "X-Ray"],
        "ci_cd": ["CodePipeline", "CodeBuild", "CodeDeploy"],
        "secrets": ["Secrets Manager", "Systems Manager Parameter Store"],
        "networking": ["VPC", "Route 53"],
    },
    "gcp": {
        "name": "Google Cloud Platform (GCP)",
        "compute": [
            "Compute Engine",
            "Cloud Run",
            "Google Kubernetes Engine (GKE)",
            "Cloud Functions",
            "App Engine",
        ],
        "database": [
            "Cloud SQL (PostgreSQL/MySQL)",
            "Cloud Spanner",
            "Firestore (NoSQL)",
            "Bigtable",
        ],
        "storage": ["Cloud Storage"],
        "cdn": ["Cloud CDN"],
        "load_balancer": ["Cloud Load Balancing"],
        "cache": ["Memorystore (Redis/Memcached)"],
        "monitoring": ["Cloud Monitoring (Stackdriver)", "Cloud Trace"],
        "ci_cd": ["Cloud Build", "Cloud Deploy"],
        "secrets": ["Secret Manager"],
        "networking": ["VPC", "Cloud DNS"],
    },
    "azure": {
        "name": "Microsoft Azure",
        "compute": [
            "Virtual Machines",
            "Container Instances",
            "Azure Kubernetes Service (AKS)",
            "Azure Functions",
            "App Service",
        ],
        "database": [
            "Azure Database for PostgreSQL/MySQL",
            "Azure SQL Database",
            "Cosmos DB (NoSQL)",
        ],
        "storage": ["Azure Blob Storage"],
        "cdn": ["Azure CDN"],
        "load_balancer": ["Azure Load Balancer", "Application Gateway"],
        "cache": ["Azure Cache for Redis"],
        "monitoring": ["Azure Monitor", "Application Insights"],
        "ci_cd": ["Azure DevOps", "GitHub Actions"],
        "secrets": ["Azure Key Vault"],
        "networking": ["Virtual Network", "Azure DNS"],
    },
    "digital_ocean": {
        "name": "DigitalOcean",
        "compute": [
            "Droplets (Virtual Machines)",
            "App Platform",
            "Kubernetes (DOKS)",
            "Functions",
        ],
        "database": [
            "Managed PostgreSQL",
            "Managed MySQL",
            "Managed MongoDB",
            "Managed Redis",
        ],
        "storage": ["Spaces (Object Storage)"],
        "cdn": ["Spaces CDN"],
        "load_balancer": ["Load Balancers"],
        "cache": ["Managed Redis"],
        "monitoring": ["Monitoring & Alerting"],
        "ci_cd": ["App Platform (built-in CI/CD)", "GitHub Actions"],
        "secrets": ["App Platform Environment Variables"],
        "networking": ["VPC", "Cloud Firewalls"],
    },
    "heroku": {
        "name": "Heroku",
        "compute": ["Dynos (Web/Worker processes)"],
        "database": [
            "Heroku Postgres",
            "Heroku Redis",
        ],
        "storage": ["AWS S3 (via add-ons)"],
        "cdn": ["Heroku SSL/CDN"],
        "load_balancer": ["Built-in Router"],
        "cache": ["Heroku Redis"],
        "monitoring": ["Heroku Metrics", "Logplex"],
        "ci_cd": ["Heroku Pipelines", "GitHub Integration"],
        "secrets": ["Config Vars"],
        "networking": ["Private Spaces", "SSL"],
    },
    "vercel": {
        "name": "Vercel",
        "compute": ["Serverless Functions", "Edge Functions"],
        "database": [
            "Vercel Postgres (Neon)",
            "Vercel KV (Redis)",
            "External databases",
        ],
        "storage": ["Vercel Blob"],
        "cdn": ["Global Edge Network"],
        "load_balancer": ["Automatic (Built-in)"],
        "cache": ["Edge Caching", "Vercel KV"],
        "monitoring": ["Vercel Analytics", "Web Vitals"],
        "ci_cd": ["Git Integration (Automatic)"],
        "secrets": ["Environment Variables"],
        "networking": ["Custom Domains", "Edge Network"],
    },
    "render": {
        "name": "Render",
        "compute": [
            "Web Services",
            "Background Workers",
            "Cron Jobs",
            "Static Sites",
        ],
        "database": [
            "PostgreSQL",
            "Redis",
        ],
        "storage": ["Disk Storage"],
        "cdn": ["Global CDN"],
        "load_balancer": ["Built-in"],
        "cache": ["Redis"],
        "monitoring": ["Metrics & Logging"],
        "ci_cd": ["Auto-deploy from Git"],
        "secrets": ["Environment Variables", "Secret Files"],
        "networking": ["Custom Domains", "TLS/SSL"],
    },
    "railway": {
        "name": "Railway",
        "compute": ["Services (Containers)", "Cron Jobs"],
        "database": [
            "PostgreSQL",
            "MySQL",
            "MongoDB",
            "Redis",
        ],
        "storage": ["Volumes"],
        "cdn": ["Railway CDN"],
        "load_balancer": ["Built-in"],
        "cache": ["Redis"],
        "monitoring": ["Metrics & Logging"],
        "ci_cd": ["GitHub Integration"],
        "secrets": ["Environment Variables"],
        "networking": ["Custom Domains", "Private Networking"],
    },
    "fly_io": {
        "name": "Fly.io",
        "compute": ["Fly Machines (Containers)", "Apps"],
        "database": [
            "Fly Postgres",
            "External databases",
        ],
        "storage": ["Fly Volumes"],
        "cdn": ["Anycast Network"],
        "load_balancer": ["Fly Proxy"],
        "cache": ["External Redis"],
        "monitoring": ["Metrics & Logging"],
        "ci_cd": ["flyctl CLI", "GitHub Actions"],
        "secrets": ["Secrets"],
        "networking": ["Private Networking", "WireGuard VPN"],
    },
}


def get_platform_services(platform: str) -> Dict[str, Any]:
    """
    Get available services for a specific platform.

    Args:
        platform: Platform identifier (aws, gcp, azure, etc.)

    Returns:
        Dictionary of platform services

    Raises:
        ValueError: If platform is not recognized
    """
    platform_key = platform.lower()
    if platform_key not in PLATFORM_SERVICES:
        raise ValueError(
            f"Unknown platform: {platform}. "
            f"Must be one of {list(PLATFORM_SERVICES.keys())}"
        )
    return PLATFORM_SERVICES[platform_key]


def get_recommended_services(
    platform: str, app_type: str = "web_app"
) -> Dict[str, str]:
    """
    Get recommended services for a specific platform and application type.

    Args:
        platform: Platform identifier
        app_type: Application type (web_app, api, static, etc.)

    Returns:
        Dictionary of recommended services
    """
    services = get_platform_services(platform)

    # Default recommendations for web applications
    recommendations = {
        "aws": {
            "compute": "ECS with Fargate",
            "database": "RDS PostgreSQL",
            "storage": "S3",
            "cdn": "CloudFront",
            "monitoring": "CloudWatch",
        },
        "gcp": {
            "compute": "Cloud Run",
            "database": "Cloud SQL PostgreSQL",
            "storage": "Cloud Storage",
            "cdn": "Cloud CDN",
            "monitoring": "Cloud Monitoring",
        },
        "azure": {
            "compute": "App Service",
            "database": "Azure Database for PostgreSQL",
            "storage": "Azure Blob Storage",
            "cdn": "Azure CDN",
            "monitoring": "Azure Monitor",
        },
        "digital_ocean": {
            "compute": "App Platform",
            "database": "Managed PostgreSQL",
            "storage": "Spaces",
            "cdn": "Spaces CDN",
            "monitoring": "Monitoring & Alerting",
        },
        "heroku": {
            "compute": "Dynos",
            "database": "Heroku Postgres",
            "storage": "S3 (add-on)",
            "cdn": "Heroku SSL/CDN",
            "monitoring": "Heroku Metrics",
        },
        "vercel": {
            "compute": "Serverless Functions",
            "database": "Vercel Postgres",
            "storage": "Vercel Blob",
            "cdn": "Global Edge Network",
            "monitoring": "Vercel Analytics",
        },
        "render": {
            "compute": "Web Services",
            "database": "PostgreSQL",
            "storage": "Disk Storage",
            "cdn": "Global CDN",
            "monitoring": "Metrics & Logging",
        },
        "railway": {
            "compute": "Services",
            "database": "PostgreSQL",
            "storage": "Volumes",
            "cdn": "Railway CDN",
            "monitoring": "Metrics & Logging",
        },
        "fly_io": {
            "compute": "Fly Machines",
            "database": "Fly Postgres",
            "storage": "Fly Volumes",
            "cdn": "Anycast Network",
            "monitoring": "Metrics & Logging",
        },
    }

    platform_key = platform.lower()
    return recommendations.get(platform_key, {})


def get_all_platforms() -> List[str]:
    """Get list of all supported platforms."""
    return list(PLATFORM_SERVICES.keys())


def get_platform_display_name(platform: str) -> str:
    """Get the display name for a platform."""
    services = get_platform_services(platform)
    return services.get("name", platform.upper())
