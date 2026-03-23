from typing import Any

import pytest
from nba_api.stats.endpoints.leaguegamefinder import LeagueGameFinder
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2
from pytest_mock import MockerFixture

from batch.services.games.games import sync_games_by_season
from batch.types import Season
from common.models.teams.teams import Team
from common.types import GameCategory

HOME_TEAM_ID = 1
AWAY_TEAM_ID = 2
NOT_EXSITING_TEAM_ID = 3


def mocker_patch(
    mocker: MockerFixture,
    mock_league_game_finder: dict[str, Any],
    mock_schedule_league_v2: dict[str, Any],
) -> None:
    mocker.patch("batch.services.games.games.get_teams", return_value=[Team(id=HOME_TEAM_ID), Team(id=AWAY_TEAM_ID)])

    def fetch_side_effect(
        endpoint_cls: type[LeagueGameFinder] | type[ScheduleLeagueV2], *args: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        if endpoint_cls is LeagueGameFinder:
            return mock_league_game_finder
        if endpoint_cls is ScheduleLeagueV2:
            return mock_schedule_league_v2
        raise ValueError(f"Unexpected endpoint_cls: {endpoint_cls}")

    mocker.patch(
        "batch.services.games.games.NbaApiGateway.fetch",
        side_effect=fetch_side_effect,
    )

    mocker.patch(
        "batch.services.games.games.upsert_games",
        return_value=None,
    )


def build_league_game_finder(game_ids: list[str]) -> dict[str, Any]:
    return {"resultSets": [{"headers": ["GAME_ID", "MIN"], "rowSet": [[id, 48 * 60 * 5] for id in game_ids]}]}


def build_schedule_league_v2(
    *, game_ids: list[str], home_team_id: int = HOME_TEAM_ID, away_team_id: int = AWAY_TEAM_ID
) -> dict[str, Any]:
    return {
        "leagueSchedule": {
            "gameDates": [
                {
                    "games": [
                        {
                            "gameId": id,
                            "gameDateTimeUTC": "2026-01-15T23:30:00Z",
                            "gameStatus": 1,
                            "homeTeam": {"teamId": home_team_id, "score": 0},
                            "awayTeam": {"teamId": away_team_id, "score": 0},
                            "gameLabel": "game label",
                            "gameSubLabel": "game sub label",
                        }
                        for id in game_ids
                    ]
                }
            ]
        }
    }


@pytest.mark.parametrize(
    "api_game_ids, expected_add_count",
    [
        ([], 0),
        (["0012400001"], 1),
        (["0012400001", "0042400002"], 2),
    ],
)
def test_sync_games_normal(
    mocker: MockerFixture,
    api_game_ids: list[str],
    expected_add_count: int,
) -> None:
    mocker_patch(mocker, build_league_game_finder(api_game_ids), build_schedule_league_v2(game_ids=api_game_ids))

    add_mock = mocker.patch("batch.services.games.games.upsert_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    assert len(added) == expected_add_count
    for game in added:
        if GameCategory.from_game_id(game.game_id) != GameCategory.playoffs:
            assert game.playoff_label is None
        else:
            assert game.playoff_label is not None


def test_sync_games_error_on_invalid_league_game_finder_response(mocker: MockerFixture) -> None:
    mocker_patch(mocker, {"resultSets": []}, build_schedule_league_v2(game_ids=["0012400001"]))

    with pytest.raises(IndexError):
        sync_games_by_season(Season.from_start_year(2024))


def test_sync_games_error_on_invalid_schedule_league_v2_response(mocker: MockerFixture) -> None:
    mocker_patch(mocker, build_league_game_finder(["0012400001"]), {"leagueSchedule": {}})

    with pytest.raises(TypeError):
        sync_games_by_season(Season.from_start_year(2024))


def test_sync_games_elapsed_sec_is_zero_on_not_found_game_in_league_game_finder(mocker: MockerFixture) -> None:
    mocker_patch(mocker, build_league_game_finder(["0012400002"]), build_schedule_league_v2(game_ids=["0012400001"]))

    add_mock = mocker.patch("batch.services.games.games.upsert_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    assert len(added) == 1
    assert added[0].elapsed_sec == 0


def test_sync_games_no_action_on_same_team_id(mocker: MockerFixture) -> None:
    mocker_patch(
        mocker,
        build_league_game_finder(["0012400001"]),
        build_schedule_league_v2(game_ids=["0012400001"], away_team_id=HOME_TEAM_ID),
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    assert len(added) == 0


def test_sync_games_no_action_on_home_team_id_is_not_existing_in_db(mocker: MockerFixture) -> None:
    mocker_patch(
        mocker,
        build_league_game_finder(["0012400001"]),
        build_schedule_league_v2(game_ids=["0012400001"], home_team_id=NOT_EXSITING_TEAM_ID, away_team_id=AWAY_TEAM_ID),
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    assert len(added) == 0


def test_sync_games_no_action_on_away_team_id_is_not_existing_in_db(mocker: MockerFixture) -> None:
    mocker_patch(
        mocker,
        build_league_game_finder(["0012400001"]),
        build_schedule_league_v2(game_ids=["0012400001"], home_team_id=HOME_TEAM_ID, away_team_id=NOT_EXSITING_TEAM_ID),
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    assert len(added) == 0
