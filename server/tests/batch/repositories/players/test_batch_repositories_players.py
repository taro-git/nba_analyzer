import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlmodel import Session, select

from batch.repositories.players.players import add_players_and_ignore_existing
from common.models.players.players import Player


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> None:
    mocker.patch("batch.repositories.players.players.engine", engine)


def _make_player(player_id: int, full_name: str = "Test Player") -> Player:
    return Player(
        id=player_id,
        updated_at=1767193200,
        full_name=full_name,
        abbreviation=f"{full_name[0]}. {full_name.split()[-1]}",
    )


def test_add_players_and_ignore_existing_adds_one(mock_engine: None, session: Session) -> None:
    add_players_and_ignore_existing([_make_player(1001)])
    result = session.exec(select(Player)).all()
    assert len(result) == 1
    assert result[0].id == 1001


def test_add_players_and_ignore_existing_adds_many(mock_engine: None, session: Session) -> None:
    players = [_make_player(i) for i in range(1001, 1006)]
    add_players_and_ignore_existing(players)
    result = session.exec(select(Player)).all()
    assert len(result) == 5


def test_add_players_and_ignore_existing_adds_only_new(mock_engine: None, session: Session) -> None:
    players = [_make_player(i) for i in range(1001, 1006)]
    session.add(Player(id=1001, updated_at=1767193200, full_name="Existing Player", abbreviation="E. Player"))
    session.commit()
    result = session.exec(select(Player)).all()
    assert len(result) == 1
    add_players_and_ignore_existing(players)
    result = session.exec(select(Player)).all()
    assert len(result) == 5
    assert [p.full_name for p in result if p.id == 1001] == ["Existing Player"]
