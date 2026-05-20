from sqlmodel import Session, col, select

from common.models.games.game_actions import GameAction
from common.models.games.games import Game


def get_game_actions_by_game(session: Session, game: Game) -> list[GameAction]:
    """
    Game を指定して、GameAction 一覧を返します.
    """
    statement = select(GameAction).where(col(GameAction.game_id) == game.id)
    return list(session.exec(statement).all())
