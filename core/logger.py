import logging
import os

LOG_DIR = "data/logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(module_name):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(f"{LOG_DIR}/{module_name}.log")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
