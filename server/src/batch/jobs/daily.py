import logging
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from batch.controllers.cache import delete_expired_caches
from batch.controllers.sync_by.season import sync_all_by_season
from batch.jobs.commons import interval_trigger, sync_game_job_func, sync_game_job_id

logger = logging.getLogger(__name__)


def _daily_jobs(scheduler: BlockingScheduler) -> None:
    """
    日次ジョブで実行する処理を定義します.
    """
    try:
        delete_expired_caches()
        sync_all_by_season()
        if scheduler.get_job(sync_game_job_id) is None:  # type: ignore
            scheduler.add_job(  # type: ignore
                func=sync_game_job_func,
                args=[scheduler],
                trigger=interval_trigger,
                id=sync_game_job_id,
                next_run_time=datetime.now().astimezone(),
                replace_existing=True,
            )
        logger.info("daily_job success")
    except Exception as e:
        logger.error(f"error in daily_jobs: {e}")


job_func: Callable[[BlockingScheduler], None] = _daily_jobs
cron_trigger: CronTrigger = CronTrigger(hour=0, minute=0)


def daily_job(scheduler: BlockingScheduler) -> None:
    """
    日次ジョブを定義します.
    """
    scheduler.add_job(  # type: ignore
        func=job_func,
        args=[scheduler],
        trigger=cron_trigger,
        id="daily_job",
        next_run_time=datetime.now().astimezone(),
        replace_existing=True,
    )
