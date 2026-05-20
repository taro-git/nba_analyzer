import pytest
from nba_api.live.nba.endpoints import BoxScore, PlayByPlay
from nba_api.stats.endpoints import BoxScoreTraditionalV3
from pytest_mock import MockerFixture

from batch.services.games.stats import sync_game_stats_by_game_id

GAME_ID = "0022500500"
HOME_TEAM_ID = 1610612765
AWAY_TEAM_ID = 1610612756
PLAYER_ID_1 = 1001
PLAYER_ID_2 = 1002


def _build_live_boxscore_response(elapsed_ms_clock: str = "PT00M00.00S", period: int = 4) -> dict[str, object]:
    return {
        "game": {
            "gameClock": elapsed_ms_clock,
            "period": period,
            "homeTeam": {
                "teamId": HOME_TEAM_ID,
                "statistics": {
                    "minutes": "PT240M00.00S",
                    "points": 110,
                    "reboundsOffensive": 10,
                    "reboundsDefensive": 30,
                    "assists": 25,
                    "steals": 8,
                    "blocks": 5,
                    "fieldGoalsAttempted": 85,
                    "fieldGoalsMade": 42,
                    "threePointersAttempted": 30,
                    "threePointersMade": 12,
                    "freeThrowsAttempted": 20,
                    "freeThrowsMade": 14,
                    "turnovers": 12,
                    "blocksReceived": 3,
                    "foulsPersonal": 18,
                    "foulsTechnical": 1,
                    "foulsDrawn": 20,
                    "plusMinusPoints": 5.0,
                    "pointsAgainst": 105,
                },
                "players": [
                    {
                        "personId": PLAYER_ID_1,
                        "statistics": {
                            "minutes": "PT36M00.00S",
                            "points": 25,
                            "reboundsOffensive": 2,
                            "reboundsDefensive": 5,
                            "assists": 6,
                            "steals": 2,
                            "blocks": 1,
                            "fieldGoalsAttempted": 18,
                            "fieldGoalsMade": 10,
                            "threePointersAttempted": 6,
                            "threePointersMade": 3,
                            "freeThrowsAttempted": 5,
                            "freeThrowsMade": 2,
                            "turnovers": 3,
                            "blocksReceived": 1,
                            "foulsPersonal": 3,
                            "foulsTechnical": 0,
                            "foulsDrawn": 5,
                            "plus": 15,
                            "plusMinusPoints": 10.0,
                        },
                    }
                ],
            },
            "awayTeam": {
                "teamId": AWAY_TEAM_ID,
                "statistics": {
                    "minutes": "PT240M00.00S",
                    "points": 105,
                    "reboundsOffensive": 8,
                    "reboundsDefensive": 28,
                    "assists": 22,
                    "steals": 6,
                    "blocks": 4,
                    "fieldGoalsAttempted": 82,
                    "fieldGoalsMade": 40,
                    "threePointersAttempted": 28,
                    "threePointersMade": 10,
                    "freeThrowsAttempted": 18,
                    "freeThrowsMade": 15,
                    "turnovers": 14,
                    "blocksReceived": 5,
                    "foulsPersonal": 20,
                    "foulsTechnical": 0,
                    "foulsDrawn": 18,
                    "plusMinusPoints": -5.0,
                    "pointsAgainst": 110,
                },
                "players": [
                    {
                        "personId": PLAYER_ID_2,
                        "statistics": {
                            "minutes": "PT32M00.00S",
                            "points": 20,
                            "reboundsOffensive": 1,
                            "reboundsDefensive": 6,
                            "assists": 4,
                            "steals": 1,
                            "blocks": 2,
                            "fieldGoalsAttempted": 15,
                            "fieldGoalsMade": 8,
                            "threePointersAttempted": 5,
                            "threePointersMade": 2,
                            "freeThrowsAttempted": 6,
                            "freeThrowsMade": 4,
                            "turnovers": 2,
                            "blocksReceived": 0,
                            "foulsPersonal": 4,
                            "foulsTechnical": 0,
                            "foulsDrawn": 6,
                            "plus": 10,
                            "plusMinusPoints": -5.0,
                        },
                    }
                ],
            },
        }
    }


def _build_live_playbyplay_response() -> dict[str, object]:
    return {
        "game": {
            "actions": [
                {
                    "clock": "PT11M00.00S",
                    "period": 1,
                    "actionType": "2pt",
                    "subType": "",
                    "shotResult": "Made",
                    "personId": PLAYER_ID_1,
                    "teamId": HOME_TEAM_ID,
                    "playerName": "Player One",
                    "assistPersonId": None,
                    "blockPlayerName": None,
                    "foulDrawnPersonId": None,
                },
            ]
        }
    }


