from fastapi import APIRouter
from app.api.endpoints import common, todos

router = APIRouter()
router.include_router(common.router)
router.include_router(todos.router)