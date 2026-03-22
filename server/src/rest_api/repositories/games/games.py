from datetime import datetime

from sqlmodel import Session, col, select

from common.models.games.games import Game


def get_games_by_start_datetime(session: Session, from_datetime: datetime, to_datetime: datetime) -> list[Game]:
    """
    試合開始時刻の範囲を指定して試合一覧を返します.
    """
    statement = select(Game).where(
        col(Game.start_epoc_sec) >= from_datetime.timestamp(), col(Game.start_epoc_sec) <= to_datetime.timestamp()
    )
    return list(session.exec(statement).all())
