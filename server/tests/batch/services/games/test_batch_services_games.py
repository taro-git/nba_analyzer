from datetime import datetime
from typing import Any

import pytest
from nba_api.stats.endpoints.leaguegamefinder import LeagueGameFinder
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2
from pytest_mock import MockerFixture

from batch.services.games.games import (
    get_games_by_start_datetime,
    get_unninitialized_games_by_start_datetime,
    sync_games_by_season,
)
from batch.types import Season
from common.models.games.games import Game
from common.models.games.stats import Stats
from common.models.teams.teams import Team
from common.types import GameCategory, GameStatus

HOME_TEAM_ID = 1
AWAY_TEAM_ID = 2
NOT_EXSITING_TEAM_ID = 3


def mocker_patch(
    mocker: MockerFixture,
    mock_league_game_finder: dict[str, Any],
    mock_schedule_league_v2: dict[str, Any],
    mock_games: list[Game],
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

    mocker.patch(
        "batch.services.games.games.get_games_by_season",
        return_value=mock_games,
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


def _build_game(
    id: int, game_id: str | None = None, start_epoc_sec: int = 1767193200, status: GameStatus = GameStatus.final
) -> Game:
    return Game(
        id=id,
        game_id=game_id or f"00225{id}",
        season=2025,
        start_epoc_sec=start_epoc_sec,
        elapsed_sec=0,
        status=status,
        category=GameCategory.regular_season,
        home_team_id=HOME_TEAM_ID,
        away_team_id=AWAY_TEAM_ID,
        home_score=110,
        away_score=105,
        playoff_label=None,
    )


@pytest.mark.parametrize(
    "api_game_ids, db_game_ids, expected_add_count, expected_remove_count",
    [
        ([], [], 0, 0),
        (["0012400001"], [], 1, 0),
        (["0012400001", "0042400002"], [], 2, 0),
        (["0012400001"], ["0012400001", "0042400002"], 1, 1),
        (["0012400001"], ["0012400001", "0042400002", "0042400003"], 1, 2),
    ],
)
def test_sync_games_normal(
    mocker: MockerFixture,
    api_game_ids: list[str],
    db_game_ids: list[str],
    expected_add_count: int,
    expected_remove_count: int,
) -> None:
    mocker_patch(
        mocker,
        build_league_game_finder(api_game_ids),
        build_schedule_league_v2(game_ids=api_game_ids),
        [_build_game(id=i, game_id=id) for i, id in enumerate(db_game_ids)],
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")
    remove_mock = mocker.patch("batch.services.games.games.remove_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    remove_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    removed = remove_mock.call_args[0][0]
    assert len(added) == expected_add_count
    assert len(removed) == expected_remove_count
    for game in added:
        if GameCategory.from_game_id(game.game_id) != GameCategory.playoffs:
            assert game.playoff_label is None
        else:
            assert game.playoff_label is not None


def test_sync_games_error_on_invalid_league_game_finder_response(mocker: MockerFixture) -> None:
    mocker_patch(mocker, {"resultSets": []}, build_schedule_league_v2(game_ids=["0012400001"]), [])

    with pytest.raises(IndexError):
        sync_games_by_season(Season.from_start_year(2024))


def test_sync_games_error_on_invalid_schedule_league_v2_response(mocker: MockerFixture) -> None:
    mocker_patch(mocker, build_league_game_finder(["0012400001"]), {"leagueSchedule": {}}, [])

    with pytest.raises(TypeError):
        sync_games_by_season(Season.from_start_year(2024))


def test_sync_games_elapsed_sec_is_zero_on_not_found_game_in_league_game_finder(mocker: MockerFixture) -> None:
    mocker_patch(
        mocker, build_league_game_finder(["0012400002"]), build_schedule_league_v2(game_ids=["0012400001"]), []
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")
    remove_mock = mocker.patch("batch.services.games.games.remove_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    remove_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    removed = remove_mock.call_args[0][0]
    assert len(added) == 1
    assert len(removed) == 0
    assert added[0].elapsed_sec == 0


def test_sync_games_no_action_on_same_team_id(mocker: MockerFixture) -> None:
    mocker_patch(
        mocker,
        build_league_game_finder(["0012400001"]),
        build_schedule_league_v2(game_ids=["0012400001"], away_team_id=HOME_TEAM_ID),
        [],
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")
    remove_mock = mocker.patch("batch.services.games.games.remove_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    remove_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    removed = remove_mock.call_args[0][0]
    assert len(added) == 0
    assert len(removed) == 0


def test_sync_games_no_action_on_home_team_id_is_not_existing_in_db(mocker: MockerFixture) -> None:
    mocker_patch(
        mocker,
        build_league_game_finder(["0012400001"]),
        build_schedule_league_v2(game_ids=["0012400001"], home_team_id=NOT_EXSITING_TEAM_ID, away_team_id=AWAY_TEAM_ID),
        [],
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")
    remove_mock = mocker.patch("batch.services.games.games.remove_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    remove_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    removed = remove_mock.call_args[0][0]
    assert len(added) == 0
    assert len(removed) == 0


def test_sync_games_no_action_on_away_team_id_is_not_existing_in_db(mocker: MockerFixture) -> None:
    mocker_patch(
        mocker,
        build_league_game_finder(["0012400001"]),
        build_schedule_league_v2(game_ids=["0012400001"], home_team_id=HOME_TEAM_ID, away_team_id=NOT_EXSITING_TEAM_ID),
        [],
    )

    add_mock = mocker.patch("batch.services.games.games.upsert_games")
    remove_mock = mocker.patch("batch.services.games.games.remove_games")

    sync_games_by_season(Season.from_start_year(2024))

    add_mock.assert_called_once()
    remove_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    removed = remove_mock.call_args[0][0]
    assert len(added) == 0
    assert len(removed) == 0


def _build_stats(game_id: int) -> Stats:
    return Stats(
        game_id=game_id,
        game_player_id=0,
        elapsed_ms=0,
        ms=0,
        points=0,
        offence_rebounds=0,
        diffence_rebounds=0,
        assists=0,
        steals=0,
        blocks=0,
        field_goal_attempts=0,
        field_goal_made=0,
        three_point_attempts=0,
        three_point_made=0,
        free_throw_attempts=0,
        free_throw_made=0,
        turnovers=0,
        personal_fouls=0,
        plus_minus=0,
    )


def test_get_games_by_start_datetime_returns_expected(mocker: MockerFixture) -> None:
    start_epoc = 1767193200
    status = GameStatus.final
    expected = [_build_game(1, start_epoc_sec=start_epoc, status=status)]
    add_mock = mocker.patch("batch.services.games.games.get_games_by_start_datetime_from_db", return_value=expected)

    result = get_games_by_start_datetime(datetime.fromtimestamp(start_epoc), datetime.fromtimestamp(start_epoc), status)

    add_mock.assert_called_once()
    assert {g.game_id for g in result} == {g.game_id for g in expected}


@pytest.mark.parametrize(
    "game_ids, game_ids_of_stats, expected_game_ids",
    [
        ([], [], {}),
        ([1], [1], {}),
        ([1], [], {1}),
        ([1, 2, 3], [1, 2, 3], {}),
        ([1, 2, 3], [], {1, 2, 3}),
        ([1, 2, 3], [2], {1, 3}),
    ],
)
def test_get_unninitialized_games_by_start_datetime_returns_matched(
    mocker: MockerFixture, game_ids: list[int], game_ids_of_stats: list[int], expected_game_ids: set[int]
) -> None:
    game_mock = mocker.patch(
        "batch.services.games.games.get_games_by_start_datetime_from_db",
        return_value=[_build_game(id) for id in game_ids],
    )
    stats_mock = mocker.patch(
        "batch.services.games.games.get_all_game_ids_of_stats",
        return_value=[_build_stats(id).game_id for id in game_ids_of_stats],
    )
    actions_mock = mocker.patch(
        "batch.services.games.games.get_all_game_ids_of_actions",
        return_value=[_build_stats(id).game_id for id in game_ids_of_stats],
    )
    result = get_unninitialized_games_by_start_datetime(
        datetime.fromtimestamp(1767193200), datetime.fromtimestamp(1767193200), GameStatus.final
    )

    game_mock.assert_called_once()
    stats_mock.assert_called_once()
    actions_mock.assert_called_once()
    assert {g.id for g in result} == set(expected_game_ids)
