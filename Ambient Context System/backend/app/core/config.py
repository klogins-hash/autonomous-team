```python
"""
Configuration management for Ambient Context System
"""

from typing import List
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "Ambient Context System"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/ambient_context"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # AI/ML
    OPENAI_API_KEY: str = ""
    MODEL_NAME: str = "gpt-4"
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    
    # Voice
    VOICE_ENABLED: bool = True
    VOICE_SAMPLE_RATE: int = 16000
    VOICE_CHUNK_SIZE: int = 1024
    
    # Collaboration
    MAX_CONCURRENT_SESSIONS: int = 100
    SESSION_TIMEOUT_MINUTES: int = 30
    PRESENCE_UPDATE_INTERVAL: int = 5
    
    # Storage
    UPLOAD_DIR: str = "/tmp/uploads"
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


settings = get_settings()
```