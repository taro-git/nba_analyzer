from typing import TypedDict

import pytest
from pytest_mock import MockerFixture
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, col, select

from batch.repositories.games.games import upsert_games
from common.models.games.games import Game
from common.types import GameCategory, GameStatus


def _create_game_id(*, category_id: int, season: int, arb: int) -> str:
    return f"00{category_id}{season % 100:02d}{arb:05d}"


def _create_game(
    *,
    game_id: str = "0012699999",
    season: int = 2026,
    start_epoc_sec: int = 1767193200,
    elapsed_sec: int = 0,
    status_id: int = 1,
    category: GameCategory | None = None,
    home_team_id: int = 1610612765,
    away_team_id: int = 1610612756,
    home_score: int = 0,
    away_score: int = 0,
    playoff_label: str | None = None,
) -> Game:
    return Game(
        game_id=game_id,
        season=season,
        start_epoc_sec=start_epoc_sec,
        elapsed_sec=elapsed_sec,
        status=GameStatus.from_status_id(status_id),
        category=category if category is not None else GameCategory.from_game_id(game_id),
        home_team_id=home_team_id,
        away_team_id=away_team_id,
        home_score=home_score,
        away_score=away_score,
        playoff_label=playoff_label,
    )


@pytest.fixture
def mock_engine(engine: Engine, mocker: MockerFixture) -> None:
    mocker.patch("batch.repositories.games.games.engine", engine)


def test_upsert_games_add_one(mock_engine: None, seed_games: dict[str, Game], session: Session) -> None:
    season = 2026
    status_id = 1
    category_id = 1
    game_id = _create_game_id(category_id=category_id, season=season, arb=status_id)
    upsert_games([_create_game(game_id=game_id, season=season, status_id=status_id)])
    result_ids = [g.game_id for g in list(session.exec(select(Game)).all())]
    expected_ids = [i for i in seed_games.keys()] + [game_id]
    assert result_ids == expected_ids


def test_upsert_games_add_many(mock_engine: None, seed_games: dict[str, Game], session: Session) -> None:
    season = 2026
    game_ids: list[str] = []
    data: list[Game] = []
    for category_id in [1, 2, 3, 4, 5, 6, 9]:
        for status_id in [1, 2, 3]:
            game_id = _create_game_id(category_id=category_id, season=season, arb=status_id)
            game_ids.append(game_id)
            playoff_label = "Playoffs" if GameCategory.from_game_id(game_id) == GameCategory.playoffs else None
            data.append(_create_game(game_id=game_id, season=season, status_id=status_id, playoff_label=playoff_label))
    upsert_games(data)
    result_ids = [g.game_id for g in list(session.exec(select(Game)).all())]
    expected_ids = [i for i in seed_games.keys()] + game_ids
    assert result_ids == expected_ids


class NewValue(TypedDict):
    start_epoc_sec: int
    elapsed_sec: int
    status: GameStatus
    home_score: int
    away_score: int


def test_upsert_games_update_one(mock_engine: None, seed_games: dict[str, Game], session: Session) -> None:
    game_id = [i for i in seed_games.keys() if seed_games[i].status == GameStatus.scheduled][0]
    new_value: NewValue = {
        "start_epoc_sec": seed_games[game_id].start_epoc_sec + 100,
        "elapsed_sec": seed_games[game_id].elapsed_sec + 100,
        "status": GameStatus.live,
        "home_score": seed_games[game_id].home_score + 100,
        "away_score": seed_games[game_id].away_score + 100,
    }
    game = Game(
        game_id=game_id,
        season=seed_games[game_id].season,
        start_epoc_sec=new_value["start_epoc_sec"],
        elapsed_sec=new_value["elapsed_sec"],
        status=new_value["status"],
        category=seed_games[game_id].category,
        home_team_id=seed_games[game_id].home_team_id,
        away_team_id=seed_games[game_id].away_team_id,
        home_score=new_value["home_score"],
        away_score=new_value["away_score"],
        playoff_label=seed_games[game_id].playoff_label,
    )
    upsert_games([game])
    session.expire_all()
    result = session.exec(select(Game).where(Game.game_id == game_id)).one()
    assert result.start_epoc_sec == new_value["start_epoc_sec"]
    assert result.elapsed_sec == new_value["elapsed_sec"]
    assert result.status == new_value["status"]
    assert result.home_score == new_value["home_score"]
    assert result.away_score == new_value["away_score"]


