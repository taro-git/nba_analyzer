import logging
from datetime import datetime, timezone

from nba_api.live.nba.endpoints import BoxScore
from nba_api.stats.endpoints import BoxScoreSummaryV3

from batch.repositories.games.games import get_game_by_game_id
from batch.repositories.players.players import add_players_and_ignore_existing
from batch.services.nba_api.gateway import NbaApiGateway
from common.models.games.games import Game
from common.models.players.players import Player

logger = logging.getLogger(__name__)


def _create_players_from_stats_endpoint(game: Game) -> list[Player]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    box_score_summary_v3 = NbaApiGateway.fetch(BoxScoreSummaryV3, game_id=game.game_id)
    epoch = int(
        datetime.strptime(box_score_summary_v3["boxScoreSummary"]["gameTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )
    return [
        Player(
            id=player["personId"],
            updated_at=epoch,
            full_name=f"{player['firstName']} {player['familyName']}",
            abbreviation=f"{player['firstName'][0]}. {player['familyName'][0]}",
        )
        for team_key in ["homeTeam", "awayTeam"]
        for player_key in ["players", "inactives"]
        for player in box_score_summary_v3["boxScoreSummary"][team_key][player_key]
    ]


def _create_players_from_live_endpoint(game: Game) -> list[Player]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    live_boxscore = NbaApiGateway.fetch(BoxScore, game_id=game.game_id)
    epoch = int(
        datetime.strptime(live_boxscore["game"]["gameTimeUTC"], "%Y-%m-%dT%H:%M:%SZ")
        .replace(tzinfo=timezone.utc)
        .timestamp()
    )
    return [
        Player(
            id=player["personId"],
            updated_at=epoch,
            full_name=f"{player['firstName']} {player['familyName']}",
            abbreviation=f"{player['firstName'][0]}. {player['familyName']}",
        )
        for key in ["homeTeam", "awayTeam"]
        for player in live_boxscore["game"][key]["players"]
    ]


def sync_players_by_game_id(game_id: str) -> None:
    """
    試合IDを指定して、最新のデータと DB の試合に関連する選手の共通情報を同期する
    """
    try:
        game = get_game_by_game_id(game_id)
        if game is None:
            raise ValueError(f"Game not found: {game_id}")
        try:
            players = _create_players_from_live_endpoint(game)
        except Exception:
            logger.info(f"live boxscore endpoint is not available. Try stats endpoint: {game_id}")
            players = _create_players_from_stats_endpoint(game)
        add_players_and_ignore_existing(players)
    except Exception as e:
        logger.error(f"error in sync_players_by_game_id: {e}")
        raise
