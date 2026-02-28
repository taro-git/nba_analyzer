import pytest
from sqlmodel import Session

from common.models.teams.regular_season_team_standings import RegularSeasonTeamStanding
from common.models.teams.teams import Team, TeamProperty
from common.types import Conference, Division


def _create_standings(season: int) -> list[RegularSeasonTeamStanding]:
    data = [
        RegularSeasonTeamStanding(
            season=season,
            team_id=i,
            rank=i,
            win=15 - i,
            lose=i,
        )
        for i in range(1, 16)
    ]
    data += [
        RegularSeasonTeamStanding(
            season=season,
            team_id=15 + i,
            rank=i,
            win=15 - i,
            lose=i,
        )
        for i in range(1, 16)
    ]
    return data


@pytest.fixture
def seed_standings(session: Session) -> dict[int, list[RegularSeasonTeamStanding]]:
    """
    RegularSeasonTeamStanding の初期データ
    2023-24, 2022-23 のみ
    """
    data_2023 = _create_standings(2023)
    data_2022 = _create_standings(2022)
    session.add_all(data_2023 + data_2022)
    session.commit()

    return {2023: data_2023, 2022: data_2022}


@pytest.fixture
def seed_teams(session: Session) -> dict[int, Team]:
    """
    Team の初期データ
    team_id: 1~30
    """

    teams = [Team(id=i + 1) for i in range(30)]
    session.add_all(teams)
    session.commit()

    return {t.id: t for t in teams}


@pytest.fixture
def seed_team_properties(session: Session) -> dict[int, TeamProperty]:

    east_divisions = (
        [Division.atlantic for _ in range(5)]
        + [Division.central for _ in range(5)]
        + [Division.southeast for _ in range(5)]
    )
    west_divisions = (
        [Division.northwest for _ in range(5)]
        + [Division.pacific for _ in range(5)]
        + [Division.southwest for _ in range(5)]
    )

    data = [
        TeamProperty(
            team_id=i + 1,
            season=2022,
            team_city=f"City {i + 1}",
            team_name=f"Name {i + 1}",
            team_tricode=f"T{i + 1:02d}",
            conference=Conference.east,
            division=division,
        )
        for i, division in enumerate(east_divisions)
    ]
    num_of_east = len(east_divisions)
    data += [
        TeamProperty(
            team_id=i + 1 + num_of_east,
            season=2022,
            team_city=f"City {i + 1 + num_of_east}",
            team_name=f"Name {i + 1 + num_of_east}",
            team_tricode=f"T{i + 1 + num_of_east:02d}",
            conference=Conference.west,
            division=division,
        )
        for i, division in enumerate(west_divisions)
    ]

    session.add_all(data)
    session.commit()

    return {t.team_id: t for t in data}
