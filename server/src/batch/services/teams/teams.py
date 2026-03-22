import logging
from datetime import datetime
from typing import TypedDict

from nba_api.stats.endpoints.leaguestandingsv3 import LeagueStandingsV3
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2

from batch.repositories.teams.teams import add_team_properties, add_teams, get_team_properties_by_season, get_teams
from batch.services.nba_api.gateway import NbaApiGateway
from batch.types import Season
from common.models.teams.teams import Team, TeamProperty
from common.types import Conference, Division

logger = logging.getLogger(__name__)


class LeagueScheduleV2Response(TypedDict):
    teamName: str | None
    teamTricode: str | None
    teamCity: str | None


class LeagueStandingsV3Response(TypedDict):
    Conference: str
    Division: str


def _get_team_props_from_league_schedule(season: Season) -> dict[int, LeagueScheduleV2Response]:
    """
    試合日程を基に、指定したシーズンに試合が予定されているチームのチームIDとチーム情報の一覧を作成します.
    """
    league_schedule = NbaApiGateway().fetch(ScheduleLeagueV2, season=season.season_str).get("leagueSchedule", {})
    season_games = league_schedule.get("gameDates", [])

    props: dict[int, LeagueScheduleV2Response] = {}

    for day_data in season_games:
        for game in day_data.get("games", []):
            for side in ("awayTeam", "homeTeam"):
                team = game.get(side, {})
                team_id = team["teamId"]
                props[team_id] = {
                    "teamName": team.get("teamName", None),
                    "teamTricode": team.get("teamTricode", None),
                    "teamCity": team.get("teamCity", None),
                }
    return props


def _get_team_props_from_league_standings(season: Season) -> dict[int, LeagueStandingsV3Response]:
    """
    リーグ順位を基に、指定したシーズンに試合が予定されているチームのチームIDとチーム情報の一覧を作成します.
    """
    league_standings = NbaApiGateway().fetch(LeagueStandingsV3, season=season.season_str).get("resultSets", [])[0]
    standings = league_standings.get("rowSet", [])
    headers = league_standings.get("headers", [])
    props: dict[int, LeagueStandingsV3Response] = {}
    for s in standings:
        team_id = s[headers.index("TeamID")]
        props[team_id] = {
            "Conference": s[headers.index("Conference")],
            "Division": s[headers.index("Division")],
        }
    return props


def _create_teams_by_season(season: Season) -> list[Team]:
    """
    シーズンを指定して、チーム一覧を作成します.
    """
    return [Team(id=id) for id in _get_team_props_from_league_schedule(season).keys() if id != 0]


def _create_team_properties_by_season(season: Season) -> list[TeamProperty]:
    """
    シーズンを指定して、チーム情報一覧を作成します.
    """
    team_props_from_league_standings = _get_team_props_from_league_standings(season)
    team_props_from_league_schedule = _get_team_props_from_league_schedule(season)
    team_properties: list[TeamProperty] = []
    for team_id, team_props in team_props_from_league_schedule.items():
        if team_id in team_props_from_league_standings:
            conference = Conference.from_str(team_props_from_league_standings[team_id]["Conference"])
            division = Division.from_str(team_props_from_league_standings[team_id]["Division"])
        else:
            conference = None
            division = None
        name = team_props["teamName"]
        tricode = team_props["teamTricode"]
        city = team_props["teamCity"]
        if team_id != 0 and name is not None and tricode is not None and city is not None:
            team_properties.append(
                TeamProperty(
                    team_id=team_id,
                    season=season.start_year,
                    team_name=name,
                    team_tricode=tricode,
                    conference=conference,
                    division=division,
                    team_city=city,
                )
            )
    return team_properties


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
