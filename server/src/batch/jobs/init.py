import logging
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.background import BlockingScheduler

from batch.controllers.sync_by.season import sync_all_by_season
from batch.jobs.commons import interval_trigger, sync_game_job_func, sync_game_job_id
from batch.types import Season

logger = logging.getLogger(__name__)

season = Season.from_datetime(datetime.now())


def _init_season_jobs(scheduler: BlockingScheduler) -> None:
    """
    シーズン単位の初期化処理を定義します.
    """
    try:
        if season.start_year < 1983:
            logger.info("remove init_season_job")
            scheduler.get_job("init_season_job").remove()  # type: ignore
            return
        sync_all_by_season(season)
        logger.info(f"init_season_job success: {season.season_str}")
        season.minus_one_season()
    except Exception as e:
        logger.error(f"error in init_season_job: {e}")


init_season_func: Callable[[BlockingScheduler], None] = _init_season_jobs


def init_job(scheduler: BlockingScheduler) -> None:
    """
    システムの初期化ジョブを定義します.
    """
    scheduler.add_job(  # type: ignore
        func=init_season_func,
        args=[scheduler],
        trigger=interval_trigger,
        id="init_season_job",
        next_run_time=datetime.now().astimezone(),
        replace_existing=True,
    )
    if scheduler.get_job(sync_game_job_id) is None:  # type: ignore
        scheduler.add_job(  # type: ignore
            func=sync_game_job_func,
            args=[scheduler],
            trigger=interval_trigger,
            id=sync_game_job_id,
            next_run_time=datetime.now().astimezone(),
            replace_existing=True,
        )
