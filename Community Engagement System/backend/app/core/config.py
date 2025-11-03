```python
"""
Application Configuration Management
"""
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Configuration
    API_HOST: str = Field(default="0.0.0.0")
    API_PORT: int = Field(default=8000)
    DEBUG: bool = Field(default=False)
    LOG_LEVEL: str = Field(default="INFO")
    
    # Database Configuration
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost:5432/community_engagement")
    DATABASE_POOL_SIZE: int = Field(default=20)
    DATABASE_TIMEOUT: int = Field(default=30)
    
    # Redis Configuration
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    REDIS_CLUSTER_ENABLED: bool = Field(default=False)
    
    # JWT Configuration
    JWT_SECRET: str = Field(default="your-secret-key-change-in-production")
    JWT_ALGORITHM: str = Field(default="HS256")
    JWT_EXPIRATION_HOURS: int = Field(default=24)
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000", "http://localhost:8000"])
    ALLOWED_HOSTS: List[str] = Field(default=["localhost", "127.0.0.1"])
    
    # S3/Storage Configuration
    S3_BUCKET_NAME: str = Field(default="community-engagement-storage")
    S3_REGION: str = Field(default="fr-par")
    S3_ACCESS_KEY: str = Field(default="")
    S3_SECRET_KEY: str = Field(default="")
    
    # Email Configuration
    SMTP_HOST: str = Field(default="smtp.gmail.com")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    
    # Feature Flags
    ENABLE_SKILL_MATCHING: bool = Field(default=True)
    ENABLE_PROJECT_DISCOVERY: bool = Field(default=True)
    ENABLE_TEAM_FORMATION: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
```
