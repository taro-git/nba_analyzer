import logging
from datetime import datetime

from nba_api.stats.endpoints.leaguestandingsv3 import LeagueStandingsV3
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2

from batch.repositories.teams.teams import add_team_properties, add_teams, get_team_properties_by_season, get_teams
from batch.services.nba_api.gateway import NbaApiGateway
from batch.types import Season
from common.models.teams.teams import Team, TeamProperty
from common.types import Conference, Division

logger = logging.getLogger(__name__)


def _create_team_tricode(season: Season) -> dict[int, str]:
    """
    指定したシーズンに試合が予定されているチームのチームIDと略称の一覧を作成します.
    """
    league_schedule = NbaApiGateway().fetch(ScheduleLeagueV2, season=season.season_str).get("leagueSchedule", {})
    season_games = league_schedule.get("gameDates", [])

    team_dict: dict[int, str] = {}

    for day_data in season_games:
        for game in day_data.get("games", []):
            for side in ("awayTeam", "homeTeam"):
                team = game.get(side, {})
                team_id = team.get("teamId")
                tricode = team.get("teamTricode")

                if team_id and tricode:
                    team_dict[team_id] = tricode
    return team_dict


def _create_teams_by_season(season: Season) -> list[Team]:
    """
    シーズンを指定して、チーム一覧を作成します.
    """
    result_set = NbaApiGateway().fetch(LeagueStandingsV3, season=season.season_str).get("resultSets", [])[0]
    standings = result_set.get("rowSet", [])
    headers = result_set.get("headers", [])
    return [Team(id=s[headers.index("TeamID")]) for s in standings]


def _create_team_properties_by_season(season: Season) -> list[TeamProperty]:
    """
    シーズンを指定して、チーム情報一覧を作成します.
    """
    result_set = NbaApiGateway().fetch(LeagueStandingsV3, season=season.season_str).get("resultSets", [])[0]
    standings = result_set.get("rowSet", [])
    headers = result_set.get("headers", [])
    team_tricode = _create_team_tricode(season)
    return [
        TeamProperty(
            team_id=s[headers.index("TeamID")],
            season=season.start_year,
            team_name=s[headers.index("TeamName")],
            team_tricode=team_tricode[s[headers.index("TeamID")]],
            conference=Conference.from_str(s[headers.index("Conference")]),
            division=Division.from_str(s[headers.index("Division")]),
            team_city=s[headers.index("TeamCity")],
        )
        for s in standings
    ]


def sync_teams_by_season(season: Season | None = None) -> None:
    """
    シーズンを指定して、最新のデータと DB のチーム情報を同期する
    """
    try:
        if season is None:
            season = Season.from_datetime(datetime.now())
        teams_from_nba_api = _create_teams_by_season(season)
        teams_from_db = get_teams()
        team_ids_from_db = [t.id for t in teams_from_db]
        add_teams([t for t in teams_from_nba_api if t.id not in team_ids_from_db])
        team_properties_from_nba_api = _create_team_properties_by_season(season)
        team_properties_from_db = get_team_properties_by_season(season)
        team_property_ids_from_db = [t.team_id for t in team_properties_from_db]
        add_team_properties([t for t in team_properties_from_nba_api if t.team_id not in team_property_ids_from_db])
    except Exception as e:
        logger.error(f"error in sync_teams_by_season: {e}")
        raise
