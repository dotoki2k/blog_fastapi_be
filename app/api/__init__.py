from fastapi import APIRouter

from .auth import router as auth_router
from .log import router as log_router


router = APIRouter()

router.include_router(auth_router, tags=["health-check"])
router.include_router(log_router, tags=["log"])
