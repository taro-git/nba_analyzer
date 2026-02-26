import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlmodel import Session, select

from batch.repositories.teams.regular_season_team_standings import upsert_regular_season_team_standings
from common.models.teams.regular_season_team_standings import RegularSeasonTeamStanding


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> Engine:
    mocker.patch("batch.repositories.teams.regular_season_team_standings.engine", engine)
    return engine


def test_upsert_regular_season_team_standings_adds_one_standing(
    mock_engine: Engine, seed_standings: dict[int, list[RegularSeasonTeamStanding]]
) -> None:
    new_standing = RegularSeasonTeamStanding(
        season=2024,
        team_id=1,
        rank=1,
        win=10,
        lose=5,
    )

    upsert_regular_season_team_standings([new_standing])

    with Session(mock_engine) as session:
        result = session.exec(
            select(RegularSeasonTeamStanding).where(
                RegularSeasonTeamStanding.season == 2024,
                RegularSeasonTeamStanding.team_id == 1,
            )
        ).one()

    assert result.rank == 1
    assert result.win == 10


def test_upsert_regular_season_team_standings_adds_some_standings(
    mock_engine: Engine, seed_standings: dict[int, list[RegularSeasonTeamStanding]]
) -> None:
    new_data = [RegularSeasonTeamStanding(season=2024, team_id=i, rank=i, win=20 - i, lose=i) for i in range(1, 6)]

    upsert_regular_season_team_standings(new_data)

    with Session(mock_engine) as session:
        result = session.exec(select(RegularSeasonTeamStanding).where(RegularSeasonTeamStanding.season == 2024)).all()

    assert len(result) == 5


def test_upsert_regular_season_team_standings_updates_one_standing(
    mock_engine: Engine, seed_standings: dict[int, list[RegularSeasonTeamStanding]]
) -> None:
    updated = RegularSeasonTeamStanding(
        season=2023,
        team_id=1,
        rank=99,
        win=99,
        lose=0,
    )

    upsert_regular_season_team_standings([updated])

    with Session(mock_engine) as session:
        result = session.exec(
            select(RegularSeasonTeamStanding).where(
                RegularSeasonTeamStanding.season == 2023,
                RegularSeasonTeamStanding.team_id == 1,
            )
        ).one()

    assert result.rank == 99
    assert result.win == 99


def test_upsert_regular_season_team_standings_updates_some_standings(
    mock_engine: Engine, seed_standings: dict[int, list[RegularSeasonTeamStanding]]
) -> None:
    updates = [
        RegularSeasonTeamStanding(
            season=2023,
            team_id=i,
            rank=50 + i,
            win=50,
            lose=10,
        )
        for i in range(1, 6)
    ]

    upsert_regular_season_team_standings(updates)

    with Session(mock_engine) as session:
        result = session.exec(select(RegularSeasonTeamStanding).where(RegularSeasonTeamStanding.season == 2023)).all()

    for r in result:
        if r.team_id <= 5:
            assert r.rank == 50 + r.team_id


def test_upsert_regular_season_team_standings_no_action_if_empty(
    mock_engine: Engine, seed_standings: dict[int, list[RegularSeasonTeamStanding]]
) -> None:
    empty: list[RegularSeasonTeamStanding] = []

    upsert_regular_season_team_standings(empty)

    with Session(mock_engine) as session:
        result_2022 = session.exec(
            select(RegularSeasonTeamStanding).where(RegularSeasonTeamStanding.season == 2022)
        ).all()
        result_2023 = session.exec(
            select(RegularSeasonTeamStanding).where(RegularSeasonTeamStanding.season == 2023)
        ).all()

    assert [s.team_id for s in result_2022] == [s.team_id for s in seed_standings[2022]]
    assert [s.rank for s in result_2022] == [s.rank for s in seed_standings[2022]]
    assert [s.win for s in result_2022] == [s.win for s in seed_standings[2022]]
    assert [s.lose for s in result_2022] == [s.lose for s in seed_standings[2022]]
    assert [s.team_id for s in result_2023] == [s.team_id for s in seed_standings[2023]]
    assert [s.rank for s in result_2023] == [s.rank for s in seed_standings[2023]]
    assert [s.win for s in result_2023] == [s.win for s in seed_standings[2023]]
    assert [s.lose for s in result_2023] == [s.lose for s in seed_standings[2023]]
