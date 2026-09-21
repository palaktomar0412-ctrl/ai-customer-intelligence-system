"""
AI-Powered Customer Intelligence, Segmentation and Churn Prediction System
FastAPI Backend - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import os

from sqlalchemy import select

from app.core.config import settings
from app.core.database import engine, Base, AsyncSessionLocal
from app.core.security import get_password_hash
from app.models.models import User
from app.routes import auth, customers, analytics, segmentation, churn, recommendations, reports


async def _ensure_admin_user():
    """Create the default admin account if no users exist (cloud-friendly bootstrap)."""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).limit(1))
        if result.scalar_one_or_none() is None:
            session.add(User(
                username="admin",
                email="admin@customerintelligence.com",
                password_hash=get_password_hash("admin123"),
                full_name="System Administrator",
                role="admin",
            ))
            await session.commit()
            print("👤 Default admin user created (admin@customerintelligence.com / admin123)")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup: create tables and bootstrap admin user
    print("🚀 Starting Customer Intelligence System...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await _ensure_admin_user()
    yield
    # Shutdown
    print("👋 Shutting down Customer Intelligence System...")


# Initialize FastAPI application
app = FastAPI(
    title="AI-Powered Customer Intelligence System",
    description="Customer analytics, segmentation, churn prediction, and recommendation engine",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(customers.router, prefix="/api/customers", tags=["Customers"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(segmentation.router, prefix="/api/segmentation", tags=["Segmentation"])
app.include_router(churn.router, prefix="/api/churn", tags=["Churn Prediction"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])


@app.get("/", tags=["Root"])
async def root():
    """Serve the SPA entry when frontend hosting is enabled, else API info."""
    if settings.SERVE_FRONTEND and settings.FRONTEND_DIST and os.path.isdir(settings.FRONTEND_DIST):
        return FileResponse(os.path.join(settings.FRONTEND_DIST, "index.html"))
    return {
        "message": "AI-Powered Customer Intelligence System API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/api/docs"
    }


@app.get("/api/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "api": "running",
            "database": "connected",
            "ml_models": "loaded"
        }
    }


# ---- Optional: serve the built React frontend from this same service ----
# Enabled when SERVE_FRONTEND=true and FRONTEND_DIST points to the build output.
if settings.SERVE_FRONTEND and settings.FRONTEND_DIST and os.path.isdir(settings.FRONTEND_DIST):
    app.mount("/assets", StaticFiles(directory=os.path.join(settings.FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_fallback(full_path: str):
        """Serve static files, falling back to index.html for SPA routes."""
        candidate = os.path.normpath(os.path.join(settings.FRONTEND_DIST, full_path))
        if candidate.startswith(os.path.normpath(settings.FRONTEND_DIST)) and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(settings.FRONTEND_DIST, "index.html"))

    print(f"🌐 Serving frontend from {settings.FRONTEND_DIST}")
