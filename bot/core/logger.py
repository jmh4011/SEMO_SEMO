import logging
import os
from logging.handlers import TimedRotatingFileHandler

try:
    from fluent.handler import FluentHandler

    fluent_available = True
except ImportError:
    fluent_available = False

LOG_DIR = "logs"
LOG_FILE = "discord.log"


def setup_logger(env: str = "default", log_level: str = "INFO"):
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

    file_handler = TimedRotatingFileHandler(
        filename=os.path.join(LOG_DIR, LOG_FILE),
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if fluent_available:
        try:
            fluent_handler = FluentHandler(
                tag=f"discord.{env}",
                host="fluentd",
                port=24224,
                buffer_overflow_handler=lambda _: None,
            )
            fluent_handler.setFormatter(logging.Formatter("%(message)s"))
            logger.addHandler(fluent_handler)
        except Exception:
            pass
