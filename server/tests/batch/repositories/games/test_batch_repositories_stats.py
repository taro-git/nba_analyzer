import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlmodel import Session, select

from batch.repositories.games.stats import add_stats_list, get_all_stats_list
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game
from common.models.games.stats import Stats
from tests.batch.repositories.games.conftest import AWAY_TEAM_ID, HOME_TEAM_ID


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> None:
    mocker.patch("batch.repositories.games.stats.engine", engine)


def _make_stats(
    game_id: int, *, game_player_id: int | None = None, team_id: int | None = None, elapsed_ms: int = 0
) -> Stats:
    return Stats(
        game_id=game_id,
        game_player_id=game_player_id,
        team_id=team_id,
        elapsed_ms=elapsed_ms,
        ms=0,
        points=10,
        offence_rebounds=1,
        diffence_rebounds=2,
        assists=3,
        steals=1,
        blocks=0,
        field_goal_attempts=8,
        field_goal_made=4,
        three_point_attempts=3,
        three_point_made=1,
        free_throw_attempts=2,
        free_throw_made=2,
        turnovers=1,
        personal_fouls=2,
        plus_minus=5,
    )


def test_add_stats_list_adds_player_stats(
    mock_engine: None, seed_game: Game, seed_game_players: list[GamePlayer], session: Session
) -> None:
    assert seed_game.id is not None
    gp = seed_game_players[0]
    add_stats_list([_make_stats(seed_game.id, game_player_id=gp.id)])
    result = session.exec(select(Stats)).all()
    assert len(result) == 1
    assert result[0].game_player_id == gp.id
    assert result[0].points == 10


def test_add_stats_list_adds_team_stats(mock_engine: None, seed_game: Game, session: Session) -> None:
    assert seed_game.id is not None
    add_stats_list([_make_stats(seed_game.id, team_id=HOME_TEAM_ID)])
    result = session.exec(select(Stats)).all()
    assert len(result) == 1
    assert result[0].team_id == HOME_TEAM_ID


def test_add_stats_list_adds_many(
    mock_engine: None, seed_game: Game, seed_game_players: list[GamePlayer], session: Session
) -> None:
    assert seed_game.id is not None
    stats = [
        _make_stats(seed_game.id, game_player_id=seed_game_players[0].id, elapsed_ms=60000),
        _make_stats(seed_game.id, game_player_id=seed_game_players[1].id, elapsed_ms=60000),
        _make_stats(seed_game.id, team_id=HOME_TEAM_ID, elapsed_ms=60000),
        _make_stats(seed_game.id, team_id=AWAY_TEAM_ID, elapsed_ms=60000),
    ]
    add_stats_list(stats)
    result = session.exec(select(Stats)).all()
    assert len(result) == 4


def test_add_stats_list_no_action_if_empty(mock_engine: None, seed_game: Game, session: Session) -> None:
    add_stats_list([])
    result = session.exec(select(Stats)).all()
    assert len(result) == 0


def test_get_all_stats_list_returns_all(
    mock_engine: None, seed_game: Game, seed_game_players: list[GamePlayer], session: Session
) -> None:
    assert seed_game.id is not None
    stats = [
        _make_stats(seed_game.id, game_player_id=seed_game_players[0].id),
        _make_stats(seed_game.id, team_id=HOME_TEAM_ID),
    ]
    session.add_all(stats)
    session.commit()

    result = get_all_stats_list()
    assert len(result) == 2


def test_get_all_stats_list_returns_empty_when_no_data(mock_engine: None, seed_game: Game) -> None:
    result = get_all_stats_list()
    assert result == []
