"""
Flable.ai - AI-Powered Marketing Platform
Main FastAPI Application
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import sentry_sdk
from prometheus_client import make_asgi_app
from loguru import logger
import sys

# Import from local modules (we're running from backend directory)
from api.routes import campaigns, analytics, integrations, auth
from api.routes.dashboard import dashboard_router, users_router
from database.connection import engine, Base
from utils.config import settings
from utils.redis_client import redis_client


# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    "../logs/flable_{time}.log",
    rotation="500 MB",
    retention="30 days",
    compression="zip",
    level="DEBUG"
)

# Initialize Sentry for error tracking
if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        traces_sample_rate=0.1,
        profiles_sample_rate=0.1,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting Flable.ai application...")
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
    
    # Test Redis connection (optional)
    try:
        await redis_client.connect()
        if await redis_client.ping():
            logger.info("✓ Redis connection established")
        else:
            logger.warning("⚠ Redis not available - running without cache")
    except Exception as e:
        logger.warning(f"⚠ Redis not available: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Flable.ai application...")
    try:
        await redis_client.close()
    except:
        pass


# Initialize FastAPI app
app = FastAPI(
    title="Flable.ai API",
    description="AI-Powered Marketing Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
    redirect_slashes=False  # Prevent 307 redirects for trailing slashes
)

# Add middlewares
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["Content-Type", "Authorization", "Accept", "X-Requested-With"],
)

# Add Prometheus metrics endpoint
try:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
except Exception as e:
    logger.warning(f"Could not mount Prometheus metrics: {e}")


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": str(exc.body) if exc.body else None
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all other exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Flable.ai API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["Campaigns"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(integrations.router, prefix="/api/v1/integrations", tags=["Integrations"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_level="info"
    )
