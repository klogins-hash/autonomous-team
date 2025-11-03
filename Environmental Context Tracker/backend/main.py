```python
"""
Environmental Context Tracker - Main Application
FastAPI application for monitoring and correlating environmental factors with creative output
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database import init_db, get_db
from backend.cache import init_redis, close_redis
from backend.routes import (
    auth_routes,
    user_routes,
    environment_routes,
    pattern_routes,
    analytics_routes,
    health_routes,
)
from backend.websocket import ConnectionManager
from backend.monitoring import setup_monitoring

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# WebSocket connection manager
manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager"""
    logger.info("Starting Environmental Context Tracker")
    
    # Startup
    await init_db()
    await init_redis()
    setup_monitoring()
    
    logger.info("Application startup complete")
    yield
    
    # Shutdown
    logger.info("Shutting down Environmental Context Tracker")
    await close_redis()
    logger.info("Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="Environmental Context Tracker",
    description="Monitor and correlate environmental factors with creative output",
    version="1.0.0",
    lifespan=lifespan,
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS,
)


# Include routers
app.include_router(health_routes.router, prefix="/api/v1", tags=["health"])
app.include_router(auth_routes.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(user_routes.router, prefix="/api/v1/users", tags=["users"])
app.include_router(environment_routes.router, prefix="/api/v1/environment", tags=["environment"])
app.include_router(pattern_routes.router, prefix="/api/v1/patterns", tags=["patterns"])
app.include_router(analytics_routes.router, prefix="/api/v1/analytics", tags=["analytics"])


# WebSocket endpoint
@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(
                {
                    "type": "update",
                    "user_id": user_id,
                    "timestamp": datetime.utcnow().isoformat(),
                    "data": data,
                }
            )
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        logger.info(f"User {user_id} disconnecte