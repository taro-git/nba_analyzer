import pytest
from nba_api.live.nba.endpoints import PlayByPlay
from nba_api.stats.endpoints import PlayByPlayV3
from pytest_mock import MockerFixture

from batch.services.games.game_actions import sync_game_actions_by_game_id

GAME_ID = "0022500500"
HOME_TEAM_ID = 1610612765
AWAY_TEAM_ID = 1610612756
PLAYER_ID_1 = 1001


def _build_live_playbyplay_response() -> dict[str, object]:
    return {
        "game": {
            "actions": [
                {
                    "clock": "PT11M30.00S",
                    "period": 1,
                    "personId": PLAYER_ID_1,
                    "teamId": HOME_TEAM_ID,
                    "description": "Player One 2pt shot",
                    "actionType": "2pt",
                    "subType": "",
                    "homeScore": 2,
                    "awayScore": 0,
                    "xLegacy": 100,
                    "yLegacy": 200,
                },
                {
                    "clock": "PT11M00.00S",
                    "period": 1,
                    "personId": 0,
                    "teamId": AWAY_TEAM_ID,
                    "description": "Team rebound",
                    "actionType": "rebound",
                    "subType": "defensive",
                },
            ]
        }
    }


def _build_stats_playbyplay_response() -> dict[str, object]:
    return {
        "game": {
            "actions": [
                {
                    "clock": "PT11M30.00S",
                    "period": 1,
                    "personId": PLAYER_ID_1,
                    "teamId": HOME_TEAM_ID,
                    "description": "Player One 2pt shot",
                    "actionType": "2pt",
                    "subType": "",
                    "shotValue": 2,
                    "scoreHome": "2",
                    "scoreAway": "0",
                    "xLegacy": 100,
                    "yLegacy": 200,
                },
            ]
        }
    }


def test_sync_game_actions_by_game_id_with_live_endpoint(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.games.game_actions.get_game_by_game_id", return_value=seed_game)
    mocker.patch("batch.services.games.game_actions.get_game_players_by_game_id", return_value=[])
    mocker.patch(
        "batch.services.games.game_actions.NbaApiGateway.fetch",
        return_value=_build_live_playbyplay_response(),
    )
    add_mock = mocker.patch("batch.services.games.game_actions.add_game_actions")

    sync_game_actions_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    actions = add_mock.call_args[0][0]
    assert len(actions) == 2
    assert actions[0].action_type == "2pt"
    assert actions[0].shot_value == 2


def test_sync_game_actions_by_game_id_with_stats_endpoint_fallback(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.games.game_actions.get_game_by_game_id", return_value=seed_game)
    mocker.patch("batch.services.games.game_actions.get_game_players_by_game_id", return_value=[])

    def fetch_side_effect(
        endpoint_cls: type[PlayByPlay] | type[PlayByPlayV3], *args: str, **kwargs: dict[str, object]
    ) -> dict[str, object]:
        if endpoint_cls is PlayByPlay:
            raise Exception("Live endpoint not available")
        if endpoint_cls is PlayByPlayV3:
            return _build_stats_playbyplay_response()
        raise ValueError(f"Unexpected endpoint: {endpoint_cls}")

    mocker.patch("batch.services.games.game_actions.NbaApiGateway.fetch", side_effect=fetch_side_effect)
    add_mock = mocker.patch("batch.services.games.game_actions.add_game_actions")

    sync_game_actions_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    actions = add_mock.call_args[0][0]
    assert len(actions) == 1


def test_sync_game_actions_by_game_id_error_on_game_not_found(mocker: MockerFixture) -> None:
    mocker.patch("batch.services.games.game_actions.get_game_by_game_id", return_value=None)

    with pytest.raises(ValueError, match="Game not found"):
        sync_game_actions_by_game_id(GAME_ID)
