import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError

from batch.repositories.teams.teams import add_team_properties, add_teams, get_team_properties_by_season, get_teams
from batch.types import Season
from common.models.teams.teams import Team, TeamProperty
from common.types import Conference, Division


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> None:
    mocker.patch("batch.repositories.teams.teams.engine", engine)


def test_get_teams_returns_team(mock_engine: None, seed_teams: dict[int, Team]) -> None:
    assert get_teams() == [seed_teams[i] for i in seed_teams.keys()]


def test_get_team_properties(mock_engine: None, seed_team_properties: dict[int, TeamProperty]) -> None:
    assert get_team_properties_by_season(Season.from_start_year(2022)) == [
        seed_team_properties[i] for i in seed_team_properties.keys()
    ]


def test_add_teams_adds_one_team(mock_engine: None, seed_teams: dict[int, Team]) -> None:
    new_team = Team(id=31)
    add_teams([new_team])
    result_teams = get_teams()
    assert [t.id for t in result_teams] == [seed_teams[i].id for i in seed_teams.keys()] + [31]


def test_add_team_properties_adds_one(mock_engine: None, seed_team_properties: dict[int, TeamProperty]) -> None:
    new_team_property = TeamProperty(
        team_id=31,
        season=2022,
        team_city="City 31",
        team_name="Name 31",
        team_tricode="T31",
        conference=Conference.east,
        division=Division.atlantic,
    )
    add_team_properties([new_team_property])
    result_teams = get_team_properties_by_season(Season.from_start_year(2022))
    assert [t.team_id for t in result_teams] == [
        seed_team_properties[i].team_id for i in seed_team_properties.keys()
    ] + [31]


def test_add_teams_adds_some_teams(mock_engine: None, seed_teams: dict[int, Team]) -> None:
    new_teams = [Team(id=i + 31) for i in range(5)]
    add_teams(new_teams)
    result_teams = get_teams()
    assert [t.id for t in result_teams] == [seed_teams[i].id for i in seed_teams.keys()] + [i + 31 for i in range(5)]


def test_add_team_properties_adds_some_teams(mock_engine: None, seed_team_properties: dict[int, TeamProperty]) -> None:
    new_teams = [
        TeamProperty(
            team_id=i + 31,
            season=2022,
            team_city=f"City {i + 31}",
            team_name=f"Name {i + 31}",
            team_tricode=f"T{i + 31:02d}",
            conference=Conference.east,
            division=Division.atlantic,
        )
        for i in range(5)
    ]
    add_team_properties(new_teams)
    result_teams = get_team_properties_by_season(Season.from_start_year(2022))
    assert [t.team_id for t in result_teams] == [
        seed_team_properties[i].team_id for i in seed_team_properties.keys()
    ] + [i + 31 for i in range(5)]


def test_add_teams_error_on_duplicate_id(mock_engine: None, seed_teams: dict[int, Team]) -> None:
    with pytest.raises(IntegrityError):
        add_teams([Team(id=1)])


def test_add_team_properties_error_on_duplicate_id(
    mock_engine: None, seed_team_properties: dict[int, TeamProperty]
) -> None:
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=1,
                    season=2022,
                    team_city="City 1",
                    team_name="Name 1",
                    team_tricode="T01",
                    conference=Conference.east,
                    division=Division.atlantic,
                )
            ]
        )


def test_add_team_properties_error_on_invalid_tricode(
    mock_engine: None, seed_team_properties: dict[int, TeamProperty]
) -> None:
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="invalid tricode",
                    conference=Conference.east,
                    division=Division.atlantic,
                )
            ]
        )
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="C",
                    conference=Conference.east,
                    division=Division.atlantic,
                )
            ]
        )


def test_add_team_properties_error_on_incorrect_conference_and_division_combination(
    mock_engine: None, seed_team_properties: dict[int, TeamProperty]
) -> None:
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="T31",
                    conference=Conference.west,
                    division=Division.atlantic,
                )
            ]
        )
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="T31",
                    conference=Conference.west,
                    division=Division.central,
                )
            ]
        )
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="T31",
                    conference=Conference.west,
                    division=Division.southeast,
                )
            ]
        )
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="T31",
                    conference=Conference.east,
                    division=Division.northwest,
                )
            ]
        )
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="T31",
                    conference=Conference.east,
                    division=Division.pacific,
                )
            ]
        )
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="T31",
                    conference=Conference.east,
                    division=Division.southwest,
                )
            ]
        )
    with pytest.raises(IntegrityError):
        add_team_properties(
            [
                TeamProperty(
                    team_id=31,
                    season=2022,
                    team_city="City 31",
                    team_name="Name 31",
                    team_tricode="T31",
                    conference=Conference.east,
                    division=Division.midwest,
                )
            ]
        )
