```python
"""Application Configuration"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings from environment variables"""

    # Application
    app_name: str = "AI Resource Manager"
    app_env: str = Field(default="development")
    debug: bool = Field(default=False)
    log_level: str = Field(default="INFO")

    # API
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_workers: int = Field(default=4)
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # Database
    database_url: str = Field(default="postgresql://user:password@localhost:5432/ai_resource_manager")
    database_pool_size: int = Field(default=20)
    database_max_overflow: int = Field(default=40)

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0")
    redis_cache_url: str = Field(default="redis://localhost:6379/1")
    redis_queue_url: str = Field(default="redis://localhost:6379/2")

    # JWT
    jwt_secret_key: str = Field(default="your-secret-key-change-in-production")
    jwt_algorithm: str = Field(default="HS256")
    jwt_expiration_hours: int = Field(default=24)
    refresh_token_expiration_days: int = Field(default=30)

    # S3/Object Storage
    s3_endpoint_url: str = Field(default="https://s3.fr-par.scw.cloud")
    s3_region: str = Field(default="fr-par")
    s3_access_key_id: str = Field(default="")
    s3_secret_access_key: str = Field(default="")
    s3_bucket_datasets: str = Field(default="ai-datasets")
    s3_bucket_models: str = Field(default="ai-models")
    s3_bucket_uploads: str = Field(default="ai-uploads")

    # Celery
    celery_broker_url: str = Fiel