from typing import Any, Generator

import pytest
from sqlmodel import Session, SQLModel, create_engine

from common.models.commons.seasons import Season  # type: ignore # noqa: F401


@pytest.fixture
def session() -> Generator[Session, Any, None]:
    """
    各テストで使用する DB セッション
    """
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
