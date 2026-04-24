import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Literal, TypedDict

from nba_api.live.nba.endpoints import BoxScore, PlayByPlay
from nba_api.stats.endpoints import BoxScoreTraditionalV3

from batch.repositories.games.game_players import get_game_players_by_game_id
from batch.repositories.games.games import get_game_by_game_id
from batch.repositories.games.stats import add_stats_list
from batch.services.commons.game_clock import (
    convert_from_clock_str_to_seconds,
    convert_from_playtime_str_to_ms,
    create_elapsed_ms_from_clock_and_period,
)
from batch.services.nba_api.gateway import NbaApiGateway
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game
from common.models.games.stats import Stats

logger = logging.getLogger(__name__)


class BoxScoreTraditionalV3Response(TypedDict):
    minutes: str
    fieldGoalsMade: int
    fieldGoalsAttempted: int
    threePointersMade: int
    threePointersAttempted: int
    freeThrowsMade: int
    freeThrowsAttempted: int
    reboundsOffensive: int
    reboundsDefensive: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    foulsPersonal: int
    points: int
    plusMinusPoints: float


class BoxScoreResponse(TypedDict):
    assists: int
    blocks: int
    blocksReceived: int
    fieldGoalsAttempted: int
    fieldGoalsMade: int
    foulsOffensive: int
    foulsDrawn: int
    foulsPersonal: int
    foulsTechnical: int
    freeThrowsAttempted: int
    freeThrowsMade: int
    minutes: str
    plus: float
    plusMinusPoints: float
    points: int
    pointsFastBreak: int
    pointsInThePaint: int
    pointsSecondChance: int
    reboundsDefensive: int
    reboundsOffensive: int
    steals: int
    threePointersAttempted: int
    threePointersMade: int
    turnovers: int


class PlayByPlayResponse(TypedDict):
    clock: str
    period: int
    actionType: Literal["freethrow", "2pt", "3pt", "rebound", "steal", "block", "turnover", "foul", "substitution"]
    """アシストと被ブロックを除く"""
    subType: Literal["offensive", "defensive", "personal", "technical", "out", "in", ""]
    """
    リバウンド、ファウル、選手交代の種類を示す  
    offensive はリバウンド、ファウルの両方を示しうる
    """
    shotResult: Literal["Missed", "Made"] | None
    personId: int
    """リバウンドおよびターンオーバーの加算について、personId が 0 の場合はチーム"""
    teamId: int | None
    assistPersonId: int | None
    """存在していればアシストを加算"""
    blockPlayerName: str | None
    """存在していれば personId のプレイヤーに被ブロックを加算"""
    playerName: str | None
    """テクニカルファウルの加算について、Noneであればチーム、それ以外はプレイヤー"""
    foulDrawnPersonId: int | None
    """存在していれば被ファウルを加算"""


@dataclass
class ActionByElapsed:
    elapsed_ms: int
    action: PlayByPlayResponse


def _init_stats(
    game_id: int,
    game_player_id: int | None = None,
    team_id: int | None = None,
    blocked_shots_received: int | None = 0,
    techical_fouls: int | None = 0,
    fouls_drawn: int | None = 0,
    plus: int | None = 0,
) -> Stats:
    return Stats(
        game_id=game_id,
        team_id=team_id,
        game_player_id=game_player_id,
        elapsed_ms=0,
        ms=0,
        points=0,
        offence_rebounds=0,
        diffence_rebounds=0,
        assists=0,
        steals=0,
        blocks=0,
        field_goal_attempts=0,
        field_goal_made=0,
        three_point_attempts=0,
        three_point_made=0,
        free_throw_attempts=0,
        free_throw_made=0,
        turnovers=0,
        blocked_shots_received=blocked_shots_received,
        personal_fouls=0,
        technical_fouls=techical_fouls,
        fouls_drawn=fouls_drawn,
        plus=plus,
        plus_minus=0,
    )


