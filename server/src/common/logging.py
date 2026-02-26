import logging
import sys
from typing import Literal


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[36m",
        logging.INFO: "\033[32m",
        logging.WARNING: "\033[33m",
        logging.ERROR: "\033[31m",
        logging.CRITICAL: "\033[1;31m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        message = record.getMessage().replace("\n", " \\ ")
        record.message = message
        color = self.COLORS.get(record.levelno, "")
        formatted = f"{self.formatTime(record)} | {record.levelname} | {record.name} | {message}"
        return f"{color}{formatted}{self.RESET}"


def setup_logging(additional_loggers: dict[str, Literal[10, 20, 30, 40, 50]] | None = None) -> None:
    """
    logging をセットアップします.
    addtional_loggers には追加ロガー名とログレベルを辞書型で指定します.
    """
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(ColorFormatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)

    if additional_loggers is not None:
        for name, level in additional_loggers.items():
            log = logging.getLogger(name)
            log.handlers = []
            log.propagate = True
            log.setLevel(level)
