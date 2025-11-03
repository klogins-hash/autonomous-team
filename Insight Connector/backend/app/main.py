```python
"""
Main application entry point for Insight Connector
Initializes FastAPI app with all middleware, routes, and services
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api import health, insights, personalization, sync, analytics
from app.services.database import init_db, close_db
from app.services.redis_service import init_redis, close_redis
from app.services.insight_sync import start_sync_scheduler, stop_sync_scheduler
from app.utils.logging_config import setup_logging
from app.utils.metrics import setup_metrics

# Setup logging
logger = setup_logging(settings.log_level, settings.log_format)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    Startup: Initialize services
    Shutdown: Cleanup resources
    """
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    
    # Initialize services
    await init_db()
    await init_redis()
    
    # Start background tasks
    if settings.enable_real_time_sync:
        await start_sync_scheduler()
    
    # Setup metrics
    if settings.enable_metrics:
        setup_metrics()
    
    logger.info("Application startup complete")
    
    yield
    
    # Cleanup
    logger.info("Shutting down application")
    
    if settings.enable_real_time_sync:
        await stop_sync_scheduler()
    
    await close_redis()
    await close_db()
    
    logger.info("Application shutdown complete")


# Create FastAPI app
app = FastAPI(