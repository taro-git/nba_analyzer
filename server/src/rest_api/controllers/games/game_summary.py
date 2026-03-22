from datetime import datetime, timezone

from sqlmodel import Session

from common.models.teams.teams import TeamProperty
from rest_api.repositories.games.games import get_games_by_start_datetime
from rest_api.repositories.teams.teams import get_team_properties_by_ids
from rest_api.schemas.commons import GameCategory, GameStatus, Season
from rest_api.schemas.games.game_summaries import GameSummarySchema
from rest_api.schemas.teams.regular_season import Team


def get_game_summaries_by_start_datetime(
    session: Session, from_datetime: datetime, to_datetime: datetime
) -> list[GameSummarySchema]:
    """
    試合開始時刻の範囲を指定して GameSummarySchema 一覧を返します.
    """
    games = get_games_by_start_datetime(session, from_datetime, to_datetime)
    seasons = {game.season for game in games}
    team_properties: dict[int, dict[int, TeamProperty]] = {}
    for season in seasons:
        season_obj = Season(f"{season}-{(season + 1) % 100:02d}")
        team_ids = {game.home_team_id for game in games if game.season == season} | {
            game.away_team_id for game in games if game.season == season
        }
        properties = get_team_properties_by_ids(session, season_obj, team_ids)
        team_properties[season] = {prop.team_id: prop for prop in properties}
    return [
        GameSummarySchema(
            game_id=game.game_id,
            status=GameStatus(game.status.value),
            category=GameCategory(game.category.value),
            start_datetime=datetime.fromtimestamp(game.start_epoc_sec, tz=timezone.utc),
            elapsed_sec=game.elapsed_sec,
            home_team=Team(
                team_id=game.home_team_id,
                team_name=team_properties[game.season][game.home_team_id].team_name,
                team_tricode=team_properties[game.season][game.home_team_id].team_tricode,
                team_logo=f"https://cdn.nba.com/logos/nba/{game.home_team_id}/global/L/logo.svg",
            ),
            away_team=Team(
                team_id=game.away_team_id,
                team_name=team_properties[game.season][game.away_team_id].team_name,
                team_tricode=team_properties[game.season][game.away_team_id].team_tricode,
                team_logo=f"https://cdn.nba.com/logos/nba/{game.away_team_id}/global/L/logo.svg",
            ),
            home_team_score=game.home_score,
            away_team_score=game.away_score,
            playoff_label=game.playoff_label,
        )
        for game in games
    ]
