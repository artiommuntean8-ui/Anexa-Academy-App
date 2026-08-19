import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.init_db import init_db, seed_demo_data
from app.db.session import SessionLocal

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.
    Initializes database schema and populates demo seed data if DB is fresh.
    """
    try:
        logger.info("Initializing database schema...")
        init_db()
        db = SessionLocal()
        try:
            logger.info("Ensuring Python Kids curriculum and demo data...")
            seed_demo_data(db)
        finally:
            db.close()
        logger.info("Database schema initialized and verified successfully.")
    except Exception as e:
        logger.warning(f"Database initialization note: {e}")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint offering a basic welcome message and documentation links.
    """
    return {
        "message": "Welcome to Academy Student Dashboard API",
        "organization": "Academia ArkiTech",
        "status": "online",
        "docs": "/docs",
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
