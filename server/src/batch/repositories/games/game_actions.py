from sqlmodel import Session

from common.db import engine
from common.models.games.game_actions import GameAction


def add_game_actions(game_actions: list[GameAction]) -> None:
    """
    GameAction 一覧を DB に登録します.
    """
    with Session(engine) as session:
        session.add_all(game_actions)
        session.commit()
