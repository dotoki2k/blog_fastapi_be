import logging
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger("test")


@router.get("/healthcheck")
async def get():
    """Check system health."""
    logger.info("Start checking system health...")
    logger.info("Health check success...")
    return {"message": "Health check success"}
