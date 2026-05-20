from datetime import datetime, timezone

from sqlmodel import Session

from common.models.teams.teams import TeamProperty
from rest_api.repositories.games.game_actions import get_game_actions_by_game
from rest_api.repositories.games.game_players import get_game_players_by_game
from rest_api.repositories.games.games import get_game_by_game_id
from rest_api.repositories.games.stats import get_stats_list_by_game
from rest_api.repositories.players.players import get_players_by_player_ids
from rest_api.repositories.teams.teams import get_team_properties_by_ids
from rest_api.schemas.commons import GameCategory, GameStatus, Season
from rest_api.schemas.games.game_detail import GameDetailSchema, Play, PlayerStats, Statics, TeamStats
from rest_api.schemas.teams.regular_season import Team


def get_game_detail_by_game_id(session: Session, game_id: str) -> GameDetailSchema:
    """
    試合ID を指定して GameDetailSchema を返します.
    """
    game = get_game_by_game_id(session, game_id)
    if game is None:
        raise ValueError(f"Game not found: {game_id}")
    team_properties: dict[int, TeamProperty] = {
        prop.team_id: prop
        for prop in get_team_properties_by_ids(
            session, Season(f"{game.season}-{(game.season + 1) % 100:02d}"), [game.home_team_id, game.away_team_id]
        )
    }
    game_players = get_game_players_by_game(session, game)
    players = {p.id: p for p in get_players_by_player_ids(session, [player.player_id for player in game_players])}
    stats = get_stats_list_by_game(session, game)
    return GameDetailSchema(
        game_id=game.game_id,
        status=GameStatus(game.status.value),
        category=GameCategory(game.category.value),
        start_datetime=datetime.fromtimestamp(game.start_epoc_sec, tz=timezone.utc),
        elapsed_sec=game.elapsed_sec,
        home_team=Team(
            team_id=game.home_team_id,
            team_name=team_properties[game.home_team_id].team_name,
            team_tricode=team_properties[game.home_team_id].team_tricode,
            team_logo=f"https://cdn.nba.com/logos/nba/{game.home_team_id}/global/L/logo.svg",
        ),
        away_team=Team(
            team_id=game.away_team_id,
            team_name=team_properties[game.away_team_id].team_name,
            team_tricode=team_properties[game.away_team_id].team_tricode,
            team_logo=f"https://cdn.nba.com/logos/nba/{game.away_team_id}/global/L/logo.svg",
        ),
        home_team_score=game.home_score,
        away_team_score=game.away_score,
        playoff_label=game.playoff_label,
        play_by_play=sorted(
            [Play.from_game_action_and_game_players(p, game_players) for p in get_game_actions_by_game(session, game)],
            key=lambda p: p.action_number,
        ),
        home_team_stats=TeamStats(
            statics=sorted(
                [Statics.from_Stats(s) for s in stats if s.team_id == game.home_team_id and s.game_player_id is None],
                key=lambda s: s.elapsed_ms,
            ),
            players=[
                PlayerStats(
                    player_id=p.player_id,
                    team_id=players[p.player_id].team_id,
                    full_name=players[p.player_id].full_name,
                    abbreviation=players[p.player_id].abbreviation,
                    position=p.position,
                    date_of_birth=players[p.player_id].date_of_birth,
                    draft_year=players[p.player_id].draft_year,
                    jearsy_num=p.jearsy_num,
                    is_home=p.is_home,
                    is_starter=p.is_starter,
                    is_active=p.is_active,
                    statics=sorted(
                        [Statics.from_Stats(s) for s in stats if s.game_player_id == p.id], key=lambda s: s.elapsed_ms
                    ),
                )
                for p in game_players
                if p.is_home
            ],
        ),
        away_team_stats=TeamStats(
            statics=sorted(
                [Statics.from_Stats(s) for s in stats if s.team_id == game.away_team_id and s.game_player_id is None],
                key=lambda s: s.elapsed_ms,
            ),
            players=[
                PlayerStats(
                    player_id=p.player_id,
                    team_id=players[p.player_id].team_id,
                    full_name=players[p.player_id].full_name,
                    abbreviation=players[p.player_id].abbreviation,
                    position=p.position,
                    date_of_birth=players[p.player_id].date_of_birth,
                    draft_year=players[p.player_id].draft_year,
                    jearsy_num=p.jearsy_num,
                    is_home=p.is_home,
                    is_starter=p.is_starter,
                    is_active=p.is_active,
                    statics=sorted(
                        [Statics.from_Stats(s) for s in stats if s.game_player_id == p.id], key=lambda s: s.elapsed_ms
                    ),
                )
                for p in game_players
                if not p.is_home
            ],
        ),
    )
