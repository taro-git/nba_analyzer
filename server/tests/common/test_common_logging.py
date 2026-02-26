import logging
import sys
from typing import Any, Generator

import pytest

from common.logging import setup_logging


@pytest.fixture(autouse=True)
def reset_logging() -> Generator[Any, Any, Any]:
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.NOTSET)
    yield
    root.handlers.clear()
    root.setLevel(logging.NOTSET)


def test_setup_logging_root_handler() -> None:
    setup_logging()
    root = logging.getLogger()

    assert root.level == logging.INFO
    stream_handlers: list[logging.Handler] = [
        h for h in root.handlers if not h.__class__.__name__ == "LogCaptureHandler"
    ]
    assert len(stream_handlers) == 1
    assert stream_handlers[0].__class__.__name__ == "StreamHandler"
    assert stream_handlers[0].stream is sys.stdout  # type: ignore


def test_setup_logging_add_one_logger() -> None:
    setup_logging(
        {
            "test_logger": logging.WARNING,
        }
    )

    test_logger = logging.getLogger("test_logger")

    assert test_logger.level == logging.WARNING
    assert test_logger.handlers == []
    assert test_logger.propagate is True


def test_setup_logging_add_some_loggers() -> None:
    setup_logging(
        {
            "test_logger.1": logging.ERROR,
            "test_logger.2": logging.WARNING,
        }
    )

    test_logger_1 = logging.getLogger("test_logger.1")
    test_logger_2 = logging.getLogger("test_logger.2")

    assert test_logger_1.level == logging.ERROR
    assert test_logger_2.level == logging.WARNING

    assert test_logger_1.handlers == []
    assert test_logger_2.handlers == []

    assert test_logger_1.propagate is True
    assert test_logger_2.propagate is True
