from fastapi import APIRouter
from backend.api import config

root_router = APIRouter()

root_router.include_router(config.router, prefix="/config", tags=["config"])