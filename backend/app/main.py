from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import Base, engine, get_db
import app.models  # Ensures all ORM models are registered
from app.api.v1 import api_router
from app.database.seed import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    Base.metadata.create_all(bind=engine)
    # Seed baseline districts, skills, and courses if table is empty
    with Session(engine) as db:
        from app.models.location import District
        if db.query(District).count() == 0:
            seed_database(db)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="Labour Market Intelligence and Curriculum Alignment Platform for Maharashtra",
    lifespan=lifespan
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "status": "online",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

@app.get("/health")
@app.get(f"{settings.API_V1_STR}/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
            "project": settings.PROJECT_NAME
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": str(e)
        }