def _add_to_stats(
    stats: Stats,
    elapsed_ms: int = 0,
    ms: int = 0,
    points: int = 0,
    offence_rebounds: int = 0,
    diffence_rebounds: int = 0,
    assists: int = 0,
    steals: int = 0,
    blocks: int = 0,
    field_goal_attempts: int = 0,
    field_goal_made: int = 0,
    three_point_attempts: int = 0,
    three_point_made: int = 0,
    free_throw_attempts: int = 0,
    free_throw_made: int = 0,
    turnovers: int = 0,
    blocked_shots_received: int = 0,
    personal_fouls: int = 0,
    technical_fouls: int = 0,
    fouls_drawn: int = 0,
    plus: int = 0,
    plus_minus: int = 0,
) -> Stats:
    return Stats(
        game_id=stats.game_id,
        team_id=stats.team_id,
        game_player_id=stats.game_player_id,
        elapsed_ms=stats.elapsed_ms + elapsed_ms,
        ms=stats.ms + ms,
        points=stats.points + points,
        offence_rebounds=stats.offence_rebounds + offence_rebounds,
        diffence_rebounds=stats.diffence_rebounds + diffence_rebounds,
        assists=stats.assists + assists,
        steals=stats.steals + steals,
        blocks=stats.blocks + blocks,
        field_goal_attempts=stats.field_goal_attempts + field_goal_attempts,
        field_goal_made=stats.field_goal_made + field_goal_made,
        three_point_attempts=stats.three_point_attempts + three_point_attempts,
        three_point_made=stats.three_point_made + three_point_made,
        free_throw_attempts=stats.free_throw_attempts + free_throw_attempts,
        free_throw_made=stats.free_throw_made + free_throw_made,
        turnovers=stats.turnovers + turnovers,
        blocked_shots_received=stats.blocked_shots_received + blocked_shots_received
        if stats.blocked_shots_received is not None
        else None,
        personal_fouls=stats.personal_fouls + personal_fouls,
        technical_fouls=stats.technical_fouls + technical_fouls if stats.technical_fouls is not None else None,
        fouls_drawn=stats.fouls_drawn + fouls_drawn if stats.fouls_drawn is not None else None,
        plus=stats.plus + plus if stats.plus is not None else None,
        plus_minus=stats.plus_minus + plus_minus,
    )


def _calc_plus_minus_from_actions(actions: list[PlayByPlayResponse], team_id: int) -> int:
    plus_minus = 0
    for action in actions:
        if action.get("shotResult", None) == "Made":
            match action["actionType"]:
                case "freethrow":
                    point = 1
                case "2pt":
                    point = 2
                case "3pt":
                    point = 3
                case _:
                    point = 0
            plus_minus += point if action["teamId"] == team_id else -point
    return plus_minus


