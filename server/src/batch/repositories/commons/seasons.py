from sqlmodel import Session, desc, select

from common.db import engine
from common.models.commons.seasons import Season


def get_newest_season() -> Season | None:
    """
    最新シーズンを取得します.
    """
    with Session(engine) as session:
        statement = select(Season).order_by(desc(Season.start_year)).limit(1)
        return session.exec(statement).first()


def add_seasons(seasons: list[Season]) -> None:
    """
    Season のリストを DB に登録します.
    """
    with Session(engine) as session:
        session.add_all(seasons)
        session.commit()
