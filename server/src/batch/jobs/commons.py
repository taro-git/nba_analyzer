import logging
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from batch.controllers.games import get_unninitialized_games_by_start_datetime
from batch.controllers.sync_by.game import sync_all_by_game
from common.types import GameStatus

logger = logging.getLogger(__name__)


def _sync_game_jobs(scheduler: BlockingScheduler) -> None:
    """
    試合のデータ同期処理を定義します.
    """
    try:
        games = get_unninitialized_games_by_start_datetime(
            from_datetime=datetime(1983, 10, 1),
            to_datetime=datetime.now(),
            status=GameStatus.final,
        )
        games.sort(reverse=True, key=lambda game: game.start_epoc_sec)
        if len(games) > 0:
            sync_all_by_game(games[0].game_id)
            logger.info(f"sync_game_job success: {games[0].game_id}")
        else:
            logger.info("remove sync_game_job")
            scheduler.get_job(sync_game_job_id).remove()  # type: ignore
    except Exception as e:
        logger.error(f"error in sync_game_job: {e}")


sync_game_job_func: Callable[[BlockingScheduler], None] = _sync_game_jobs
sync_game_job_id = "sync_game_job"
interval_trigger: IntervalTrigger = IntervalTrigger(minutes=15)
