from datetime import datetime, timezone

import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlmodel import Session, select

from batch.repositories.commons.caches import (
    add_cache,
    get_cache_by_hash,
    get_expired_caches,
    remove_cache,
    remove_caches,
)
from common.models.commons.caches import Cache


@pytest.fixture
def seed_caches(session: Session) -> None:
    caches = [
        Cache(
            request_hash=111,
            response={"response": 111},
            expires_at=datetime(2022, 1, 1, 0, 0).astimezone(tz=timezone.utc),
        ),
        Cache(
            request_hash=222,
            response={"response": 222},
            expires_at=datetime(2022, 1, 1, 0, 0).astimezone(tz=timezone.utc),
        ),
        Cache(
            request_hash=333,
            response={"response": 333},
            expires_at=datetime(2023, 1, 1, 0, 0).astimezone(tz=timezone.utc),
        ),
        Cache(
            request_hash=444,
            response={"response": 444},
            expires_at=datetime(2023, 1, 1, 0, 0).astimezone(tz=timezone.utc),
        ),
    ]
    session.add_all(caches)
    session.commit()


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> Engine:
    mocker.patch("batch.repositories.commons.caches.engine", engine)
    return engine


def test_get_cache_by_hash_returns_hit_cache(mock_engine: Engine, seed_caches: None) -> None:
    result = get_cache_by_hash(111)
    assert result is not None
    assert result.response == {"response": 111}


def test_get_cache_by_hash_returns_none(mock_engine: Engine, seed_caches: None) -> None:
    result = get_cache_by_hash(555)
    assert result is None


def test_get_expired_caches_returns_expired_caches(mock_engine: Engine, seed_caches: None) -> None:
    result = get_expired_caches(datetime(2022, 1, 2, 0, 0).astimezone(tz=timezone.utc))
    assert len(result) == 2
    assert result[0].response == {"response": 111}
    assert result[1].response == {"response": 222}


def test_get_expired_caches_returns_empty_list(mock_engine: Engine, seed_caches: None) -> None:
    result = get_expired_caches(datetime(2021, 1, 1, 0, 0).astimezone(tz=timezone.utc))
    assert len(result) == 0


def test_add_cache_adds_new_cache(mock_engine: Engine, seed_caches: None) -> None:
    add_cache(
        Cache(
            request_hash=555,
            response={"response": 555},
            expires_at=datetime(2022, 1, 1, 0, 0).astimezone(tz=timezone.utc),
        )
    )

    with Session(mock_engine) as session:
        result = session.exec(select(Cache)).all()

    assert len(result) == 5
    assert result[4].response == {"response": 555}


def test_add_cache_error_in_duplicate_hash(mock_engine: Engine, seed_caches: None) -> None:
    with pytest.raises(IntegrityError):
        add_cache(
            Cache(
                request_hash=111,
                response={"response": 555},
                expires_at=datetime(2022, 1, 1, 0, 0).astimezone(tz=timezone.utc),
            )
        )


def test_remove_cache_removes_cache(mock_engine: Engine, seed_caches: None) -> None:
    cache = get_cache_by_hash(111)
    assert cache is not None
    remove_cache(cache)

    with Session(mock_engine) as session:
        result = session.exec(select(Cache)).all()

    assert len(result) == 3


def test_remove_cache_error_in_cache_not_from_db(mock_engine: Engine, seed_caches: None) -> None:
    with pytest.raises(InvalidRequestError):
        remove_cache(
            Cache(
                request_hash=111,
                response={"response": 111},
                expires_at=datetime(2022, 1, 1, 0, 0).astimezone(tz=timezone.utc),
            )
        )


def test_remove_caches_removes_caches(mock_engine: Engine, seed_caches: None) -> None:
    cache_1 = get_cache_by_hash(111)
    cache_2 = get_cache_by_hash(222)
    assert cache_1 is not None and cache_2 is not None
    remove_caches([cache_1, cache_2])

    with Session(mock_engine) as session:
        result = session.exec(select(Cache)).all()

    assert len(result) == 2


def test_remove_caches_not_action_if_empty(mock_engine: Engine, seed_caches: None) -> None:
    remove_caches([])

    with Session(mock_engine) as session:
        result = session.exec(select(Cache)).all()

    assert len(result) == 4


def test_remove_caches_error_in_cache_not_from_db(mock_engine: Engine, seed_caches: None) -> None:
    cache = get_cache_by_hash(111)
    assert cache is not None
    with pytest.raises(InvalidRequestError):
        remove_caches(
            [
                cache,
                Cache(
                    request_hash=222,
                    response={"response": 222},
                    expires_at=datetime(2022, 1, 1, 0, 0).astimezone(tz=timezone.utc),
                ),
            ]
        )


def test_remove_caches_error_in_duplicate_hash(mock_engine: Engine, seed_caches: None) -> None:
    cache = get_cache_by_hash(111)
    assert cache is not None
    with pytest.raises(ValueError):
        remove_caches([cache, cache])
