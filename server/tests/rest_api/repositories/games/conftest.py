from datetime import datetime, timedelta, timezone

import pytest
from sqlmodel import Session

from common.models.games.games import Game
from common.types import GameCategory, GameStatus


def _create_games(from_utc: datetime, to_utc: datetime) -> list[Game]:
    data: list[Game] = []
    if to_utc < from_utc:
        return data
    for days in [i for i in range((to_utc - from_utc).days + 1)]:
        game_date = from_utc + timedelta(days=days)
        season = game_date.year if game_date.month >= 10 else game_date.year - 1
        game_id = f"002{season % 100:02d}{days:05d}"
        data.append(
            Game(
                game_id=game_id,
                season=season,
                start_epoc_sec=int(game_date.timestamp()),
                elapsed_sec=0,
                status=GameStatus.scheduled,
                category=GameCategory.from_game_id(game_id),
                home_team_id=1610612765,
                away_team_id=1610612756,
                home_score=0,
                away_score=0,
                playoff_label=None,
            )
        )
    return data


@pytest.fixture
def seed_games(session: Session) -> dict[str, Game]:
    """
    Game のテスト用データ
    2025-09-01T00:00:00Z から 2026-01-31T00:00:00Z まで24時間ごとに1試合ずつ
    """

    games = _create_games(datetime(2025, 9, 1, tzinfo=timezone.utc), datetime(2026, 1, 31, tzinfo=timezone.utc))
    session.add_all(games)
    session.commit()

    return {g.game_id: g for g in games}