def _build_boxscore_traditional_v3_response() -> dict[str, object]:
    return {
        "boxScoreTraditional": {
            "homeTeam": {
                "teamId": HOME_TEAM_ID,
                "statistics": {
                    "minutes": "240:00",
                    "points": 110,
                    "reboundsOffensive": 10,
                    "reboundsDefensive": 30,
                    "assists": 25,
                    "steals": 8,
                    "blocks": 5,
                    "fieldGoalsAttempted": 85,
                    "fieldGoalsMade": 42,
                    "threePointersAttempted": 30,
                    "threePointersMade": 12,
                    "freeThrowsAttempted": 20,
                    "freeThrowsMade": 14,
                    "turnovers": 12,
                    "foulsPersonal": 18,
                    "plusMinusPoints": 5.0,
                },
                "players": [
                    {
                        "personId": PLAYER_ID_1,
                        "statistics": {
                            "minutes": "36:00",
                            "points": 25,
                            "reboundsOffensive": 2,
                            "reboundsDefensive": 5,
                            "assists": 6,
                            "steals": 2,
                            "blocks": 1,
                            "fieldGoalsAttempted": 18,
                            "fieldGoalsMade": 10,
                            "threePointersAttempted": 6,
                            "threePointersMade": 3,
                            "freeThrowsAttempted": 5,
                            "freeThrowsMade": 2,
                            "turnovers": 3,
                            "foulsPersonal": 3,
                            "plusMinusPoints": 10.0,
                        },
                    }
                ],
            },
            "awayTeam": {
                "teamId": AWAY_TEAM_ID,
                "statistics": {
                    "minutes": "240:00",
                    "points": 105,
                    "reboundsOffensive": 8,
                    "reboundsDefensive": 28,
                    "assists": 22,
                    "steals": 6,
                    "blocks": 4,
                    "fieldGoalsAttempted": 82,
                    "fieldGoalsMade": 40,
                    "threePointersAttempted": 28,
                    "threePointersMade": 10,
                    "freeThrowsAttempted": 18,
                    "freeThrowsMade": 15,
                    "turnovers": 14,
                    "foulsPersonal": 20,
                    "plusMinusPoints": -5.0,
                },
                "players": [
                    {
                        "personId": PLAYER_ID_2,
                        "statistics": {
                            "minutes": "32:00",
                            "points": 20,
                            "reboundsOffensive": 1,
                            "reboundsDefensive": 6,
                            "assists": 4,
                            "steals": 1,
                            "blocks": 2,
                            "fieldGoalsAttempted": 15,
                            "fieldGoalsMade": 8,
                            "threePointersAttempted": 5,
                            "threePointersMade": 2,
                            "freeThrowsAttempted": 6,
                            "freeThrowsMade": 4,
                            "turnovers": 2,
                            "foulsPersonal": 4,
                            "plusMinusPoints": -5.0,
                        },
                    }
                ],
            },
        }
    }


