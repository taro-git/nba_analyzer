import pytest
from pytest_mock import MockerFixture

from batch.services.commons.seasons import sync_seasons
from batch.types import Season
from common.models.commons.seasons import Season as SeasonModel


def test_sync_seasons_newest_none(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.commons.seasons.get_newest_season",
        return_value=None,
    )
    mock_add = mocker.patch("batch.services.commons.seasons.add_seasons")

    season = Season.from_start_year(1972)

    sync_seasons(season)

    passed = mock_add.call_args[0][0]
    assert [s.start_year for s in passed] == [1970, 1971, 1972]


def test_sync_seasons_add_missing(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.commons.seasons.get_newest_season",
        return_value=SeasonModel(start_year=2020),
    )
    mock_add = mocker.patch("batch.services.commons.seasons.add_seasons")

    season = Season.from_start_year(2023)

    sync_seasons(season)

    passed = mock_add.call_args[0][0]
    assert [s.start_year for s in passed] == [2021, 2022, 2023]


def test_sync_seasons_no_add_when_equal(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.commons.seasons.get_newest_season",
        return_value=SeasonModel(start_year=2023),
    )
    mock_add = mocker.patch("batch.services.commons.seasons.add_seasons")

    season = Season.from_start_year(2023)

    sync_seasons(season)

    mock_add.assert_not_called()


def test_sync_seasons_no_add_when_newer_exists(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.commons.seasons.get_newest_season",
        return_value=SeasonModel(start_year=2025),
    )
    mock_add = mocker.patch("batch.services.commons.seasons.add_seasons")

    season = Season.from_start_year(2023)

    sync_seasons(season)

    mock_add.assert_not_called()


def test_sync_seasons_with_none_argument(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.commons.seasons.get_newest_season",
        return_value=SeasonModel(start_year=2020),
    )
    mock_add = mocker.patch("batch.services.commons.seasons.add_seasons")

    mocker.patch(
        "batch.services.commons.seasons.Season.from_datetime",
        return_value=Season.from_start_year(2022),
    )

    sync_seasons(None)

    passed = mock_add.call_args[0][0]
    assert [s.start_year for s in passed] == [2021, 2022]


def test_sync_seasons_get_newest_error(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.commons.seasons.get_newest_season",
        side_effect=RuntimeError("db error"),
    )

    with pytest.raises(RuntimeError):
        sync_seasons(Season.from_start_year(2023))


def test_sync_seasons_add_error(mocker: MockerFixture) -> None:

    mocker.patch(
        "batch.services.commons.seasons.get_newest_season",
        return_value=SeasonModel(start_year=2020),
    )

    mocker.patch(
        "batch.services.commons.seasons.add_seasons",
        side_effect=RuntimeError("insert error"),
    )

    with pytest.raises(RuntimeError):
        sync_seasons(Season.from_start_year(2023))
