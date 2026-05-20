from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session

from common.db import engine
from common.models.players.players import Player


def add_players_and_ignore_existing(players: list[Player]) -> None:
    """
    Player 一覧を DB に登録します.
    一覧に既存 Player が含まれる場合には、当該 Player は無視されます.
    """
    with Session(engine) as session:
        stmt = insert(Player).values([p.model_dump() for p in players])
        stmt = stmt.on_conflict_do_nothing()

        session.exec(stmt)
        session.commit()
