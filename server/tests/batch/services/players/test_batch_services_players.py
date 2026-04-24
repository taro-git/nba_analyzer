import pytest
from nba_api.live.nba.endpoints import BoxScore
from nba_api.stats.endpoints import BoxScoreSummaryV3
from pytest_mock import MockerFixture

from batch.services.players.players import sync_players_by_game_id

GAME_ID = "0022500500"
PLAYER_ID_1 = 1001
PLAYER_ID_2 = 1002


def _build_live_boxscore_response() -> dict[str, object]:
    return {
        "game": {
            "gameTimeUTC": "2026-01-15T23:30:00Z",
            "homeTeam": {
                "players": [
                    {"personId": PLAYER_ID_1, "firstName": "Player", "familyName": "One"},
                ]
            },
            "awayTeam": {
                "players": [
                    {"personId": PLAYER_ID_2, "firstName": "Player", "familyName": "Two"},
                ]
            },
        }
    }


def _build_stats_boxscore_summary_response() -> dict[str, object]:
    return {
        "boxScoreSummary": {
            "gameTimeUTC": "2026-01-15T23:30:00Z",
            "homeTeam": {
                "players": [
                    {"personId": PLAYER_ID_1, "firstName": "Player", "familyName": "One"},
                ],
                "inactives": [],
            },
            "awayTeam": {
                "players": [
                    {"personId": PLAYER_ID_2, "firstName": "Player", "familyName": "Two"},
                ],
                "inactives": [],
            },
        }
    }


def test_sync_players_by_game_id_with_live_endpoint(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.players.players.get_game_by_game_id", return_value=seed_game)
    mocker.patch(
        "batch.services.players.players.NbaApiGateway.fetch",
        return_value=_build_live_boxscore_response(),
    )
    add_mock = mocker.patch("batch.services.players.players.add_players_and_ignore_existing")

    sync_players_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    players = add_mock.call_args[0][0]
    assert len(players) == 2
    player_ids = {p.id for p in players}
    assert player_ids == {PLAYER_ID_1, PLAYER_ID_2}


def test_sync_players_by_game_id_full_name_is_set(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.players.players.get_game_by_game_id", return_value=seed_game)
    mocker.patch(
        "batch.services.players.players.NbaApiGateway.fetch",
        return_value=_build_live_boxscore_response(),
    )
    add_mock = mocker.patch("batch.services.players.players.add_players_and_ignore_existing")

    sync_players_by_game_id(GAME_ID)

    players = add_mock.call_args[0][0]
    p1 = next(p for p in players if p.id == PLAYER_ID_1)
    assert p1.full_name == "Player One"


def test_sync_players_by_game_id_with_stats_endpoint_fallback(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.players.players.get_game_by_game_id", return_value=seed_game)

    def fetch_side_effect(
        endpoint_cls: type[BoxScore] | type[BoxScoreSummaryV3], *args: str, **kwargs: str
    ) -> dict[str, object]:
        if endpoint_cls is BoxScore:
            raise Exception("Live endpoint not available")
        if endpoint_cls is BoxScoreSummaryV3:
            return _build_stats_boxscore_summary_response()
        raise ValueError(f"Unexpected endpoint: {endpoint_cls}")

    mocker.patch("batch.services.players.players.NbaApiGateway.fetch", side_effect=fetch_side_effect)
    add_mock = mocker.patch("batch.services.players.players.add_players_and_ignore_existing")

    sync_players_by_game_id(GAME_ID)

    add_mock.assert_called_once()
    players = add_mock.call_args[0][0]
    assert len(players) == 2


def test_sync_players_by_game_id_error_on_game_not_found(mocker: MockerFixture) -> None:
    mocker.patch("batch.services.players.players.get_game_by_game_id", return_value=None)

    with pytest.raises(ValueError, match="Game not found"):
        sync_players_by_game_id(GAME_ID)


def test_sync_players_by_game_id_updated_at_is_epoch(mocker: MockerFixture) -> None:
    seed_game = mocker.MagicMock()
    seed_game.id = 1
    seed_game.game_id = GAME_ID

    mocker.patch("batch.services.players.players.get_game_by_game_id", return_value=seed_game)
    mocker.patch(
        "batch.services.players.players.NbaApiGateway.fetch",
        return_value=_build_live_boxscore_response(),
    )
    add_mock = mocker.patch("batch.services.players.players.add_players_and_ignore_existing")

    sync_players_by_game_id(GAME_ID)

    players = add_mock.call_args[0][0]
    for p in players:
        assert isinstance(p.updated_at, int)
        assert p.updated_at > 0
