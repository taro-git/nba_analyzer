from datetime import datetime, timedelta, timezone
from typing import Any

import pytest
from nba_api.stats.endpoints._base import Endpoint as StatsEndpoint
from pytest_mock import MockerFixture

from batch.services.nba_api.gateway import NbaApiGateway
from common.models.commons.caches import Cache


class DummyEndpoint(StatsEndpoint):
    def __init__(self, *args: str, **kwargs: str) -> None:
        self.args = args
        self.kwargs = kwargs

    def get_dict(self) -> dict[str, Any]:
        return {"result": "ok", "args": self.args, "kwargs": self.kwargs}


class ErrorEndpoint(StatsEndpoint):
    def __init__(self, *args: str, **kwargs: str) -> None:
        raise RuntimeError("endpoint error")


def make_cache(response: dict[str, Any], expires_delta_seconds: int) -> Cache:
    return Cache(
        request_hash=123,
        response=response,
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=expires_delta_seconds),
    )


def test_fetch_use_cache(mocker: MockerFixture) -> None:

    response = {"cached": True}
    cache = make_cache(response, 60)

    mocker.patch("batch.services.nba_api.gateway.get_cache_by_hash", return_value=cache)
    mocker.patch("batch.services.nba_api.gateway.remove_cache")
    mocker.patch("batch.services.nba_api.gateway.add_cache")

    result = NbaApiGateway.fetch(DummyEndpoint, season="2024")

    assert result == response


def test_fetch_cache_expired(mocker: MockerFixture) -> None:

    expired_cache = make_cache({"old": True}, -60)

    mock_get = mocker.patch(
        "batch.services.nba_api.gateway.get_cache_by_hash",
        return_value=expired_cache,
    )
    mock_remove = mocker.patch("batch.services.nba_api.gateway.remove_cache")
    mock_add = mocker.patch("batch.services.nba_api.gateway.add_cache")

    result = NbaApiGateway.fetch(DummyEndpoint, season="2024")

    assert result["result"] == "ok"
    mock_get.assert_called_once()
    mock_remove.assert_called_once()
    mock_add.assert_called_once()


def test_fetch_no_cache(mocker: MockerFixture) -> None:

    mock_get = mocker.patch(
        "batch.services.nba_api.gateway.get_cache_by_hash",
        return_value=None,
    )
    mock_add = mocker.patch("batch.services.nba_api.gateway.add_cache")

    result = NbaApiGateway.fetch(DummyEndpoint, season="2024")

    assert result["result"] == "ok"
    mock_get.assert_called_once()
    mock_add.assert_called_once()


def test_fetch_endpoint_error(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.nba_api.gateway.get_cache_by_hash",
        return_value=None,
    )
    mock_add = mocker.patch("batch.services.nba_api.gateway.add_cache")

    with pytest.raises(RuntimeError):
        NbaApiGateway.fetch(ErrorEndpoint)

    mock_add.assert_not_called()


def test_fetch_add_cache_error(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.nba_api.gateway.get_cache_by_hash",
        return_value=None,
    )

    mocker.patch(
        "batch.services.nba_api.gateway.add_cache",
        side_effect=RuntimeError("db error"),
    )

    with pytest.raises(RuntimeError):
        NbaApiGateway.fetch(DummyEndpoint)
