"""
review_system/utils/logging_utils.py

Dedicated review-system logging.
Creates four separate rotating log files inside review_system/logs/:
  review_run.log        — top-level pipeline progress
  claim_extraction.log  — claim extraction step
  review_generation.log — output generation step
  error.log             — all ERROR and above across the whole system
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from review_system.config.review_config import LOG_FILES

# Logs directory is always relative to the review_system package root
_LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"

# Max 5 MB per file, keep 3 rotations
_MAX_BYTES = 5 * 1024 * 1024
_BACKUP_COUNT = 3

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_initialised: set[str] = set()


def _ensure_logs_dir() -> None:
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)


def _make_handler(log_file: str, level: int = logging.DEBUG) -> RotatingFileHandler:
    _ensure_logs_dir()
    handler = RotatingFileHandler(
        _LOGS_DIR / log_file,
        maxBytes=_MAX_BYTES,
        backupCount=_BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATE_FORMAT))
    return handler


def _stderr_handler(level: int = logging.INFO) -> logging.StreamHandler:
    h = logging.StreamHandler(sys.stderr)
    h.setLevel(level)
    h.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))
    return h


def get_run_logger() -> logging.Logger:
    """Logger for top-level pipeline progress — writes to review_run.log."""
    name = "review.run"
    if name in _initialised:
        return logging.getLogger(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_make_handler(LOG_FILES["run"]))
    logger.addHandler(_make_handler(LOG_FILES["error"], level=logging.ERROR))
    logger.addHandler(_stderr_handler())
    logger.propagate = False
    _initialised.add(name)
    return logger


def get_claims_logger() -> logging.Logger:
    """Logger for claim extraction step — writes to claim_extraction.log."""
    name = "review.claims"
    if name in _initialised:
        return logging.getLogger(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_make_handler(LOG_FILES["claims"]))
    logger.addHandler(_make_handler(LOG_FILES["error"], level=logging.ERROR))
    logger.propagate = False
    _initialised.add(name)
    return logger


def get_generation_logger() -> logging.Logger:
    """Logger for output generation step — writes to review_generation.log."""
    name = "review.generation"
    if name in _initialised:
        return logging.getLogger(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(_make_handler(LOG_FILES["generation"]))
    logger.addHandler(_make_handler(LOG_FILES["error"], level=logging.ERROR))
    logger.propagate = False
    _initialised.add(name)
    return logger


def get_error_logger() -> logging.Logger:
    """Logger for errors only — writes to error.log."""
    name = "review.error"
    if name in _initialised:
        return logging.getLogger(name)
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.addHandler(_make_handler(LOG_FILES["error"], level=logging.ERROR))
    logger.addHandler(_stderr_handler(level=logging.ERROR))
    logger.propagate = False
    _initialised.add(name)
    return logger
