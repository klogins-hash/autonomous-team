```python
"""
Creative Pattern Analytics Platform - Main Application
Autonomous AI system for tracking and analyzing creative patterns
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.database.connection import init_db, close_db
from app.cache.redis_client import init_redis, close_redis
from app.api.routes import (
    auth,
    patterns,
    activities,
    analytics,
    insights,
    health,
)
from app.middleware.error_handler import error_handler_middleware
from app.middleware.request_logger import request_logger_middleware

# Setup logging
logger = setup_logging(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown
    """
    logger.info("🚀 Starting Creative Pattern Analytics Platform")
    
    # Startup
    try:
        await init_db()
        logger.info("✅ Database initialized")
        
        await init_redis()
        logger.info("✅ Redis cache initialized")
        
    except Exception as e:
        logger.error(f"❌ Startup failed: {str(e)}")
        raise
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Creative Pattern Analytics Platform")
    try:
        await close_db()
        await close_redis()
        logger.info("✅ Cleanup completed")
    except Exception as e:
        logger.error(f"⚠️ Shutdown error: {str(e)}")


# Initialize FastAPI app
app = FastAPI(
    title="Creative Pattern Analytics Platform",
    description="AI-powered system for tracking and analyzing creative patterns",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security Middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)

# Custom Middleware
app.middleware("http")(request_logger_middleware)
app.middleware("http")(error_handler_middleware)


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# Include Routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(patterns.router, prefix="/api/v1/patterns", tags=["patterns"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])
app.include_router(insights.router, prefix="/api/v1/insights", tags=["insights"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Creative Pattern Analytics Platform",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",