import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from batch.repositories.commons.seasons import add_seasons, get_newest_season
from common.models.commons.seasons import Season


@pytest.fixture
def seed_seasons(session: Session) -> None:
    seasons = [
        Season(start_year=2022),
        Season(start_year=2021),
        Season(start_year=2020),
    ]
    session.add_all(seasons)
    session.commit()


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> Engine:
    mocker.patch("batch.repositories.commons.seasons.engine", engine)
    return engine


def test_get_newest_season(mock_engine: Engine, seed_seasons: None) -> None:
    result = get_newest_season()
    assert result is not None
    assert result.start_year == 2022


def test_add_seasons_adds_one_season(mock_engine: Engine, seed_seasons: None) -> None:
    add_seasons([Season(start_year=2019)])

    with Session(mock_engine) as session:
        result = session.exec(select(Season)).all()

    assert [s.start_year for s in result] == [2019, 2020, 2021, 2022]


def test_add_seasons_adds_some_seasons(mock_engine: Engine, seed_seasons: None) -> None:
    add_seasons([Season(start_year=2019), Season(start_year=2018)])

    with Session(mock_engine) as session:
        result = session.exec(select(Season)).all()

    assert [s.start_year for s in result] == [2018, 2019, 2020, 2021, 2022]


def test_add_seasons_error_in_duplicate_season(mock_engine: Engine, seed_seasons: None) -> None:
    with pytest.raises(IntegrityError):
        add_seasons([Season(start_year=2022)])


def test_add_seasons_error_in_before_1970(mock_engine: Engine, seed_seasons: None) -> None:
    with pytest.raises(IntegrityError):
        add_seasons([Season(start_year=1969)])
