from datetime import date, datetime, timezone

import pytest
from sqlmodel import Session

from common.models.players.players import Player
from common.types import PlayerPosition


@pytest.fixture
def seed_players(session: Session) -> dict[int, Player]:
    """
    Player のテスト用データ
    """

    players = [
        Player(
            id=id,
            updated_at=int(datetime.now(tz=timezone.utc).timestamp()),
            full_name=f"full_name_{id}",
            abbreviation=f"abbreviation_{id}",
            date_of_birth=date(1997, 9, id % 30),
            draft_year=2020 + id % 5,
            position=PlayerPosition.point_guard,
            team_id=1000 + id,
        )
        for id in [1, 2, 3]
    ]
    session.add_all(players)
    session.commit()

    return {p.id: p for p in players}
