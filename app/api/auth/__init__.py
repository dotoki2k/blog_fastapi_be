import logging
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger("test")


@router.get("/healthcheck")
async def get():
    """Check system health."""
    logger.debug("log debug")
    logger.info("log info")
    logger.warning("log warning")
    logger.error("log error")
    logger.critical("log critical")
    return {"message": "Health check success"}
