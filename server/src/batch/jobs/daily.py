import logging
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

from batch.controllers.cache import delete_expired_caches
from batch.controllers.sync_by.season import sync_all_by_season

logger = logging.getLogger(__name__)


def _daily_jobs() -> None:
    """
    日次ジョブで実行する処理を定義します.
    """
    try:
        delete_expired_caches()
        sync_all_by_season()
        logger.info("daily_job success")
    except Exception as e:
        logger.error(f"error in daily_jobs: {e}")


job_func: Callable[[], None] = _daily_jobs
cron_trigger: CronTrigger = CronTrigger(hour=0, minute=0)


def daily_job(scheduler: BlockingScheduler) -> None:
    """
    日次ジョブを定義します.
    """
    scheduler.add_job(  # type: ignore
        func=job_func,
        trigger=cron_trigger,
        id="daily_job",
        next_run_time=datetime.now().astimezone(),
        replace_existing=True,
    )
