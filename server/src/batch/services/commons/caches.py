from datetime import datetime, timezone

from batch.repositories.commons.caches import get_expired_caches, remove_caches


def remove_expired_caches(now: datetime | None = None) -> None:
    """
    有効期限を過ぎたキャッシュを削除します.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    remove_caches(get_expired_caches(now))
