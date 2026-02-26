from datetime import datetime, timezone

import pytest
from pytest_mock import MockerFixture

from batch.services.commons.caches import remove_expired_caches


def test_remove_expired_caches_with_now(mocker: MockerFixture) -> None:
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    expired = ["cache1", "cache2"]
    mock_get = mocker.patch(
        "batch.services.commons.caches.get_expired_caches",
        return_value=expired,
    )
    mock_remove = mocker.patch(
        "batch.services.commons.caches.remove_caches",
    )
    remove_expired_caches(now)
    mock_get.assert_called_once_with(now)
    mock_remove.assert_called_once_with(expired)


def test_remove_expired_caches_without_now(mocker: MockerFixture) -> None:
    fixed_now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    mocker.patch(
        "batch.services.commons.caches.datetime",
    )
    mocker.patch(
        "batch.services.commons.caches.datetime.now",
        return_value=fixed_now,
    )
    expired = ["cache1"]
    mock_get = mocker.patch(
        "batch.services.commons.caches.get_expired_caches",
        return_value=expired,
    )
    mock_remove = mocker.patch(
        "batch.services.commons.caches.remove_caches",
    )
    remove_expired_caches(None)
    mock_get.assert_called_once_with(fixed_now)
    mock_remove.assert_called_once_with(expired)


def test_remove_expired_caches_get_error(mocker: MockerFixture) -> None:
    mocker.patch(
        "batch.services.commons.caches.get_expired_caches",
        side_effect=RuntimeError("db error"),
    )
    with pytest.raises(RuntimeError):
        remove_expired_caches(datetime.now(timezone.utc))


def test_remove_expired_caches_remove_error(mocker: MockerFixture) -> None:
    mocker.patch(
        "batch.services.commons.caches.get_expired_caches",
        return_value=["cache1"],
    )
    mocker.patch(
        "batch.services.commons.caches.remove_caches",
        side_effect=RuntimeError("delete error"),
    )
    with pytest.raises(RuntimeError):
        remove_expired_caches(datetime.now(timezone.utc))
