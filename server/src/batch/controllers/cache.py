from datetime import datetime, timezone

from batch.services.commons.caches import remove_expired_caches


def delete_expired_caches(now: datetime | None = None) -> None:
    """
    有効期限が切れたキャッシュを削除します.
    """
    if now is None:
        now = datetime.now(timezone.utc)
    remove_expired_caches(now)
