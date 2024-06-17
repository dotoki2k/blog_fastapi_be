import json
import logging.config
import logging.handlers
import pathlib


def setup_logging():
    config_file = pathlib.Path("logger/logger_config.json")
    with open(config_file) as f_in:
        config = json.load(f_in)
    logging.config.dictConfig(config)
