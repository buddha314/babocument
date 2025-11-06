"""
Babocument Server - Main Application

FastAPI application with REST API and WebSocket support for multi-agent research assistant.
"""

import logging
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager - handles startup and shutdown tasks.
    """
    # Startup
    logger.info(
        "starting_server",
        environment=settings.environment,
        debug=settings.debug,
        port=settings.port,
    )

    # TODO: Initialize resources (Phase 1)
    # - Connect to Redis
    # - Initialize Vector Database
    # - Start Agent Coordinator
    # - Load MCP clients (Phase 2)

    yield

    # Shutdown
    logger.info("shutting_down_server")

    # TODO: Cleanup resources
    # - Close Redis connections
    # - Close Vector DB
    # - Stop agents gracefully


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    description="Multi-agent research assistant for scientific literature analysis",
    version="0.1.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - health check."""
    return {
        "name": settings.app_name,
        "version": "0.1.0",
        "status": "running",
        "environment": settings.environment,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.environment,
        # TODO: Add resource health checks (Redis, Vector DB, etc.)
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        exc_info=exc,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred",
        },
    )


# TODO: Import and register routers (Phase 1)
# from app.api import rest, websocket
# app.include_router(rest.router, prefix="/api/v1")
# app.include_router(websocket.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