def test_sync_game_stats_by_game_id_with_live_endpoint(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID
    seed_game.home_team_id = HOME_TEAM_ID
    seed_game.away_team_id = AWAY_TEAM_ID

    mocker.patch("batch.services.games.stats.get_game_by_game_id", return_value=seed_game)
    mocker.patch("batch.services.games.stats.get_game_players_by_game_id", return_value=[])

    def fetch_side_effect(
        endpoint_cls: type[BoxScore] | type[PlayByPlay], *args: str, **kwargs: str
    ) -> dict[str, object]:
        if endpoint_cls is BoxScore:
            return _build_live_boxscore_response()
        if endpoint_cls is PlayByPlay:
            return _build_live_playbyplay_response()
        raise ValueError(f"Unexpected endpoint: {endpoint_cls}")

    mocker.patch("batch.services.games.stats.NbaApiGateway.fetch", side_effect=fetch_side_effect)
    add_mock = mocker.patch("batch.services.games.stats.upsert_stats_list")

    sync_game_stats_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    stats = add_mock.call_args[0][0]
    assert len(stats) > 0


def test_sync_game_stats_by_game_id_falls_back_to_boxscore_when_playbyplay_fails(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID
    seed_game.home_team_id = HOME_TEAM_ID
    seed_game.away_team_id = AWAY_TEAM_ID

    mocker.patch("batch.services.games.stats.get_game_by_game_id", return_value=seed_game)
    mocker.patch("batch.services.games.stats.get_game_players_by_game_id", return_value=[])

    def fetch_side_effect(
        endpoint_cls: type[BoxScore] | type[PlayByPlay], *args: str, **kwargs: str
    ) -> dict[str, object]:
        if endpoint_cls is BoxScore:
            return _build_live_boxscore_response()
        if endpoint_cls is PlayByPlay:
            raise Exception("PlayByPlay not available")
        raise ValueError(f"Unexpected endpoint: {endpoint_cls}")

    mocker.patch("batch.services.games.stats.NbaApiGateway.fetch", side_effect=fetch_side_effect)
    add_mock = mocker.patch("batch.services.games.stats.upsert_stats_list")

    sync_game_stats_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    stats = add_mock.call_args[0][0]
    assert len(stats) == 2


def test_sync_game_stats_by_game_id_error_on_game_not_found(mocker: MockerFixture) -> None:
    mocker.patch("batch.services.games.stats.get_game_by_game_id", return_value=None)

    with pytest.raises(ValueError, match="Game not found"):
        sync_game_stats_by_game_id(GAME_ID)


def test_sync_game_stats_by_game_id_home_player_plus_minus_is_positive(mocker: MockerFixture) -> None:
    """ホームチームが得点した場合、ホームプレイヤーの plus_minus は正"""
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID
    seed_game.home_team_id = HOME_TEAM_ID
    seed_game.away_team_id = AWAY_TEAM_ID

    mocker.patch("batch.services.games.stats.get_game_by_game_id", return_value=seed_game)

    game_player_1 = mocker.MagicMock()
    game_player_1.id = 1
    game_player_1.player_id = PLAYER_ID_1
    game_player_1.is_home = True

    game_player_2 = mocker.MagicMock()
    game_player_2.id = 2
    game_player_2.player_id = PLAYER_ID_2
    game_player_2.is_home = False

    mocker.patch("batch.services.games.stats.get_game_players_by_game_id", return_value=[game_player_1, game_player_2])

    def fetch_side_effect(
        endpoint_cls: type[BoxScore] | type[PlayByPlay], *args: str, **kwargs: str
    ) -> dict[str, object]:
        if endpoint_cls is BoxScore:
            return _build_live_boxscore_response()
        if endpoint_cls is PlayByPlay:
            return _build_live_playbyplay_response()
        raise ValueError(f"Unexpected endpoint: {endpoint_cls}")

    mocker.patch("batch.services.games.stats.NbaApiGateway.fetch", side_effect=fetch_side_effect)
    add_mock = mocker.patch("batch.services.games.stats.upsert_stats_list")

    sync_game_stats_by_game_id(GAME_ID)

    stats = add_mock.call_args[0][0]
    home_player_stats = [s for s in stats if s.game_player_id is not None]
    assert len(home_player_stats) > 0


def test_sync_game_stats_by_game_id_with_stats_endpoint_fallback(mocker: MockerFixture) -> None:
    """Live endpoint が失敗した場合、BoxScoreTraditionalV3 にフォールバック"""
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID
    seed_game.home_team_id = HOME_TEAM_ID
    seed_game.away_team_id = AWAY_TEAM_ID

    mocker.patch("batch.services.games.stats.get_game_by_game_id", return_value=seed_game)

    # ゲームプレイヤーをモック
    game_player_1 = mocker.MagicMock()
    game_player_1.id = 1
    game_player_1.player_id = PLAYER_ID_1
    game_player_1.is_home = True

    game_player_2 = mocker.MagicMock()
    game_player_2.id = 2
    game_player_2.player_id = PLAYER_ID_2
    game_player_2.is_home = False

    mocker.patch("batch.services.games.stats.get_game_players_by_game_id", return_value=[game_player_1, game_player_2])

    def fetch_side_effect(
        endpoint_cls: type[BoxScore] | type[PlayByPlay] | type[BoxScoreTraditionalV3], *args: str, **kwargs: str
    ) -> dict[str, object]:
        if endpoint_cls is BoxScore:
            raise Exception("Live BoxScore not available")
        if endpoint_cls is PlayByPlay:
            raise Exception("Live PlayByPlay not available")
        if endpoint_cls is BoxScoreTraditionalV3:
            return _build_boxscore_traditional_v3_response()
        raise ValueError(f"Unexpected endpoint: {endpoint_cls}")

    mocker.patch("batch.services.games.stats.NbaApiGateway.fetch", side_effect=fetch_side_effect)
    add_mock = mocker.patch("batch.services.games.stats.upsert_stats_list")

    sync_game_stats_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    stats = add_mock.call_args[0][0]
    assert len(stats) > 0
