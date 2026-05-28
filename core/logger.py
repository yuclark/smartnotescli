import logging
import os

LOG_FILE = "app.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_info(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message, exc_info=True)