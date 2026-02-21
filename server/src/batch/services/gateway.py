import hashlib
import json
from datetime import datetime, time, timedelta, timezone
from typing import Any, Callable, ParamSpec, TypeVar, cast

from nba_api.live.nba.endpoints._base import Endpoint as LiveEndpoint
from nba_api.stats.endpoints._base import Endpoint as StatsEndpoint

from batch.repositories.commons.caches import create_cache, get_cache_by_hash
from common.models.commons.caches import Cache

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
        hash = cls._make_request_hash(f"{endpoint_cls.__module__}.{endpoint_cls.__name__}", args, kwargs)
        cache = get_cache_by_hash(hash)
        if cache and cache.expires_at > datetime.now(timezone.utc):
            return cache.response
        instance = endpoint_cls(*args, **kwargs)
        response = cast(dict[str, Any], instance.get_dict())
        create_cache(Cache(request_hash=hash, response=response, expires_at=expires_at))
        return response
