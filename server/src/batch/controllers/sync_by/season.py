from datetime import datetime

from batch.services.commons.seasons import sync_seasons
from batch.services.teams.regular_season_team_standings import sync_regular_season_team_standings_by_season
from batch.services.teams.teams import sync_teams_by_season
from batch.types import Season


def sync_all_by_season(season: Season | None = None) -> None:
    """
    シーズンを指定して、最新のデータと DB を同期します.
    """
    if season is None:
        season = Season.from_datetime(datetime.now())
    sync_seasons(season)
    sync_teams_by_season(season)
    sync_regular_season_team_standings_by_season(season)
