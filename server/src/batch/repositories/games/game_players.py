from sqlalchemy.dialects.postgresql import insert
from sqlmodel import Session, col, select

from common.db import engine
from common.models.games.game_players import GamePlayer


def get_game_players_by_game_id(game_id: int) -> list[GamePlayer]:
    """
    Game の内部管理用ID を指定して GamePlayer 一覧を返します.
    """
    with Session(engine) as session:
        statement = select(GamePlayer).where(col(GamePlayer.game_id) == game_id)
        return list(session.exec(statement).all())


def add_game_players_and_ignore_existing(game_players: list[GamePlayer]) -> None:
    """
    GamePlayer 一覧を DB に登録します.
    一覧に既存 GamePlayer が含まれる場合には、当該 GamePlayer は無視されます.
    """
    with Session(engine) as session:
        stmt = insert(GamePlayer).values(
            [p.model_dump(exclude={"id"}) if p.id is None else p.model_dump() for p in game_players]
        )
        stmt = stmt.on_conflict_do_nothing()

        session.exec(stmt)
        session.commit()
