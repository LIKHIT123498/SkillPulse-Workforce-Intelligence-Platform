from fastapi import APIRouter
from app.api.v1.jobs import router as jobs_router
from app.api.v1.skills import router as skills_router
from app.api.v1.courses import router as courses_router
from app.api.v1.districts import router as districts_router

api_router = APIRouter()
api_router.include_router(jobs_router)
api_router.include_router(skills_router)
api_router.include_router(courses_router)
api_router.include_router(districts_router)
