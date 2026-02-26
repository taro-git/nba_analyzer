import logging
from datetime import datetime

from batch.repositories.commons.seasons import (
    add_seasons,
    get_newest_season,
)
from batch.types import Season
from common.models.commons.seasons import Season as SeasonModel

logger = logging.getLogger(__name__)


def _create_missing_seasons(season: Season) -> list[SeasonModel]:
    """
    未登録の Season を作成します.
    """
    newest = get_newest_season()
    newest_start_year = newest.start_year if newest else 1969
    if newest_start_year >= season.start_year:
        return []
    return [SeasonModel(start_year=i) for i in range(newest_start_year + 1, season.start_year + 1)]


def sync_seasons(season: Season | None = None) -> None:
    """
    DB のシーズンを同期します.
    """
    try:
        if season is None:
            season = Season.from_datetime(datetime.now())
        seasons = _create_missing_seasons(season)
        if len(seasons) >= 1:
            add_seasons(seasons)
    except Exception as e:
        logger.error(f"error in sync_seasons: {e}")
        raise