def test_upsert_games_update_many(mock_engine: None, seed_games: dict[str, Game], session: Session) -> None:
    scheduled_game_id = [i for i in seed_games.keys() if seed_games[i].status == GameStatus.scheduled][0]
    live_game_id = [i for i in seed_games.keys() if seed_games[i].status == GameStatus.live][0]
    new_values: dict[str, NewValue] = {
        scheduled_game_id: {
            "start_epoc_sec": seed_games[scheduled_game_id].start_epoc_sec + 100,
            "elapsed_sec": seed_games[scheduled_game_id].elapsed_sec + 100,
            "status": GameStatus.live,
            "home_score": seed_games[scheduled_game_id].home_score + 100,
            "away_score": seed_games[scheduled_game_id].away_score + 100,
        },
        live_game_id: {
            "start_epoc_sec": seed_games[live_game_id].start_epoc_sec + 100,
            "elapsed_sec": seed_games[live_game_id].elapsed_sec + 100,
            "status": GameStatus.final,
            "home_score": seed_games[live_game_id].home_score + 100,
            "away_score": seed_games[live_game_id].away_score + 100,
        },
    }
    games = [
        Game(
            game_id=game_id,
            season=seed_games[game_id].season,
            start_epoc_sec=new_values[game_id]["start_epoc_sec"],
            elapsed_sec=new_values[game_id]["elapsed_sec"],
            status=new_values[game_id]["status"],
            category=seed_games[game_id].category,
            home_team_id=seed_games[game_id].home_team_id,
            away_team_id=seed_games[game_id].away_team_id,
            home_score=new_values[game_id]["home_score"],
            away_score=new_values[game_id]["away_score"],
            playoff_label=seed_games[game_id].playoff_label,
        )
        for game_id in [scheduled_game_id, live_game_id]
    ]
    upsert_games(games)
    session.expire_all()
    results = session.exec(select(Game).where(col(Game.game_id).in_([scheduled_game_id, live_game_id]))).all()
    for result in results:
        assert result.start_epoc_sec == new_values[result.game_id]["start_epoc_sec"]
        assert result.elapsed_sec == new_values[result.game_id]["elapsed_sec"]
        assert result.status == new_values[result.game_id]["status"]
        assert result.home_score == new_values[result.game_id]["home_score"]
        assert result.away_score == new_values[result.game_id]["away_score"]


def test_upsert_games_no_action_if_empty(mock_engine: None, seed_games: dict[str, Game], session: Session) -> None:
    upsert_games([])
    results = session.exec(select(Game)).all()
    for result in results:
        assert result.game_id == seed_games[result.game_id].game_id
        assert result.season == seed_games[result.game_id].season
        assert result.start_epoc_sec == seed_games[result.game_id].start_epoc_sec
        assert result.elapsed_sec == seed_games[result.game_id].elapsed_sec
        assert result.status == seed_games[result.game_id].status
        assert result.category == seed_games[result.game_id].category
        assert result.home_team_id == seed_games[result.game_id].home_team_id
        assert result.away_team_id == seed_games[result.game_id].away_team_id
        assert result.home_score == seed_games[result.game_id].home_score
        assert result.away_score == seed_games[result.game_id].away_score
        assert result.playoff_label == seed_games[result.game_id].playoff_label


def test_upsert_games_error_on_invalid_game_id_length(mock_engine: None, seed_games: dict[str, Game]) -> None:
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(game_id="invalid_game_id_length", category=GameCategory.preseason)])


def test_upsert_games_error_on_invalid_incorrect_home_team_and_away_team_combination(
    mock_engine: None, seed_games: dict[str, Game]
) -> None:
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(home_team_id=0, away_team_id=0)])


def test_upsert_games_error_on_negative_score(mock_engine: None, seed_games: dict[str, Game]) -> None:
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(home_score=-1)])
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(away_score=-1)])


def test_upsert_games_error_on_negative_elapsed_sec(mock_engine: None, seed_games: dict[str, Game]) -> None:
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(elapsed_sec=-1)])


def test_upsert_games_error_on_start_epoc_sec_less_than_1983_10_01(
    mock_engine: None, seed_games: dict[str, Game]
) -> None:
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(start_epoc_sec=433814399)])


def test_upsert_games_error_on_playoffs_have_not_playoff_label(mock_engine: None, seed_games: dict[str, Game]) -> None:
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(category=GameCategory.playoffs, playoff_label=None)])


def test_upsert_games_error_on_all_except_playoffs_have_playoff_label(
    mock_engine: None, seed_games: dict[str, Game]
) -> None:
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(category=GameCategory.preseason, playoff_label="preseason")])
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(category=GameCategory.regular_season, playoff_label="regular season")])
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(category=GameCategory.all_star, playoff_label="all star")])
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(category=GameCategory.playin_tournament, playoff_label="play in tournament")])
    with pytest.raises(IntegrityError):
        upsert_games([_create_game(category=GameCategory.nba_cup, playoff_label="nba cup")])
