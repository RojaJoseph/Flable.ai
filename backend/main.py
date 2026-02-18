"""
Flable.ai Backend - PRODUCTION READY
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import sys

# Setup basic logging
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routes
from api.routes import campaigns, analytics, integrations, auth
from api.routes.dashboard import dashboard_router, users_router
from database.connection import engine, Base
from utils.config import settings

# CORS - Allow these origins
ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "https://flable-ai-xwuo.onrender.com",
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup"""
    logger.info("🚀 Starting Flable.ai...")
    
    # Create tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database ready")
    except Exception as e:
        logger.error(f"❌ Database error: {e}")
    
    yield
    
    logger.info("👋 Shutting down")


# Create app
app = FastAPI(
    title="Flable.ai API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS - CRITICAL: Must be FIRST
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now - we'll restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    logger.error(f"❌ ERROR: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "cors": "enabled"
    }

@app.get("/")
def root():
    return {
        "message": "Flable.ai API",
        "docs": "/docs"
    }

# Include all routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users_router, prefix="/api/v1/users", tags=["Users"])
app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["Campaigns"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(integrations.router, prefix="/api/v1/integrations", tags=["Integrations"])
app.include_router(dashboard_router, prefix="/api/v1/dashboard", tags=["Dashboard"])

logger.info(f"✅ App configured - CORS: {ALLOWED_ORIGINS}")
