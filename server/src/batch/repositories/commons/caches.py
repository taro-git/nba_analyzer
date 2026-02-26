from datetime import datetime, timezone

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


def get_expired_caches(now: datetime | None = None) -> list[Cache]:
    """
    有効期限を過ぎたキャッシュの一覧を返します.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    with Session(engine) as session:
        statement = select(Cache).where(Cache.expires_at < now)
        return list(session.exec(statement).all())


def add_cache(cache: Cache) -> None:
    """
    Cache を DB に登録します.
    """
    with Session(engine) as session:
        session.add(cache)
        session.commit()


def remove_cache(cache: Cache) -> None:
    """
    Cache を 1 件削除します.
    """
    with Session(engine) as session:
        session.delete(cache)
        session.commit()


def remove_caches(caches: list[Cache]) -> None:
    """
    Cache を複数件削除します.
    """
    hashes = [cache.request_hash for cache in caches]
    if len(hashes) != len(set(hashes)):
        raise ValueError("Duplicate cache.request_hash detected.")
    for cache in caches:
        remove_cache(cache)
