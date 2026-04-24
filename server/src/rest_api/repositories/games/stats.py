from sqlmodel import Session, col, select

from common.models.games.games import Game
from common.models.games.stats import Stats


def get_stats_list_by_game(session: Session, game: Game) -> list[Stats]:
    """
    Game を指定して Stats 一覧を返します.
    """
    statement = select(Stats).where(col(Stats.game_id) == game.id)
    return list(session.exec(statement).all())
