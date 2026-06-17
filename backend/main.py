"""
FastAPI Application Main Entry Point
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.api.routes import router as api_router
from config.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Requirements to ADO Artifacts System",
    description="Convert stakeholder requirements into structured engineering artifacts and sync to Azure DevOps",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Settings
settings = get_settings()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include API routes
app.include_router(api_router)

# Health check
@app.get("/")
async def root():
    return {
        "message": "Requirements to ADO Artifacts System API",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting Requirements to ADO System")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Azure DevOps Organization: {settings.ado_organization}")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("🛑 Shutting down Requirements to ADO System")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.server_host,
        port=settings.server_port,
        reload=settings.debug
    )
