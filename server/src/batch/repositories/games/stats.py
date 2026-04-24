from sqlmodel import Session, select

from common.db import engine
from common.models.games.stats import Stats


def get_all_stats_list() -> list[Stats]:
    """
    Stats 一覧を返します.
    """
    with Session(engine) as session:
        return list(session.exec(select(Stats)).all())


def add_stats_list(stats_list: list[Stats]) -> None:
    """
    Stats 一覧を DB に登録します.
    """
    with Session(engine) as session:
        session.add_all(stats_list)
        session.commit()
