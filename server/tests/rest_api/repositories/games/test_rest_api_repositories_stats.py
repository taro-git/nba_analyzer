from sqlmodel import Session

from common.models.games.games import Game
from common.types import GameCategory, GameStatus
from rest_api.repositories.games.stats import get_stats_list_by_game
from tests.rest_api.repositories.games.conftest import GameDataSeed


def _create_game(id: int | None) -> Game:
    return Game(
        id=id + 1 if id is not None else None,
        game_id="not_existing",
        season=2022,
        start_epoc_sec=0,
        elapsed_sec=0,
        status=GameStatus.scheduled,
        category=GameCategory.regular_season,
        home_team_id=1610612765,
        away_team_id=1610612756,
        home_score=0,
        away_score=0,
        playoff_label=None,
    )


def test_get_stats_list_by_game_returns_matched_stats(session: Session, seed_stats: list[GameDataSeed]) -> None:
    seed = [s for s in seed_stats if s.game.id is not None][0]
    result = get_stats_list_by_game(session, seed.game)
    assert {s.id for s in seed.stats} == {s.id for s in result}


def test_get_stats_list_by_game_returns_empty_if_not_existing(session: Session, seed_stats: list[GameDataSeed]) -> None:
    max_game_id = max({s.game.id for s in seed_stats if s.game.id is not None})
    result = get_stats_list_by_game(session, _create_game(max_game_id + 1))
    assert len(result) == 0


def test_get_stats_list_by_game_returns_empty_if_game_id_is_none(
    session: Session, seed_stats: list[GameDataSeed]
) -> None:
    result = get_stats_list_by_game(session, _create_game(None))
    assert len(result) == 0
