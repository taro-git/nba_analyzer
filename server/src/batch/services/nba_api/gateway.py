import hashlib
import json
import logging
from datetime import datetime, time, timedelta, timezone
from typing import Any, Callable, ParamSpec, TypeVar, cast

from nba_api.live.nba.endpoints._base import Endpoint as LiveEndpoint
from nba_api.stats.endpoints._base import Endpoint as StatsEndpoint

from batch.repositories.commons.caches import add_cache, get_cache_by_hash, remove_cache
from common.models.commons.caches import Cache

logger = logging.getLogger(__name__)

P = ParamSpec("P")
T = TypeVar("T", bound=StatsEndpoint | LiveEndpoint)


class NbaApiGateway:
    """
    nba_api のゲートウェイクラス.
    """

    default_expires_at = datetime.combine(
        datetime.now().astimezone().date() + timedelta(days=1),
        time.min,
        tzinfo=datetime.now().astimezone().tzinfo,
    ).astimezone(timezone.utc)

    @staticmethod
    def _make_request_hash(
        endpoint_name: str,
        args: tuple[Any, ...],
        kwargs: dict[str, Any],
    ) -> int:
        payload: dict[str, Any] = {
            "endpoint": endpoint_name,
            "args": args,
            "kwargs": kwargs,
        }
        serialized = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        )

        digest = hashlib.sha256(serialized.encode()).digest()

        return int.from_bytes(digest[:8], "big", signed=True)

    @classmethod
    def fetch(
        cls,
        endpoint_cls: Callable[P, T],
        expires_at: datetime = default_expires_at,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> dict[str, Any]:
        """
        Endpoint クラスとパラメータを受け取り、キャッシュされたレスポンスを返します.
        キャッシュが存在しない、もしくは有効期限を過ぎた場合、API を叩いて新規レスポンスをキャッシュして返します.
        """
        try:
            # 短時間で複数回の呼び出しがあるとキャッシュの取得に失敗することがある（ほとんどは成功する）
            # 原因は呼び出しごとに session が別々になっているため
            # TODO: 複数の呼び出し元で session を共有できるようにする
            endpoint = f"{endpoint_cls.__module__}.{endpoint_cls.__name__}"
            hash = cls._make_request_hash(endpoint, args, kwargs)
            cache = get_cache_by_hash(hash)
            if cache:
                if cache.expires_at > datetime.now(timezone.utc):
                    logger.info(f"use cache in fetch: {endpoint}, {args}, {kwargs}")
                    return cache.response
                remove_cache(cache)
            logger.info(f"use endpoint in fetch: {endpoint}, {args}, {kwargs}")
            response = cast(dict[str, Any], endpoint_cls(*args, **kwargs).get_dict())
            logger.info(f"add cache in fetch: {endpoint}, {args}, {kwargs}, expiry to {expires_at}")
            add_cache(Cache(request_hash=hash, response=response, expires_at=expires_at))
            return response
        except Exception as e:
            logger.error(f"error in fetch: {e}")
            raise
