from batch.services.games.game_actions import sync_game_actions_by_game_id
from batch.services.games.game_players import sync_game_players_by_game_id
from batch.services.games.stats import sync_game_stats_by_game_id
from batch.services.players.players import sync_players_by_game_id


def sync_all_by_game(game_id: str) -> None:
    """
    試合ID を指定して、最新のデータと DB を同期します.
    """
    sync_players_by_game_id(game_id)
    sync_game_players_by_game_id(game_id)
    sync_game_actions_by_game_id(game_id)
    sync_game_stats_by_game_id(game_id)
