import logging
import os

from apscheduler.schedulers.background import BlockingScheduler

from batch.jobs.daily import daily_job
from common.logging import setup_logging

setup_logging({"apscheduler": logging.INFO})

WITH_INIT = os.getenv("NBA_ANALYZER_BATCH_WITH_INIT", "false").lower() == "true"

scheduler: BlockingScheduler = BlockingScheduler(timezone="Asia/Tokyo")

if WITH_INIT:
    from batch.jobs.init import init_job

    init_job(scheduler)

daily_job(scheduler)

scheduler.start()  # type: ignore