def _calc_additional_stats_by_player_or_team_id_from_actions(
    actions: list[PlayByPlayResponse],
) -> dict[int, dict[str, int]]:
    """
    player(or team)_id: additional_stats_dict の形式
    """
    calc: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for action in actions:
        team_id = action.get("teamId", None)
        if team_id is None:
            continue

        if (assist_player_id := action.get("assistPersonId", None)) is not None:
            calc[assist_player_id]["assists"] += 1

        if (foul_drawn_player_id := action.get("foulDrawnPersonId", None)) is not None:
            calc[foul_drawn_player_id]["fouls_drawn"] += 1

        person_id = action["personId"]
        action_principal_id = person_id if action.get("playerName", None) is not None else team_id
        if action.get("blockPlayerName", None) is not None:
            calc[action_principal_id]["blocked_shots_received"] += 1
        match action["actionType"]:
            case "freethrow":
                calc[action_principal_id]["free_throw_attempts"] += 1
                if action.get("shotResult", None) == "Made":
                    calc[action_principal_id]["free_throw_made"] += 1
                    calc[action_principal_id]["points"] += 1
            case "2pt":
                calc[action_principal_id]["field_goal_attempts"] += 1
                if action.get("shotResult", None) == "Made":
                    calc[action_principal_id]["field_goal_made"] += 1
                    calc[action_principal_id]["points"] += 2
            case "3pt":
                calc[action_principal_id]["field_goal_attempts"] += 1
                calc[action_principal_id]["three_point_attempts"] += 1
                if action.get("shotResult", None) == "Made":
                    calc[action_principal_id]["field_goal_made"] += 1
                    calc[action_principal_id]["three_point_made"] += 1
                    calc[action_principal_id]["points"] += 3
            case "rebound":
                if action["subType"] == "offensive":
                    calc[action_principal_id]["offence_rebounds"] += 1
                if action["subType"] == "defensive":
                    calc[action_principal_id]["diffence_rebounds"] += 1
            case "steal":
                calc[action_principal_id]["steals"] += 1
            case "block":
                calc[action_principal_id]["blocks"] += 1
            case "turnover":
                calc[action_principal_id]["turnovers"] += 1
            case "foul":
                if action["subType"] == "personal":
                    calc[action_principal_id]["personal_fouls"] += 1
                if action["subType"] == "technical":
                    calc[action_principal_id]["technical_fouls"] += 1
            case _:
                pass

    return calc


def _substitute_players_from_actions(
    actions: list[PlayByPlayResponse], game_players: dict[int, GamePlayer], on_court_game_player_ids: set[int]
) -> dict[int, GamePlayer]:
    out_player_ids = {a["personId"] for a in actions if a["actionType"] == "substitution" and a["subType"] == "out"}
    in_player_ids = {a["personId"] for a in actions if a["actionType"] == "substitution" and a["subType"] == "in"}
    return {
        i: p
        for i, p in game_players.items()
        if i in in_player_ids or (i not in out_player_ids and i in on_court_game_player_ids)
    }


def _create_game_stats_from_stats_endpoint(game: Game) -> list[Stats]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    box_score_traditional_v3 = NbaApiGateway.fetch(BoxScoreTraditionalV3, game_id=game.game_id)
    box_score_traditional_v3_players: dict[int, BoxScoreTraditionalV3Response] = {}
    team_keys = ["homeTeam", "awayTeam"]
    for team_key in team_keys:
        for player in box_score_traditional_v3["boxScoreTraditional"][team_key]["players"]:
            box_score_traditional_v3_players[player["personId"]] = player["statistics"]
    elapsed_ms = (
        round(
            convert_from_clock_str_to_seconds(
                box_score_traditional_v3["boxScoreTraditional"]["homeTeam"]["statistics"]["minutes"]
            )
            / 5
        )
        * 1000
    )
    game_players: dict[int, int] = {
        p.player_id: p.id for p in get_game_players_by_game_id(game.id) if p.id is not None and p.is_active
    }
    return [
        Stats(
            game_id=game.id,
            game_player_id=game_players[id],
            elapsed_ms=elapsed_ms,
            ms=convert_from_clock_str_to_seconds(box_score_traditional_v3_players[id]["minutes"]) * 1000,
            points=box_score_traditional_v3_players[id]["points"],
            offence_rebounds=box_score_traditional_v3_players[id]["reboundsOffensive"],
            diffence_rebounds=box_score_traditional_v3_players[id]["reboundsDefensive"],
            assists=box_score_traditional_v3_players[id]["assists"],
            steals=box_score_traditional_v3_players[id]["steals"],
            blocks=box_score_traditional_v3_players[id]["blocks"],
            field_goal_attempts=box_score_traditional_v3_players[id]["fieldGoalsAttempted"],
            field_goal_made=box_score_traditional_v3_players[id]["fieldGoalsMade"],
            three_point_attempts=box_score_traditional_v3_players[id]["threePointersAttempted"],
            three_point_made=box_score_traditional_v3_players[id]["threePointersMade"],
            free_throw_attempts=box_score_traditional_v3_players[id]["freeThrowsAttempted"],
            free_throw_made=box_score_traditional_v3_players[id]["freeThrowsMade"],
            turnovers=box_score_traditional_v3_players[id]["turnovers"],
            personal_fouls=box_score_traditional_v3_players[id]["foulsPersonal"],
            plus_minus=int(box_score_traditional_v3_players[id]["plusMinusPoints"]),
        )
        for id in game_players.keys()
    ] + [
        Stats(
            game_id=game.id,
            team_id=box_score_traditional_v3["boxScoreTraditional"][key]["teamId"],
            elapsed_ms=elapsed_ms,
            ms=elapsed_ms,
            points=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["points"],
            offence_rebounds=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["reboundsOffensive"],
            diffence_rebounds=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["reboundsDefensive"],
            assists=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["assists"],
            steals=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["steals"],
            blocks=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["blocks"],
            field_goal_attempts=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"][
                "fieldGoalsAttempted"
            ],
            field_goal_made=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["fieldGoalsMade"],
            three_point_attempts=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"][
                "threePointersAttempted"
            ],
            three_point_made=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["threePointersMade"],
            free_throw_attempts=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"][
                "freeThrowsAttempted"
            ],
            free_throw_made=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["freeThrowsMade"],
            turnovers=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["turnovers"],
            personal_fouls=box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["foulsPersonal"],
            plus_minus=int(box_score_traditional_v3["boxScoreTraditional"][key]["statistics"]["plusMinusPoints"]),
        )
        for key in team_keys
    ]


