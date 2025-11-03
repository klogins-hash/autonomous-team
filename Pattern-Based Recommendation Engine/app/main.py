```python
"""
Main FastAPI application for Pattern-Based Recommendation Engine
"""
import logging
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db, close_db
from app.cache import init_cache, close_cache
from app.routes import (
    health,
    auth,
    patterns,
    insights,
    recommendations,
    users,
    voice,
)
from app.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    logger.info("Starting Pattern-Based Recommendation Engine")
    
    # Startup
    await init_db()
    await init_cache()
    logger.info("Database and cache initialized")
    
    yield
    
    # Shutdown
    await close_db()
    await close_cache()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Pattern-Based Recommendation Engine",
    description="System that suggests actions, ideas, or connections based on recognized patterns",
    version="1.0.0",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.cascade.ai"],
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(patterns.router, prefix="/api/v1/patterns", tags=["patterns"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["insights"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(voice.router, prefix="/api/v1/voice", tags=["voice"])


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,