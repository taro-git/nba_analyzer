import logging
from typing import TypedDict

from nba_api.live.nba.endpoints import BoxScore
from nba_api.stats.endpoints import BoxScoreSummaryV3, BoxScoreTraditionalV3

from batch.repositories.games.game_players import add_game_players_and_ignore_existing
from batch.repositories.games.games import get_game_by_game_id
from batch.services.nba_api.gateway import NbaApiGateway
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game
from common.types import PlayerPosition

logger = logging.getLogger(__name__)


class BoxScoreTraditionalV3Response(TypedDict):
    position: PlayerPosition | None
    is_starter: bool


def _create_player_props_from_boxscore_traditional_v3(game: Game) -> dict[int, BoxScoreTraditionalV3Response]:
    box_score_traditional_v3 = NbaApiGateway.fetch(BoxScoreTraditionalV3, game_id=game.game_id)
    return {
        p["personId"]: {"position": pos, "is_starter": pos is not None}
        for k in ["homeTeam", "awayTeam"]
        for p in box_score_traditional_v3["boxScoreTraditional"][k]["players"]
        for pos in [PlayerPosition.from_endpoints(p.get("position", None))]
    }


def _create_game_players_from_stats_endpoint(game: Game) -> list[GamePlayer]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    box_score_summary_v3 = NbaApiGateway.fetch(BoxScoreSummaryV3, game_id=game.game_id)
    player_props_from_boxscore_traditional_v3 = _create_player_props_from_boxscore_traditional_v3(game)
    return [
        GamePlayer(
            game_id=game.id,
            player_id=player["personId"],
            jearsy_num=player["jerseyNum"],
            position=player_props_from_boxscore_traditional_v3[player["personId"]]["position"],
            is_home=team_key == "homeTeam",
            is_starter=player_props_from_boxscore_traditional_v3[player["personId"]]["is_starter"],
            is_active=player_key == "players",
        )
        for team_key in ["homeTeam", "awayTeam"]
        for player_key in ["players", "inactives"]
        for player in box_score_summary_v3["boxScoreSummary"][team_key][player_key]
    ]


def _create_game_players_from_live_endpoint(game: Game) -> list[GamePlayer]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    live_boxscore = NbaApiGateway.fetch(BoxScore, game_id=game.game_id)
    return [
        GamePlayer(
            game_id=game.id,
            player_id=player["personId"],
            jearsy_num=player["jerseyNum"],
            position=PlayerPosition.from_endpoints(player.get("position", None)),
            is_home=key == "homeTeam",
            is_starter=player["starter"] == "1",
            is_active=player["status"] == "ACTIVE",
        )
        for key in ["homeTeam", "awayTeam"]
        for player in live_boxscore["game"][key]["players"]
    ]


def sync_game_players_by_game_id(game_id: str) -> None:
    """
    試合IDを指定して、最新のデータと DB の試合に紐づいた選手情報を同期する
    """
    try:
        game = get_game_by_game_id(game_id)
        if game is None:
            raise ValueError(f"Game not found: {game_id}")
        try:
            game_players = _create_game_players_from_live_endpoint(game)
        except Exception as e:
            logger.info(f"live boxscore endpoint is not available. Try stats endpoint: {game_id}, {e}")
            game_players = _create_game_players_from_stats_endpoint(game)
        add_game_players_and_ignore_existing(game_players)
    except Exception as e:
        logger.error(f"error in sync_game_players_by_game_id: {e}")
        raise
