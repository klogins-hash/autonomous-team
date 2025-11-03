```python
"""Application configuration management."""

from typing import Optional
from functools import lru_cache
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class DatabaseSettings(BaseSettings):
    """Database configuration."""

    url: str = Field(default="postgresql://localhost/creativity_journal")
    pool_size: int = Field(default=20)
    max_overflow: int = Field(default=40)
    echo: bool = Field(default=False)
    pool_pre_ping: bool = Field(default=True)

    class Config:
        env_prefix = "DATABASE_"


class RedisSettings(BaseSettings):
    """Redis configuration."""

    url: str = Field(default="redis://localhost:6379/0")
    cluster_nodes: Optional[str] = Field(default=None)
    cluster_mode: bool = Field(default=False)
    ttl_pattern_results: int = Field(default=3600)
    ttl_user_preferences: int = Field(default=1800)
    ttl_visualization_data: int = Field(default=900)

    class Config:
        env_prefix = "REDIS_"


class CartesiaSettings(BaseSettings):
    """Cartesia Voice API configuration."""

    api_key: str = Field(default="")
    voice_id: str = Field(default="default")
    model: str = Field(default="sonic")
    sample_rate: int = Field(default=16000)
    timeout: int = Field(default=30)

    class Config:
        env_prefix = "CARTESIA_"


class StorageSettings(BaseSettings):
    """Object storage configuration."""

    access_key: str = Field(default="")
    secret_key: str = Field(default="")
    region: str = Field(default="fr-par")
    bucket_name: str = Field(default="creativity-journal-assets")
    endpoint_url: Optional[str] = Field(default=None)
    encryption: str = Field(default="AES-256")

    class Config:
        env_prefix = "SCALEWAY_"


class SecuritySettings(BaseSettings):
    """Security configuration."""

    secret_key: str = Field(default="change-me-in-production")
    jwt_secret: str = Field(default="change-me-in-production")
    jwt_expiration: int = Field(default=86400)
    algorithm: str = Field(default="HS256")
    bcrypt_rounds: int = Field(default=12)

    class Config:
        env_prefix = ""


class Settings(BaseSettings):
    """Main application settings."""

    # Environment
    environment: str = Field(default="development")
    debug: bool = Field(default=False)

    # API Configuration
    api_host: str = Field(default="0.0.0.0")
    api_port: int = Field(default=8000)
    api_title: str = Field(default="Creativity Journal Integration API")
    api_version: str = Field(default="1.0.0")
    cors_origins: list[str] = Field(default=["http://localhost:3000"])

    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json")

    # Feature Flags
    enable_pattern_recognition: bool = Field(default=True)
    enable_real_time_analytics: bool = Field(default=True)
    enable_voice_transcription: bool = Field(default=True)

    # Sub-configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    redis: RedisSettings = Field(default_factory=RedisSettings)
    cartesia: CartesiaSettings = Field(default_factory=CartesiaSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
```
