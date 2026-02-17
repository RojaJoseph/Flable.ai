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
from loguru import logger
import sys
import traceback

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
    level="DEBUG"  # Set to DEBUG to see everything
)

# CORS origins - hardcoded as primary source of truth
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "https://flable-ai-xwuo.onrender.com",
]

# Also add any from environment variable
try:
    env_origins = settings.ALLOWED_ORIGINS
    if isinstance(env_origins, str):
        env_origins = [o.strip() for o in env_origins.split(',') if o.strip()]
    for origin in env_origins:
        if origin not in CORS_ORIGINS:
            CORS_ORIGINS.append(origin)
except:
    pass

logger.info(f"CORS allowed origins: {CORS_ORIGINS}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Flable.ai application...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Database URL type: {settings.DATABASE_URL[:20]}...")

    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Database tables created")
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        logger.error(traceback.format_exc())

    try:
        await redis_client.connect()
        if await redis_client.ping():
            logger.info("✓ Redis connected")
        else:
            logger.warning("⚠ Redis not available")
    except Exception as e:
        logger.warning(f"⚠ Redis not available: {e}")

    yield

    logger.info("Shutting down...")
    try:
        await redis_client.close()
    except:
        pass


app = FastAPI(
    title="Flable.ai API",
    description="AI-Powered Marketing Platform API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ============================================================
# CORS - MUST be first middleware
# ============================================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)


# ============================================================
# Exception handlers - include CORS headers in error responses
# ============================================================
def add_cors_headers(response: JSONResponse, request: Request) -> JSONResponse:
    """Add CORS headers to error responses"""
    origin = request.headers.get("origin", "")
    if origin in CORS_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()}")
    response = JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )
    return add_cors_headers(response, request)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_detail = traceback.format_exc()
    logger.error(f"Unhandled exception on {request.method} {request.url}: {exc}")
    logger.error(error_detail)
    response = JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "error": str(exc),  # Show actual error for debugging
        },
    )
    return add_cors_headers(response, request)


# ============================================================
# Routes
# ============================================================
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "allowed_origins": CORS_ORIGINS,
        "database": settings.DATABASE_URL[:30] + "..."
    }


@app.get("/")
async def root():
    return {
        "message": "Welcome to Flable.ai API",
        "version": "1.0.0",
        "docs": "/docs",
    }


app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["Campaigns"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(integrations.router, prefix="/api/v1/integrations", tags=["Integrations"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
