import logging
import sys
from logging.handlers import RotatingFileHandler

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        "app.log",        # основной файл
        maxBytes=10 * 1024 * 1024,  # 10 МБ максимум
        backupCount=1,    # хранить app.log, app.log.1,
        encoding="utf-8"
    )
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler.setFormatter(formatter)

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


