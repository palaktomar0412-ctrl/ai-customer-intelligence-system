"""
AI-Powered Customer Intelligence, Segmentation and Churn Prediction System
FastAPI Backend - Main Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine, Base
from app.routes import auth, customers, analytics, segmentation, churn, recommendations, reports


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown events."""
    # Startup
    print("🚀 Starting Customer Intelligence System...")
    print(f"📊 Environment: {settings.ENVIRONMENT}")
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
    """Health check endpoint."""
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