def _create_game_stats_from_live_playbyplay(game: Game) -> list[Stats]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    game_players: dict[int, GamePlayer] = {p.player_id: p for p in get_game_players_by_game_id(game.id)}
    stats: list[Stats] = [
        _init_stats(game.id, game_player_id=p.id) for p in game_players.values() if p.id is not None
    ] + [_init_stats(game.id, team_id=i) for i in [game.home_team_id, game.away_team_id]]
    on_court_game_players: dict[int, GamePlayer] = {
        p.player_id: p for p in get_game_players_by_game_id(game.id) if p.is_starter
    }
    live_playbyplay = NbaApiGateway.fetch(PlayByPlay, game_id=game.game_id)
    actions: list[ActionByElapsed] = [
        ActionByElapsed(elapsed_ms=create_elapsed_ms_from_clock_and_period(a["clock"], a["period"]), action=a)
        for a in live_playbyplay["game"]["actions"]
    ]
    for elapsed_ms in sorted({a.elapsed_ms for a in actions}):
        actions_in_the_elapsed_ms = [a.action for a in actions if a.elapsed_ms == elapsed_ms]
        additional_stats_by_id = _calc_additional_stats_by_player_or_team_id_from_actions(actions_in_the_elapsed_ms)
        sum_of_players_additional_stats_by_team_id: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        for player_id, stats_dict in additional_stats_by_id.items():
            if player_id in game_players.keys():
                for k, v in stats_dict.items():
                    sum_of_players_additional_stats_by_team_id[
                        game.home_team_id if game_players[player_id].is_home else game.away_team_id
                    ][k] += v
        home_team_plus_minus = _calc_plus_minus_from_actions(actions_in_the_elapsed_ms, game.home_team_id)
        for game_player in [p for p in game_players.values()]:
            last_stats = sorted(
                [s for s in stats if s.game_player_id == game_player.id], key=lambda s: s.elapsed_ms, reverse=True
            )[0]
            additional_stats_dict = additional_stats_by_id.get(game_player.player_id, {})
            if game_player.id in {p.id for p in on_court_game_players.values()}:
                if game_player.is_home:
                    stats.append(
                        _add_to_stats(
                            last_stats,
                            elapsed_ms=elapsed_ms - last_stats.elapsed_ms,
                            ms=elapsed_ms - last_stats.elapsed_ms,
                            plus=max([home_team_plus_minus, 0]),
                            plus_minus=home_team_plus_minus,
                            **additional_stats_dict,
                        )
                    )
                else:
                    stats.append(
                        _add_to_stats(
                            last_stats,
                            elapsed_ms=elapsed_ms - last_stats.elapsed_ms,
                            ms=elapsed_ms - last_stats.elapsed_ms,
                            plus=abs(min([home_team_plus_minus, 0])),
                            plus_minus=-home_team_plus_minus,
                            **additional_stats_dict,
                        )
                    )
            else:
                stats.append(
                    _add_to_stats(last_stats, elapsed_ms=elapsed_ms - last_stats.elapsed_ms, **additional_stats_dict)
                )
        for team_id in [game.home_team_id, game.away_team_id]:
            last_stats = sorted([s for s in stats if s.team_id == team_id], key=lambda s: s.elapsed_ms, reverse=True)[0]
            additional_stats_dict = additional_stats_by_id.get(team_id, {})
            players_stats = sum_of_players_additional_stats_by_team_id.get(team_id, {})
            merged_stats = defaultdict(int, additional_stats_dict)
            for k, v in players_stats.items():
                merged_stats[k] += v
            if team_id == game.home_team_id:
                stats.append(
                    _add_to_stats(
                        last_stats,
                        elapsed_ms=elapsed_ms - last_stats.elapsed_ms,
                        ms=(elapsed_ms - last_stats.elapsed_ms) * 5,
                        plus=max([home_team_plus_minus, 0]),
                        plus_minus=home_team_plus_minus,
                        **merged_stats,
                    )
                )
            else:
                stats.append(
                    _add_to_stats(
                        last_stats,
                        elapsed_ms=elapsed_ms - last_stats.elapsed_ms,
                        ms=(elapsed_ms - last_stats.elapsed_ms) * 5,
                        plus=abs(min([home_team_plus_minus, 0])),
                        plus_minus=-home_team_plus_minus,
                        **merged_stats,
                    )
                )
        on_court_game_players = _substitute_players_from_actions(
            actions_in_the_elapsed_ms, game_players, set(on_court_game_players.keys())
        )

    return stats


