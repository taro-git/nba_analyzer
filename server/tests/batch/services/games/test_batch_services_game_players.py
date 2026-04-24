import pytest
from nba_api.live.nba.endpoints import BoxScore
from nba_api.stats.endpoints import BoxScoreSummaryV3, BoxScoreTraditionalV3
from pytest_mock import MockerFixture

from batch.services.games.game_players import sync_game_players_by_game_id
from common.types import PlayerPosition

GAME_ID = "0022500500"
PLAYER_ID_1 = 1001
PLAYER_ID_2 = 1002


def _build_live_boxscore_response() -> dict[str, object]:
    return {
        "game": {
            "homeTeam": {
                "players": [
                    {
                        "personId": PLAYER_ID_1,
                        "jerseyNum": "23",
                        "position": "PG",
                        "starter": "1",
                        "status": "ACTIVE",
                    }
                ]
            },
            "awayTeam": {
                "players": [
                    {
                        "personId": PLAYER_ID_2,
                        "jerseyNum": "11",
                        "position": "SF",
                        "starter": "1",
                        "status": "ACTIVE",
                    }
                ]
            },
        }
    }


def _build_stats_boxscore_summary_response() -> dict[str, object]:
    return {
        "boxScoreSummary": {
            "homeTeam": {
                "players": [{"personId": PLAYER_ID_1, "jerseyNum": "23"}],
                "inactives": [],
            },
            "awayTeam": {
                "players": [{"personId": PLAYER_ID_2, "jerseyNum": "11"}],
                "inactives": [],
            },
        }
    }


def _build_stats_boxscore_traditional_response() -> dict[str, object]:
    return {
        "boxScoreTraditional": {
            "homeTeam": {"players": [{"personId": PLAYER_ID_1, "position": "PG"}]},
            "awayTeam": {"players": [{"personId": PLAYER_ID_2, "position": "SF"}]},
        }
    }


def test_sync_game_players_by_game_id_with_live_endpoint(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.games.game_players.get_game_by_game_id", return_value=seed_game)
    mocker.patch(
        "batch.services.games.game_players.NbaApiGateway.fetch",
        return_value=_build_live_boxscore_response(),
    )
    add_mock = mocker.patch("batch.services.games.game_players.add_game_players_and_ignore_existing")

    sync_game_players_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    players = add_mock.call_args[0][0]
    assert len(players) == 2
    home_player = next(p for p in players if p.player_id == PLAYER_ID_1)
    away_player = next(p for p in players if p.player_id == PLAYER_ID_2)
    assert home_player.is_home is True
    assert home_player.is_starter is True
    assert home_player.is_active is True
    assert home_player.position == PlayerPosition.point_guard
    assert away_player.is_home is False


def test_sync_game_players_by_game_id_with_stats_endpoint_fallback(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.games.game_players.get_game_by_game_id", return_value=seed_game)

    def fetch_side_effect(
        endpoint_cls: type[BoxScore] | type[BoxScoreSummaryV3] | type[BoxScoreTraditionalV3],
        *args: str,
        **kwargs: str,
    ) -> dict[str, object]:
        if endpoint_cls is BoxScore:
            raise Exception("Live endpoint not available")
        if endpoint_cls is BoxScoreSummaryV3:
            return _build_stats_boxscore_summary_response()
        if endpoint_cls is BoxScoreTraditionalV3:
            return _build_stats_boxscore_traditional_response()
        raise ValueError(f"Unexpected endpoint: {endpoint_cls}")

    mocker.patch("batch.services.games.game_players.NbaApiGateway.fetch", side_effect=fetch_side_effect)
    add_mock = mocker.patch("batch.services.games.game_players.add_game_players_and_ignore_existing")

    sync_game_players_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    players = add_mock.call_args[0][0]
    assert len(players) == 2


def test_sync_game_players_by_game_id_error_on_game_not_found(mocker: MockerFixture) -> None:
    mocker.patch("batch.services.games.game_players.get_game_by_game_id", return_value=None)

    with pytest.raises(ValueError, match="Game not found"):
        sync_game_players_by_game_id(GAME_ID)


def test_sync_game_players_starter_is_set_correctly(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    response = _build_live_boxscore_response()
    assert isinstance(response["game"], dict)
    assert isinstance(response["game"]["homeTeam"], dict)
    assert isinstance(response["game"]["homeTeam"]["players"], list)
    response["game"]["homeTeam"]["players"].append(  # type: ignore
        {
            "personId": 9999,
            "jerseyNum": "5",
            "position": "C",
            "starter": "0",
            "status": "ACTIVE",
        }
    )
    mocker.patch("batch.services.games.game_players.get_game_by_game_id", return_value=seed_game)
    mocker.patch("batch.services.games.game_players.NbaApiGateway.fetch", return_value=response)
    add_mock = mocker.patch("batch.services.games.game_players.add_game_players_and_ignore_existing")

    sync_game_players_by_game_id(GAME_ID)

    players = add_mock.call_args[0][0]
    bench_player = next(p for p in players if p.player_id == 9999)
    assert bench_player.is_starter is False
