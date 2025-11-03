```python
"""
Creative Flow AI - Main Application Entry Point
"""

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db, get_db
from app.cache import init_cache, get_cache
from app.routes import (
    auth,
    users,
    projects,
    collaboration,
    ai_suggestions,
    analytics,
    health,
)
from app.middleware import LoggingMiddleware, ErrorHandlingMiddleware
from app.utils.logger import setup_logging

# Setup logging
logger = setup_logging(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle - startup and shutdown
    """
    # Startup