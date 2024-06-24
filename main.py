import uvicorn
import logging

from fastapi import FastAPI
from app.api import router
from logger.logger_config import setup_logging

API_PREFIX = ""

logger = logging.getLogger("Blog_fastapi")


# define application
def get_application() -> FastAPI:
    application = FastAPI(
        title="blog_fastapi",
        docs_url="/docs",
        redoc_url="/re-docs",
        openapi_url=f"{API_PREFIX}/openapi.json",
        description="""
        Just no document...
        """,
    )
    application.include_router(router, prefix=API_PREFIX)

    return application


app = get_application()
if __name__ == "__main__":
    setup_logging()
    logging.basicConfig(level="INFO")
    logger.info("Starting Blog_fastapi sever...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
