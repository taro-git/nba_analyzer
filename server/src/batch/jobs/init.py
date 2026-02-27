import logging
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from batch.controllers.sync_by.season import sync_all_by_season
from batch.types import Season

logger = logging.getLogger(__name__)

season = Season.from_datetime(datetime.now())


def _init_jobs(scheduler: BlockingScheduler) -> None:
    """
    システムの初期化ジョブで実行される処理を定義します.
    """
    try:
        if season.start_year < 1970:
            logger.critical("init_job remove")
            scheduler.get_job("init_job").remove()  # type: ignore
        sync_all_by_season(season)
        logger.info(f"init_job success: {season.season_str}")
        season.minus_one_season()
    except Exception as e:
        logger.error(f"error in init_jobs: {e}")


job_func: Callable[[BlockingScheduler], None] = _init_jobs
interval_trigger: IntervalTrigger = IntervalTrigger(minutes=15)


def init_job(scheduler: BlockingScheduler) -> None:
    """
    システムの初期化ジョブを定義します.
    """
    scheduler.add_job(  # type: ignore
        func=job_func,
        args=[scheduler],
        trigger=interval_trigger,
        id="init_job",
        next_run_time=datetime.now().astimezone(),
        replace_existing=True,
    )
