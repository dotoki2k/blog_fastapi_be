import logging
import json
import pathlib
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, Annotated
from enum import Enum
from logger.logger_config import setup_logging
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
logger = logging.getLogger("log")


class LogLevel(str, Enum):
    NOTSET = "NOTSET"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@router.get("/log_information")
async def get_log_information():
    """Get log information."""
    log_config = {}
    config = {}
    config_file = pathlib.Path("logger/logger_config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)

    log_config.update({"level": config["loggers"]["root"]["level"]})
    log_config.update({"maxBytes": config["handlers"]["file"]["maxBytes"]})
    log_config.update({"backupCount": config["handlers"]["file"]["backupCount"]})

    return log_config


jwt_auth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


@router.put("/log_level", summary="Edit log config", dependencies=[Depends(jwt_auth)])
async def set_log_config(
    log_level: LogLevel,
    maxBytes: Annotated[int, Query(title="Max bytes of log file", gt=0)] = 10000,
    backupCount: Annotated[int, Query(title="Max file backup of log file", gt=0)] = 5,
):
    """set log config."""
    try:
        config = {}
        config_file = pathlib.Path("logger/logger_config.json")
        with open(config_file) as f_in:
            config = json.load(f_in)

        with open(config_file, "w") as f_write:
            config["loggers"]["root"]["level"] = log_level
            config["handlers"]["file"]["maxBytes"] = maxBytes
            config["handlers"]["file"]["backupCount"] = backupCount
            json.dump(config, f_write, indent=4)

        setup_logging()
        return "Update log level successfully!"
    except Exception as e:
        logger.exception("An error occurred when setting log level")
        raise HTTPException(
            status_code=400, detail=f"error occurred when set log level - {str(e)}"
        )