def _create_game_stats_from_live_boxscore(game: Game) -> list[Stats]:
    if game.id is None:
        raise ValueError(f"game is not existing in db {game.game_id}")
    live_boxscore = NbaApiGateway.fetch(BoxScore, game_id=game.game_id)
    team_keys = ["homeTeam", "awayTeam"]
    live_boxscore_players: dict[int, BoxScoreResponse] = {
        p["personId"]: p["statistics"] for k in team_keys for p in live_boxscore["game"][k]["players"]
    }
    elapsed_ms = create_elapsed_ms_from_clock_and_period(
        live_boxscore["game"]["gameClock"], live_boxscore["game"]["period"]
    )
    game_players: dict[int, int] = {p.player_id: p.id for p in get_game_players_by_game_id(game.id) if p.id is not None}
    return [
        Stats(
            game_id=game.id,
            game_player_id=game_players[id],
            elapsed_ms=elapsed_ms,
            ms=convert_from_playtime_str_to_ms(live_boxscore_players[id]["minutes"]),
            points=live_boxscore_players[id]["points"],
            offence_rebounds=live_boxscore_players[id]["reboundsOffensive"],
            diffence_rebounds=live_boxscore_players[id]["reboundsDefensive"],
            assists=live_boxscore_players[id]["assists"],
            steals=live_boxscore_players[id]["steals"],
            blocks=live_boxscore_players[id]["blocks"],
            field_goal_attempts=live_boxscore_players[id]["fieldGoalsAttempted"],
            field_goal_made=live_boxscore_players[id]["fieldGoalsMade"],
            three_point_attempts=live_boxscore_players[id]["threePointersAttempted"],
            three_point_made=live_boxscore_players[id]["threePointersMade"],
            free_throw_attempts=live_boxscore_players[id]["freeThrowsAttempted"],
            free_throw_made=live_boxscore_players[id]["freeThrowsMade"],
            turnovers=live_boxscore_players[id]["turnovers"],
            blocked_shots_received=live_boxscore_players[id]["blocksReceived"],
            personal_fouls=live_boxscore_players[id]["foulsPersonal"],
            technical_fouls=live_boxscore_players[id]["foulsTechnical"],
            fouls_drawn=live_boxscore_players[id]["foulsDrawn"],
            plus=int(live_boxscore_players[id]["plus"]),
            plus_minus=int(live_boxscore_players[id]["plusMinusPoints"]),
        )
        for id in game_players.keys()
    ] + [
        Stats(
            game_id=game.id,
            team_id=live_boxscore["game"][key]["teamId"],
            elapsed_ms=elapsed_ms,
            ms=convert_from_playtime_str_to_ms(live_boxscore["game"][key]["statistics"]["minutes"]),
            points=live_boxscore["game"][key]["statistics"]["points"],
            offence_rebounds=live_boxscore["game"][key]["statistics"]["reboundsOffensive"],
            diffence_rebounds=live_boxscore["game"][key]["statistics"]["reboundsDefensive"],
            assists=live_boxscore["game"][key]["statistics"]["assists"],
            steals=live_boxscore["game"][key]["statistics"]["steals"],
            blocks=live_boxscore["game"][key]["statistics"]["blocks"],
            field_goal_attempts=live_boxscore["game"][key]["statistics"]["fieldGoalsAttempted"],
            field_goal_made=live_boxscore["game"][key]["statistics"]["fieldGoalsMade"],
            three_point_attempts=live_boxscore["game"][key]["statistics"]["threePointersAttempted"],
            three_point_made=live_boxscore["game"][key]["statistics"]["threePointersMade"],
            free_throw_attempts=live_boxscore["game"][key]["statistics"]["freeThrowsAttempted"],
            free_throw_made=live_boxscore["game"][key]["statistics"]["freeThrowsMade"],
            turnovers=live_boxscore["game"][key]["statistics"]["turnovers"],
            blocked_shots_received=live_boxscore["game"][key]["statistics"]["blocksReceived"],
            personal_fouls=live_boxscore["game"][key]["statistics"]["foulsPersonal"],
            technical_fouls=live_boxscore["game"][key]["statistics"]["foulsTechnical"],
            fouls_drawn=live_boxscore["game"][key]["statistics"]["foulsDrawn"],
            plus=int(live_boxscore["game"][key]["statistics"]["points"]),
            plus_minus=int(
                live_boxscore["game"][key]["statistics"]["points"]
                - live_boxscore["game"][key]["statistics"]["pointsAgainst"]
            ),
        )
        for key in team_keys
    ]


def _create_game_stats_from_live_endpoint(game: Game) -> list[Stats]:
    final_stats = _create_game_stats_from_live_boxscore(game)
    try:
        midpoint_stats = _create_game_stats_from_live_playbyplay(game)
        return midpoint_stats + final_stats
    except Exception as e:
        logger.error(f"error in _create_game_stats_from_live_playbyplay: {game.game_id}, {e}")
        return final_stats


def sync_game_stats_by_game_id(game_id: str) -> None:
    """
    試合IDを指定して、最新のデータと DB のプレイバイプレイを同期する
    """
    try:
        game = get_game_by_game_id(game_id)
        if game is None:
            raise ValueError(f"Game not found: {game_id}")
        try:
            game_stats = _create_game_stats_from_live_endpoint(game)
        except Exception as e:
            logger.info(f"live game_stats endpoint is not available. Try stats endpoint: {game_id}, {e}")
            game_stats = _create_game_stats_from_stats_endpoint(game)
        add_stats_list(game_stats)
    except Exception as e:
        logger.error(f"error in sync_game_stats_by_game_id: {e}")
        raise
