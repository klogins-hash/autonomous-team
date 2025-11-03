```python
"""
Community Engagement System - Main Application Entry Point
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.routes import router as api_router
from app.db.database import init_db, close_db
from app.cache.redis_client import init_redis, close_redis

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown events
    """
    # Startup
    logger.info("Starting Community Engagement System")
    await init_db()
    await init_redis()
    logger.info("Database and Redis initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Community Engagement System")
    await close_db()
    await close_redis()
    logger.info("Cleanup completed")


# Create FastAPI application
app = FastAPI(
    title="Community Engagement System",
    description="Tools for team formation, skill matching, and project discovery",
    version="1.0.0",
    lifespan=lifespan
)

# Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)


# Exception Handlers
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Health Check Endpoints
@app.get("/health", tags=["Health"])
async def health_check():
    """Basic health check endpoint"""
    return {
        "status": "healthy",
        "service": "Community Engagement System",
        "version": "1.0.0"
    }


@app.get("/health/ready", tags=["Health"])
async def readiness_check():
    """Readiness check - verifies database and cache connectivity"""
    try:
        from app.db.database import get_db
        from app.cache.redis_client import get_redis
        
        # Check database
        db = await get_db()
        await db.execute("SELECT 1")
        
        # Check Redis
        redis = await get_redis()
        await redis.ping()
        
        return {"status": "ready"}
    except Exception as e:
        logger.error(f"Readiness check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "error": str(e)}
        )


# Include API Routes
app.include_router(api_router, prefix="/api/v1")


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Community Engagement System",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
```
