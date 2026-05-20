import logging
from datetime import datetime, timezone

from nba_api.stats.endpoints.leaguegamefinder import LeagueGameFinder
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2

from batch.repositories.games.games import (
    get_games_by_season,
    remove_games,
    upsert_games,
)
from batch.repositories.games.games import (
    get_games_by_start_datetime as get_games_by_start_datetime_from_db,
)
from batch.repositories.games.stats import get_all_game_ids as get_all_game_ids_of_stats
from batch.repositories.games.game_actions import get_all_game_ids as get_all_game_ids_of_actions
from batch.repositories.teams.teams import get_teams
from batch.services.nba_api.gateway import NbaApiGateway
from batch.types import Season
from common.models.games.games import Game
from common.types import GameCategory, GameStatus

logger = logging.getLogger(__name__)


def _create_game_elapsed_secs(season: Season) -> dict[str, int]:
    result_sets = NbaApiGateway().fetch(LeagueGameFinder, season_nullable=season.season_str).get("resultSets", [])[0]
    headers = result_sets.get("headers", [])
    games = result_sets.get("rowSet", [])
    game_elapsed_secs: dict[str, int] = {}
    for game in games:
        game_elapsed_secs[game[headers.index("GAME_ID")]] = round(game[headers.index("MIN")] / 5) * 60
    return game_elapsed_secs


def sync_games_by_season(season: Season | None = None) -> None:
    """
    シーズンを指定して、最新のデータと DB の試合情報を同期する
    """
    try:
        if season is None:
            season = Season.from_datetime(datetime.now())
        league_schedule = NbaApiGateway().fetch(ScheduleLeagueV2, season=season.season_str).get("leagueSchedule", {})
        game_dates = league_schedule.get("gameDates")
        games: list[Game] = []
        teams = get_teams()
        team_ids = [t.id for t in teams]
        game_elapsed_secs: dict[str, int] = _create_game_elapsed_secs(season)
        for game_date in game_dates:
            for game in game_date.get("games", []):
                try:
                    category = GameCategory.from_game_id(game.get("gameId"))
                    home_team_id = game.get("homeTeam", {}).get("teamId")
                    away_team_id = game.get("awayTeam", {}).get("teamId")
                    if home_team_id in team_ids and away_team_id in team_ids and home_team_id != away_team_id:
                        games.append(
                            Game(
                                game_id=game.get("gameId"),
                                season=season.start_year,
                                start_epoc_sec=int(
                                    datetime.strptime(game.get("gameDateTimeUTC"), "%Y-%m-%dT%H:%M:%SZ")
                                    .replace(tzinfo=timezone.utc)
                                    .timestamp()
                                ),
                                status=GameStatus.from_status_id(game.get("gameStatus")),
                                elapsed_sec=game_elapsed_secs.get(game.get("gameId"), 0),
                                category=category,
                                home_team_id=home_team_id,
                                away_team_id=away_team_id,
                                home_score=game.get("homeTeam", {}).get("score", 0),
                                away_score=game.get("awayTeam", {}).get("score", 0),
                                playoff_label=f"{game.get('gameLabel', 'Playoff')} {game.get('gameSubLabel', '')}"
                                if category == GameCategory.playoffs
                                else None,
                            )
                        )
                except Exception:
                    logger.error(f"error in sync_games_by_season: {game.get('gameId', 'cannot get game id')}")
        upsert_games(games)
        remove_games([g for g in get_games_by_season(season) if g.game_id not in {g.game_id for g in games}])
    except Exception as e:
        logger.error(f"error in sync_games_by_season: {e}")
        raise


def get_games_by_start_datetime(from_datetime: datetime, to_datetime: datetime, status: GameStatus) -> list[Game]:
    """
    試合開始時刻の範囲を指定して Game 一覧を返します.
    """
    return get_games_by_start_datetime_from_db(from_datetime, to_datetime, status)


def get_unninitialized_games_by_start_datetime(
    from_datetime: datetime, to_datetime: datetime, status: GameStatus
) -> list[Game]:
    """
    試合開始時刻の範囲と試合ステータスを指定して Game 一覧を返します.
    """
    all_games = get_games_by_start_datetime_from_db(from_datetime, to_datetime, status)
    all_stats = {s for s in get_all_game_ids_of_stats()}
    all_actions = {a for a in get_all_game_ids_of_actions()}
    return [g for g in all_games if g.id not in all_stats or g.id not in all_actions]
