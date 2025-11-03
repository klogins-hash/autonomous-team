```python
"""
Configuration management for Insight Connector
Handles environment-based settings with sensible defaults
"""

from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    app_name: str = "Insight Connector"
    app_version: str = "1.0.0"
    debug: bool = Field(default=False, env="DEBUG")
    environment: str = Field(default="development", env="ENVIRONMENT")
    
    # Server
    host: str = Field(default="0.0.0.0", env="HOST")
    port: int = Field(default=8000, env="PORT")
    reload: bool = Field(default=True, env="RELOAD")
    
    # Database
    database_url: str = Field(
        default="postgresql://user:password@localhost:5432/insight_connector",
        env="DATABASE_URL"
    )
    database_pool_size: int = Field(default=20, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(default=10, env="DATABASE_MAX_OVERFLOW")
    database_pool_recycle: int = Field(default=3600, env="DATABASE_POOL_RECYCLE")
    
    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        env="REDIS_URL"
    )
    redis_cache_ttl: int = Field(default=3600, env="REDIS_CACHE_TTL")
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-change-in-production",
        env="SECRET_KEY"
    )
    algorithm: str = Field(default="HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=7, env="REFRESH_TOKEN_EXPIRE_DAYS")
    
    # CORS
    cors_origins: list = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        env="CORS_ORIGINS"
    )
    cors_credentials: bool = Field(default=True, env="CORS_CREDENTIALS")
    cors_methods: list = Field(default=["*"], env="CORS_METHODS")
    cors_headers: list = Field(default=["*"], env="CORS_HEADERS")
    
    # Insight Engine Integration
    insight_engine_url: str = Field(
        default="http://localhost:8001",
        env="INSIGHT_ENGINE_URL"
    )
    insight_engine_api_key: str = Field(
        default="",
        env="INSIGHT_ENGINE_API_KEY"
    )
    insight_sync_interval: int = Field(default=300, env="INSIGHT_SYNC_INTERVAL")  # 5 minutes
    
    # Collaboration Hub Integration
    collaboration_hub_url: str = Field(
        default="http://localhost:8002",
        env="COLLABORATION_HUB_URL"
    )
    collaboration_hub_api_key: str = Field(
        default="",
        env="COLLABORATION_HUB_API_KEY"
    )
    
    # WebSocket
    websocket_heartbeat_interval: int = Field(default=30, env="WEBSOCKET_HEARTBEAT_INTERVAL")
    websocket_max_connections: int = Field(default=1000, env="WEBSOCKET_MAX_CONNECTIONS")
    
    # Logging
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    log_format: str = Field(default="json", env="LOG_FORMAT")
    
    # Monitoring
    enable_metrics: bool = Field(default=True, env="ENABLE_METRICS")
    metrics_port: int = Field(default=9090, env="METRICS_PORT")
    
    # Feature Flags
    enable_voice_integration: bool = Field(default=True, env="ENABLE_VOICE_INTEGRATION")
    enable_real_time_sync: bool = Field(default=True, env="ENABLE_REAL_TIME_SYNC")
    enable_analytics: bool = Field(default=True, env="ENABLE_ANALYTICS")
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export for easy access
settings = get_settings()
```
