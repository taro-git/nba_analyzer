from sqlmodel import Session, col, select

from common.models.players.players import Player


def get_players_by_player_ids(session: Session, player_ids: list[int]) -> list[Player]:
    """
    選手ID 一覧を指定して、対応する Player 一覧を返します.
    """
    statement = select(Player).where(col(Player.id).in_(player_ids))
    return list(session.exec(statement).all())
