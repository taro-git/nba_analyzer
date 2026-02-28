import pytest
from pytest_mock import MockerFixture
from sqlmodel import Session

import rest_api.controllers.teams.regular_season as target
from common.models.teams.regular_season_team_standings import RegularSeasonTeamStanding
from common.models.teams.teams import TeamProperty
from common.types import Conference, Division
from rest_api.schemas.commons import Season
from rest_api.schemas.teams.regular_season import RegularSeasonTeam


def mocker_patch(
    mocker: MockerFixture, mock_team: list[TeamProperty], mock_standings: list[RegularSeasonTeamStanding]
) -> None:
    mocker.patch(
        "rest_api.controllers.teams.regular_season.get_regular_season_team_standings",
        return_value=mock_standings,
    )

    mocker.patch(
        "rest_api.controllers.teams.regular_season.get_team_properties_by_ids",
        return_value=mock_team,
    )


@pytest.fixture
def mock_success_case(mocker: MockerFixture) -> list[RegularSeasonTeam]:
    mock_standings = [
        RegularSeasonTeamStanding(team_id=1, season=2023, win=10, lose=5, rank=1),
        RegularSeasonTeamStanding(team_id=2, season=2023, win=8, lose=7, rank=2),
    ]
    mock_teams = [
        TeamProperty(
            team_id=1,
            season=2023,
            team_name="Team A",
            team_tricode="AAA",
            team_city="City A",
            conference=Conference.east,
            division=Division.atlantic,
        ),
        TeamProperty(
            team_id=2,
            season=2023,
            team_name="Team B",
            team_tricode="BBB",
            team_city="City B",
            conference=Conference.east,
            division=Division.central,
        ),
    ]
    mocker_patch(mocker, mock_teams, mock_standings)
    return [
        RegularSeasonTeam(
            team_id=1,
            team_name="Team A",
            team_tricode="AAA",
            team_logo="https://cdn.nba.com/logos/nba/1/global/L/logo.svg",
            conference=Conference.east,
            division=Division.atlantic,
            rank=1,
            win=10,
            lose=5,
        ),
        RegularSeasonTeam(
            team_id=2,
            team_name="Team B",
            team_tricode="BBB",
            team_logo="https://cdn.nba.com/logos/nba/2/global/L/logo.svg",
            conference=Conference.east,
            division=Division.central,
            rank=2,
            win=8,
            lose=7,
        ),
    ]


def test_get_regular_season_teams_by_season_return_matched(
    session: Session,
    mock_success_case: list[RegularSeasonTeam],
) -> None:
    result = sorted(
        [s.model_dump() for s in target.get_regular_season_teams_by_season(session, Season("2023-24"))],
        key=lambda x: x["team_id"],
    )
    expected = sorted([s.model_dump() for s in mock_success_case], key=lambda x: x["team_id"])

    assert result == expected


def test_get_regular_season_teams_by_season_return_empty_when_no_standings(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mocker_patch(mocker, [], [])
    result = target.get_regular_season_teams_by_season(session, Season("2023-24"))
    assert result == []


def test_get_regular_season_teams_by_season_missing_team(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_standings = [
        RegularSeasonTeamStanding(team_id=99, season=2023, win=10, lose=5, rank=1),
    ]
    mocker_patch(mocker, [], mock_standings)

    with pytest.raises(ValueError):
        target.get_regular_season_teams_by_season(session, Season("2023-24"))
