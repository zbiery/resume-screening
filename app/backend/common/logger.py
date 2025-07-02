import sys
import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .config import AppConfig

CONFIG = AppConfig()

def get_logger(name: str) -> logging.Logger:
    log_level_str = CONFIG.log_level
    log_level = getattr(logging, log_level_str, logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        # Ensure the logs directory exists
        log_dir = Path(__file__).parent.parent.parent / 'logs' 
        log_dir.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Console output
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(log_level)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        # Rotating file handler
        log_file_path = log_dir / "app.log"
        fh = RotatingFileHandler(log_file_path, maxBytes=5_000_000, backupCount=5)
        fh.setLevel(log_level)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        logger.propagate = False

    return logger
