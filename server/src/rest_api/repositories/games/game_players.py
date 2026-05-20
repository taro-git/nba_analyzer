from sqlmodel import Session, col, select

from common.models.games.game_players import GamePlayer
from common.models.games.games import Game


def get_game_players_by_game(session: Session, game: Game) -> list[GamePlayer]:
    """
    Game を指定して GamePlayer 一覧を返します.
    """
    statement = select(GamePlayer).where(col(GamePlayer.game_id) == game.id)
    return list(session.exec(statement).all())
