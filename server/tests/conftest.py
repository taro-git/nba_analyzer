from typing import Any, Generator

import pytest
from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine

from common.models.commons.seasons import Season  # type: ignore # noqa: F401


@pytest.fixture
def engine() -> Engine:
    return create_engine("sqlite:///:memory:")


@pytest.fixture
def session(engine: Engine) -> Generator[Session, Any, None]:
    """
    各テストで使用する DB セッション
    """
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
