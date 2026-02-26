from typing import Any

import pytest
from nba_api.stats.endpoints.leaguestandingsv3 import LeagueStandingsV3
from pytest_mock import MockerFixture

from batch.services.teams.regular_season_team_standings import (
    sync_regular_season_team_standings_by_season,
)
from batch.types import Season
from common.models.teams.regular_season_team_standings import (
    RegularSeasonTeamStanding,
)


def mocker_patch(
    mocker: MockerFixture,
    mock_league_standings_v3: dict[str, Any],
) -> None:
    def fetch_side_effect(
        endpoint_cls: type[LeagueStandingsV3], *args: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        if endpoint_cls is LeagueStandingsV3:
            return mock_league_standings_v3
        raise ValueError(f"Unexpected endpoint_cls: {endpoint_cls}")

    mocker.patch(
        "batch.services.teams.regular_season_team_standings.NbaApiGateway.fetch",
        side_effect=fetch_side_effect,
    )

    mocker.patch(
        "batch.services.teams.regular_season_team_standings.upsert_regular_season_team_standings",
        return_value=None,
    )


@pytest.fixture
def season() -> Season:
    return Season.from_season_str("2023-24")


def build_standings(rows: list[list[Any]]) -> dict[str, Any]:
    return {
        "resultSets": [
            {
                "headers": [
                    "TeamID",
                    "PlayoffRank",
                    "WINS",
                    "LOSSES",
                ],
                "rowSet": rows,
            }
        ]
    }


@pytest.mark.parametrize(
    "rows, expected_count",
    [
        ([], 0),
        ([[1, 1, 50, 32]], 1),
        ([[1, 1, 50, 32], [2, 2, 48, 34]], 2),
    ],
)
def test_sync_regular_season_team_standings_normal(
    mocker: MockerFixture,
    season: Season,
    rows: list[list[Any]],
    expected_count: int,
) -> None:
    mock_standings = build_standings(rows)

    mocker_patch(mocker, mock_standings)

    upsert_mock = mocker.patch(
        "batch.services.teams.regular_season_team_standings.upsert_regular_season_team_standings"
    )

    sync_regular_season_team_standings_by_season(season)

    upsert_mock.assert_called_once()

    passed_models: list[RegularSeasonTeamStanding] = upsert_mock.call_args[0][0]
    assert len(passed_models) == expected_count

    for model, row in zip(passed_models, rows, strict=True):
        assert model.team_id == row[0]
        assert model.rank == row[1]
        assert model.win == row[2]
        assert model.lose == row[3]
        assert model.season == season.start_year


def test_missing_resultsets_key_raises(
    mocker: MockerFixture,
    season: Season,
) -> None:
    mock_standings = {"invalid": "structure"}

    mocker_patch(mocker, mock_standings)

    with pytest.raises(IndexError):
        sync_regular_season_team_standings_by_season(season)


def test_missing_headers_key_raises(
    mocker: MockerFixture,
    season: Season,
) -> None:
    mock_standings: dict[str, Any] = {"resultSets": [{"rowSet": []}]}

    mocker_patch(mocker, mock_standings)

    with pytest.raises(KeyError):
        sync_regular_season_team_standings_by_season(season)


def test_missing_rowset_key_raises(
    mocker: MockerFixture,
    season: Season,
) -> None:
    mock_standings: dict[str, Any] = {"resultSets": [{"headers": []}]}

    mocker_patch(mocker, mock_standings)

    with pytest.raises(KeyError):
        sync_regular_season_team_standings_by_season(season)


def test_season_none_uses_current_datetime(
    mocker: MockerFixture,
) -> None:
    mock_standings = build_standings([[1, 1, 50, 32]])

    mocker_patch(mocker, mock_standings)

    upsert_mock = mocker.patch(
        "batch.services.teams.regular_season_team_standings.upsert_regular_season_team_standings"
    )

    sync_regular_season_team_standings_by_season(None)

    upsert_mock.assert_called_once()
