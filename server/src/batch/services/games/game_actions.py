import logging

from nba_api.live.nba.endpoints import PlayByPlay
from nba_api.stats.endpoints import PlayByPlayV3

from batch.repositories.games.game_actions import upsert_game_actions
from batch.repositories.games.game_players import get_game_players_by_game_id
from batch.repositories.games.games import get_game_by_game_id
from batch.services.commons.game_clock import create_elapsed_ms_from_clock_and_period
from batch.services.nba_api.gateway import NbaApiGateway
from common.models.games.game_actions import GameAction
from common.models.games.games import Game

logger = logging.getLogger(__name__)


def _create_actions_from_stats_endpoint(game: Game) -> list[GameAction]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    play_by_play_v3 = NbaApiGateway.fetch(PlayByPlayV3, game_id=game.game_id)
    game_players: dict[int, int] = {p.player_id: p.id for p in get_game_players_by_game_id(game.id) if p.id is not None}
    return [
        GameAction(
            game_id=game.id,
            action_number=i,
            elapsed_ms=create_elapsed_ms_from_clock_and_period(action["clock"], action["period"]),
            game_player_id=id,
            team_id=team_id,
            description=action["description"],
            action_type=action["actionType"],
            sub_type=action["subType"] if action["subType"] != "" else None,
            shot_value=None if action["shotValue"] == 0 else action["shotValue"],
            home_score=int(action["scoreHome"]) if action["scoreHome"] != "" else None,
            away_score=int(action["scoreAway"]) if action["scoreAway"] != "" else None,
            x_legacy=action.get("xLegacy", None),
            y_legacy=action.get("yLegacy", None),
        )
        for i, action in enumerate(play_by_play_v3["game"]["actions"])
        for id in [game_players[action["personId"]] if action.get("personId", None) in game_players.keys() else None]
        for team_id in [
            action["teamId"]
            if action.get("teamId", None) in [game.home_team_id, game.away_team_id]
            else action["personId"]
            if action.get("personId", None) in [game.home_team_id, game.away_team_id]
            else None
        ]
    ]


def _create_actions_from_live_endpoint(game: Game) -> list[GameAction]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    live_playbyplay = NbaApiGateway.fetch(PlayByPlay, game_id=game.game_id)
    game_players: dict[int, int] = {p.player_id: p.id for p in get_game_players_by_game_id(game.id) if p.id is not None}
    return [
        GameAction(
            game_id=game.id,
            action_number=i,
            elapsed_ms=create_elapsed_ms_from_clock_and_period(action["clock"], action["period"]),
            game_player_id=id,
            team_id=team_id,
            description=action["description"],
            action_type=action["actionType"],
            sub_type=action["subType"] if action["subType"] != "" else None,
            shot_value=1
            if action["actionType"] == "freethrow"
            else 2
            if action["actionType"] == "2pt"
            else 3
            if action["actionType"] == "3pt"
            else None,
            home_score=action.get("homeScore", None),
            away_score=action.get("awayScore", None),
            x_legacy=action.get("xLegacy", None),
            y_legacy=action.get("yLegacy", None),
        )
        for i, action in enumerate(live_playbyplay["game"]["actions"])
        for id in [game_players[action["personId"]] if action.get("personId", None) in game_players.keys() else None]
        for team_id in [
            action["teamId"] if action.get("teamId", None) in [game.home_team_id, game.away_team_id] else None
        ]
    ]


def sync_game_actions_by_game_id(game_id: str) -> None:
    """
    試合IDを指定して、最新のデータと DB のプレイバイプレイを同期する
    """
    try:
        game = get_game_by_game_id(game_id)
        if game is None:
            raise ValueError(f"Game not found: {game_id}")
        try:
            actions = _create_actions_from_live_endpoint(game)
        except Exception as e:
            logger.info(f"live boxscore endpoint is not available. Try stats endpoint: {game_id}, {e}")
            actions = _create_actions_from_stats_endpoint(game)
        upsert_game_actions(actions)
    except Exception as e:
        logger.error(f"error in sync_game_actions_by_game_id: {e}")
        raise
