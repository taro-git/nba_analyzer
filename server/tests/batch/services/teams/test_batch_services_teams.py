from typing import Any

import pytest
from nba_api.stats.endpoints.leaguestandingsv3 import LeagueStandingsV3
from nba_api.stats.endpoints.scheduleleaguev2 import ScheduleLeagueV2
from pytest_mock import MockerFixture

from batch.services.teams.teams import sync_teams_by_season
from batch.types import Season
from common.models.teams.teams import Team
from common.types import Conference, Division


def mocker_patch(
    mocker: MockerFixture,
    mock_team: list[Team],
    mock_league_Standings_v3: dict[str, Any],
    mock_schedule_league_v2: dict[str, Any],
) -> None:
    mocker.patch("batch.services.teams.teams.get_teams", return_value=mock_team)

    def fetch_side_effect(
        endpoint_cls: type[LeagueStandingsV3] | type[ScheduleLeagueV2], *args: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        if endpoint_cls is LeagueStandingsV3:
            return mock_league_Standings_v3
        if endpoint_cls is ScheduleLeagueV2:
            return mock_schedule_league_v2
        raise ValueError(f"Unexpected endpoint_cls: {endpoint_cls}")

    mocker.patch(
        "batch.services.teams.teams.NbaApiGateway.fetch",
        side_effect=fetch_side_effect,
    )

    mocker.patch("batch.services.teams.teams.add_teams", return_value=None)


@pytest.fixture
def season() -> Season:
    return Season.from_season_str("2023-24")


def build_standings(team_rows: list[list[Any]]) -> dict[str, Any]:
    return {
        "resultSets": [
            {
                "headers": [
                    "TeamID",
                    "TeamName",
                    "Conference",
                    "Division",
                    "TeamCity",
                ],
                "rowSet": team_rows,
            }
        ]
    }


def build_schedule(team_ids: list[int]) -> dict[str, Any]:
    games: list[dict[str, Any]] = []
    for i, team_id in enumerate(team_ids):
        games.append(
            {
                "awayTeam": {"teamId": team_id, "teamTricode": f"T{team_id:02d}"},
                "homeTeam": {"teamId": team_ids[i - 1], "teamTricode": f"T{team_ids[i - 1]:02d}"},
            }
        )

    return {"leagueSchedule": {"gameDates": [{"games": games}]}}


def existing_team(team_id: int) -> Team:
    return Team(
        id=team_id,
        team_name=f"Team{team_id}",
        team_tricode=f"T{team_id:02d}",
        conference=Conference.west,
        division=Division.pacific,
        team_city="City",
    )


@pytest.mark.parametrize(
    "db_ids, api_ids, expected_add_count",
    [
        ([], [], 0),
        ([], [1], 1),
        ([], [1, 2], 2),
        ([1], [1], 0),
        ([1], [1, 2], 1),
        ([1], [1, 2, 3], 2),
    ],
)
def test_sync_teams_normal(
    mocker: MockerFixture,
    season: Season,
    db_ids: list[int],
    api_ids: list[int],
    expected_add_count: int,
) -> None:
    standings_rows: list[list[Any]] = [[i, f"Team{i}", "West", "Pacific", "City"] for i in api_ids]

    mock_standings = build_standings(standings_rows)
    mock_schedule = build_schedule(api_ids)

    db_teams = [existing_team(i) for i in db_ids]

    mocker_patch(mocker, db_teams, mock_standings, mock_schedule)

    add_mock = mocker.patch("batch.services.teams.teams.add_teams")

    sync_teams_by_season(season)

    add_mock.assert_called_once()
    added = add_mock.call_args[0][0]
    assert len(added) == expected_add_count


def test_missing_standings_key_raises(mocker: MockerFixture, season: Season) -> None:
    mock_standings = {"invalid": "structure"}
    mock_schedule = build_schedule([1])

    mocker_patch(mocker, [], mock_standings, mock_schedule)

    with pytest.raises(IndexError):
        sync_teams_by_season(season)


def test_missing_schedule_key_raises(mocker: MockerFixture, season: Season) -> None:
    mock_standings = build_standings([[1, "Team1", "West", "Pacific", "City"]])
    mock_schedule = {"invalid": "structure"}

    mocker_patch(mocker, [], mock_standings, mock_schedule)

    with pytest.raises(KeyError):
        sync_teams_by_season(season)


def test_team_in_standings_not_in_schedule_raises(mocker: MockerFixture, season: Season) -> None:
    mock_standings = build_standings([[1, "Team1", "West", "Pacific", "City"]])
    mock_schedule = build_schedule([])

    mocker_patch(mocker, [], mock_standings, mock_schedule)

    with pytest.raises(KeyError):
        sync_teams_by_season(season)


def test_empty_schedule_raises(mocker: MockerFixture, season: Season) -> None:
    mock_standings = build_standings([[1, "Team1", "West", "Pacific", "City"]])
    mock_schedule = build_schedule([])

    mocker_patch(mocker, [], mock_standings, mock_schedule)

    with pytest.raises(KeyError):
        sync_teams_by_season(season)
