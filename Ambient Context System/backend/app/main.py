```python
"""
Ambient Context System - Main Application Entry Point
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging

from app.core.config import settings
from app.core.logging import setup_logging
from app.api.routes import (
    context_router,
    collaboration_router,
    suggestions_router,
    voice_router,
    health_router
)
from app.services.context_engine import ContextEngine
from app.services.cache_manager import CacheManager

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown
    """
    # Startup
    logger.info("Starting Ambient Context System")
    
    # Initialize services
    app.state.context_engine = ContextEngine()
    app.state.cache_manager = CacheManager()
    
    await app.state.cache_manager.connect()
    await app.state.context_engine.initialize()
    
    logger.info("Services initialized successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Ambient Context System")
    await app.state.cache_manager.disconnect()
    await app.state.context_engine.cleanup()
    logger.info("Shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Ambient Context System",
    description="Background system maintaining awareness of project context and creative direction",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Include routers
app.include_router(health_router.router, prefix="/api/health", tags=["health"])
app.include_router(context_router.router, prefix="/api/context", tags=["context"])
app.include_router(collaboration_router.router, prefix="/api/collaboration", tags=["collaboration"])
app.include_router(suggestions_router.router, prefix="/api/suggestions", tags=["suggestions"])
app.include_router(voice_router.router, prefix="/api/voice", tags=["voice"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Ambient Context System",
        "status": "operational",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
```