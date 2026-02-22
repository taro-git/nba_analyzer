from sqlmodel import Session, select

from common.db import engine
from common.models.commons.caches import Cache


def get_cache_by_hash(hash: int) -> Cache | None:
    """
    リクエストのハッシュ値を指定して Cache を返します.
    """
    with Session(engine) as session:
        statement = select(Cache).where(Cache.request_hash == hash)
        return session.exec(statement).first()


def add_cache(cache: Cache) -> None:
    """
    Cache を DB に登録します.
    """
    with Session(engine) as session:
        session.add(cache)
        session.commit()
