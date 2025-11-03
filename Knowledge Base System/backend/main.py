```python
"""
Knowledge Base System - Main Application Entry Point
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import settings
from database.models import Base
from routes import (
    auth_routes,
    articles_routes,
    categories_routes,
    search_routes,
    user_routes,
    health_routes,
)
from middleware.error_handler import setup_error_handlers
from middleware.logging_config import setup_logging
from services.cache_service import CacheService

# Setup logging
logger = setup_logging()

# Initialize cache service
cache_service = CacheService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown
    """
    # Startup
    logger.info("Starting Knowledge Base System")
    
    # Initialize database
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Initialize cache
    await cache_service.connect()
    logger.info("Cache service initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Knowledge Base System")
    await cache_service.disconnect()
    await engine.dispose()


# Database setup
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_size=settings.database_pool_size,
    max_overflow=10,
    pool_pre_ping=True,
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """Dependency for database session"""
    async with async_session_maker() as session:
        yield session


# Create FastAPI app
app = FastAPI(
    title="Knowledge Base System",
    description="Integrated documentation and learning resource center",
    version="1.0.0",
    lifespan=lifespan,
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts,
)

# Setup error handlers
setup_error_handlers(app)


# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests and responses"""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


# Include routers
app.include_router(health_routes.router, prefix="/api/v1", tags=["health"])
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])
app.include_router(articles_routes.router, prefix="/api/v1/articles", tags=["articles"])
app.include_router(categories_routes.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(search_routes.router, prefix="/api/v1/search", tags=["search"])


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Knowledge Base System API",
        "version": "1.0.0",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(