from datetime import datetime, timezone

import pytest
from pytest_mock import MockerFixture
from sqlmodel import Session

from common.models.games.game_actions import GameAction
from common.models.games.game_players import GamePlayer
from common.models.games.games import Game
from common.models.games.stats import Stats
from common.models.players.players import Player
from common.models.teams.teams import TeamProperty
from common.settings import NBA_PERIOD_SECONDS
from common.types import Conference, Division, GameCategory, GameStatus
from rest_api.controllers.games.game_detail import get_game_detail_by_game_id
from rest_api.schemas.commons import GameCategory as GameCategorySchema
from rest_api.schemas.commons import GameStatus as GameStatusSchema
from rest_api.schemas.games.game_detail import GameDetailSchema, PlayerStats

GAME_INNTERNAL_ID = 1
HOME_TEAM_ID = 1
AWAY_TEAM_ID = 2
HOME_PLAYER_INTERNAL_IDS = list(range(10))
AWAY_PLAYER_INTERNAL_IDS = list(range(10, 20))
PLAYER_IDS = {i: i + 100 for i in HOME_PLAYER_INTERNAL_IDS + AWAY_PLAYER_INTERNAL_IDS}


def mocker_patch(
    mocker: MockerFixture,
    mock_game: Game | None,
    mock_game_actions: list[GameAction],
    mock_game_players: list[GamePlayer],
    mock_stats: list[Stats],
    mock_players: list[Player],
    mock_teams: list[TeamProperty],
) -> None:
    mocker.patch(
        "rest_api.controllers.games.game_detail.get_game_by_game_id",
        return_value=mock_game,
    )
    mocker.patch(
        "rest_api.controllers.games.game_detail.get_game_actions_by_game",
        return_value=mock_game_actions,
    )
    mocker.patch(
        "rest_api.controllers.games.game_detail.get_game_players_by_game",
        return_value=mock_game_players,
    )
    mocker.patch(
        "rest_api.controllers.games.game_detail.get_stats_list_by_game",
        return_value=mock_stats,
    )
    mocker.patch(
        "rest_api.controllers.games.game_detail.get_players_by_player_ids",
        return_value=mock_players,
    )

    mocker.patch(
        "rest_api.controllers.games.game_detail.get_team_properties_by_ids",
        return_value=mock_teams,
    )


def _create_game() -> Game:
    season = 2023
    return Game(
        id=GAME_INNTERNAL_ID,
        game_id=f"002{season % 100:02d}00001",
        season=season,
        start_epoc_sec=int(datetime(season, 1, 1, tzinfo=timezone.utc).timestamp()),
        elapsed_sec=NBA_PERIOD_SECONDS * 4,
        status=GameStatus.final,
        category=GameCategory.regular_season,
        home_team_id=HOME_TEAM_ID,
        away_team_id=AWAY_TEAM_ID,
        home_score=0,
        away_score=0,
        playoff_label=None,
    )


def _create_game_actions() -> list[GameAction]:
    return [
        GameAction(
            game_id=GAME_INNTERNAL_ID,
            action_number=i,
            elapsed_ms=i * 1000,
            description=f"action {i}",
            action_type=f"action type {i}",
        )
        for i in range(10)
    ]


def _create_game_players() -> list[GamePlayer]:
    return [
        GamePlayer(
            id=i,
            game_id=GAME_INNTERNAL_ID,
            player_id=PLAYER_IDS[i],
            jearsy_num=str(i),
            is_home=True,
            is_starter=False,
            is_active=True,
        )
        for i in HOME_PLAYER_INTERNAL_IDS
    ] + [
        GamePlayer(
            id=i,
            game_id=GAME_INNTERNAL_ID,
            player_id=PLAYER_IDS[i],
            jearsy_num=str(i),
            is_home=False,
            is_starter=False,
            is_active=True,
        )
        for i in AWAY_PLAYER_INTERNAL_IDS
    ]


def _create_stats() -> list[Stats]:
    return [
        Stats(
            game_id=GAME_INNTERNAL_ID,
            game_player_id=i,
            elapsed_ms=erapsed_ms,
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
            blocked_shots_received=0,
            personal_fouls=0,
            technical_fouls=0,
            fouls_drawn=0,
            plus=0,
            plus_minus=0,
        )
        for i in HOME_PLAYER_INTERNAL_IDS + AWAY_PLAYER_INTERNAL_IDS
        for erapsed_ms in range(10)
    ] + [
        Stats(
            game_id=GAME_INNTERNAL_ID,
            team_id=i,
            elapsed_ms=erapsed_ms,
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
            blocked_shots_received=0,
            personal_fouls=0,
            technical_fouls=0,
            fouls_drawn=0,
            plus=0,
            plus_minus=0,
        )
        for i in [HOME_TEAM_ID, AWAY_TEAM_ID]
        for erapsed_ms in range(10)
    ]


def _create_players() -> list[Player]:
    return [
        Player(
            id=PLAYER_IDS[i],
            updated_at=int(datetime.now(tz=timezone.utc).timestamp()),
            full_name=f"full_name_{i}",
            abbreviation=f"abbreviation_{i}",
            team_id=HOME_TEAM_ID,
        )
        for i in HOME_PLAYER_INTERNAL_IDS
    ] + [
        Player(
            id=PLAYER_IDS[i],
            updated_at=int(datetime.now(tz=timezone.utc).timestamp()),
            full_name=f"full_name_{i}",
            abbreviation=f"abbreviation_{i}",
            team_id=AWAY_TEAM_ID,
        )
        for i in AWAY_PLAYER_INTERNAL_IDS
    ]


def _create_teams() -> list[TeamProperty]:
    season = 2023
    return [
        TeamProperty(
            team_id=HOME_TEAM_ID,
            season=season,
            team_name="Team A",
            team_tricode="AAA",
            team_city="City A",
            conference=Conference.east,
            division=Division.atlantic,
        ),
        TeamProperty(
            team_id=AWAY_TEAM_ID,
            season=season,
            team_name="Team B",
            team_tricode="BBB",
            team_city="City B",
            conference=Conference.east,
            division=Division.central,
        ),
    ]


def _is_correct_player_stats(
    result: PlayerStats, mock_game_player: GamePlayer, mock_stats: list[Stats], mock_player: Player
) -> bool:
    return (
        result.player_id == mock_game_player.player_id
        and result.team_id == mock_player.team_id
        and result.full_name == mock_player.full_name
        and result.abbreviation == mock_player.abbreviation
        and result.position == mock_game_player.position
        and result.date_of_birth == mock_player.date_of_birth
        and result.draft_year == mock_player.draft_year
        and result.jearsy_num == mock_game_player.jearsy_num
        and result.is_home == mock_game_player.is_home
        and result.is_active == mock_game_player.is_active
        and result.is_starter == mock_game_player.is_starter
        and [s.elapsed_ms for s in result.statics] == sorted([s.elapsed_ms for s in mock_stats])
    )


def _is_correct_game_detail(
    result: GameDetailSchema,
    mock_game: Game,
    mock_game_actions: list[GameAction],
    mock_game_players: list[GamePlayer],
    mock_stats: list[Stats],
    mock_players: list[Player],
    mock_teams: list[TeamProperty],
) -> bool:
    mock_game_player_by_player_id: dict[int, GamePlayer] = {gp.player_id: gp for gp in mock_game_players}
    mock_player_by_player_id: dict[int, Player] = {p.id: p for p in mock_players}
    return (
        result.game_id == mock_game.game_id
        and result.status == GameStatusSchema(mock_game.status.value)
        and result.category == GameCategorySchema(mock_game.category.value)
        and result.start_datetime == datetime.fromtimestamp(mock_game.start_epoc_sec, tz=timezone.utc)
        and result.elapsed_sec == mock_game.elapsed_sec
        and result.home_team.team_id == mock_game.home_team_id
        and result.home_team.team_name == next(t.team_name for t in mock_teams if t.team_id == mock_game.home_team_id)
        and result.home_team.team_tricode
        == next(t.team_tricode for t in mock_teams if t.team_id == mock_game.home_team_id)
        and result.home_team.team_logo == f"https://cdn.nba.com/logos/nba/{mock_game.home_team_id}/global/L/logo.svg"
        and result.away_team.team_id == mock_game.away_team_id
        and result.away_team.team_name == next(t.team_name for t in mock_teams if t.team_id == mock_game.away_team_id)
        and result.away_team.team_tricode
        == next(t.team_tricode for t in mock_teams if t.team_id == mock_game.away_team_id)
        and result.away_team.team_logo == f"https://cdn.nba.com/logos/nba/{mock_game.away_team_id}/global/L/logo.svg"
        and result.home_team_score == mock_game.home_score
        and result.away_team_score == mock_game.away_score
        and result.playoff_label == mock_game.playoff_label
        and [p.action_number for p in result.play_by_play] == sorted([p.action_number for p in mock_game_actions])
        and [s.elapsed_ms for s in result.home_team_stats.statics]
        == sorted([s.elapsed_ms for s in mock_stats if s.team_id == HOME_TEAM_ID])
        and [s.elapsed_ms for s in result.away_team_stats.statics]
        == sorted([s.elapsed_ms for s in mock_stats if s.team_id == AWAY_TEAM_ID])
        and all(
            _is_correct_player_stats(
                p,
                mock_game_player_by_player_id[p.player_id],
                [s for s in mock_stats if s.game_player_id == mock_game_player_by_player_id[p.player_id].id],
                mock_player_by_player_id[p.player_id],
            )
            for p in result.home_team_stats.players + result.away_team_stats.players
        )
    )


def test_get_game_detail_by_game_id_return_matched(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game = _create_game()
    mock_game_actions = _create_game_actions()
    mock_game_players = _create_game_players()
    mock_stats = _create_stats()
    mock_players = _create_players()
    mock_teams = _create_teams()
    mocker_patch(mocker, mock_game, mock_game_actions, mock_game_players, mock_stats, mock_players, mock_teams)
    result = get_game_detail_by_game_id(session, "game_id")

    assert _is_correct_game_detail(
        result, mock_game, mock_game_actions, mock_game_players, mock_stats, mock_players, mock_teams
    )


def test_get_game_detail_by_game_id_return_matched_even_if_no_game_actions(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game = _create_game()
    mock_game_players = _create_game_players()
    mock_stats = _create_stats()
    mock_players = _create_players()
    mock_teams = _create_teams()
    mocker_patch(mocker, mock_game, [], mock_game_players, mock_stats, mock_players, mock_teams)
    result = get_game_detail_by_game_id(session, "game_id")

    assert _is_correct_game_detail(result, mock_game, [], mock_game_players, mock_stats, mock_players, mock_teams)


def test_get_game_detail_by_game_id_return_matched_even_if_no_game_players(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game = _create_game()
    mock_game_actions = _create_game_actions()
    mock_stats = _create_stats()
    mock_players = _create_players()
    mock_teams = _create_teams()
    mocker_patch(mocker, mock_game, mock_game_actions, [], mock_stats, mock_players, mock_teams)
    result = get_game_detail_by_game_id(session, "game_id")

    assert _is_correct_game_detail(result, mock_game, mock_game_actions, [], mock_stats, mock_players, mock_teams)


def test_get_game_detail_by_game_id_return_matched_even_if_no_stats(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game = _create_game()
    mock_game_actions = _create_game_actions()
    mock_game_players = _create_game_players()
    mock_players = _create_players()
    mock_teams = _create_teams()
    mocker_patch(mocker, mock_game, mock_game_actions, mock_game_players, [], mock_players, mock_teams)
    result = get_game_detail_by_game_id(session, "game_id")

    assert _is_correct_game_detail(
        result, mock_game, mock_game_actions, mock_game_players, [], mock_players, mock_teams
    )


def test_get_game_detail_by_game_id_return_matched_even_if_no_game_players_and_players(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game = _create_game()
    mock_game_actions = _create_game_actions()
    mock_stats = _create_stats()
    mock_teams = _create_teams()
    mocker_patch(mocker, mock_game, mock_game_actions, [], mock_stats, [], mock_teams)
    result = get_game_detail_by_game_id(session, "game_id")

    assert _is_correct_game_detail(result, mock_game, mock_game_actions, [], mock_stats, [], mock_teams)


def test_get_game_detail_by_game_id_raise_exception_if_existing_game_players_but_no_players(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game = _create_game()
    mock_game_actions = _create_game_actions()
    mock_game_players = _create_game_players()
    mock_stats = _create_stats()
    mock_teams = _create_teams()
    mocker_patch(mocker, mock_game, mock_game_actions, mock_game_players, mock_stats, [], mock_teams)
    with pytest.raises(KeyError):
        get_game_detail_by_game_id(session, "game_id")


def test_get_game_detail_by_game_id_raise_exception_if_no_teams(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game = _create_game()
    mock_game_actions = _create_game_actions()
    mock_game_players = _create_game_players()
    mock_stats = _create_stats()
    mock_players = _create_players()
    mocker_patch(mocker, mock_game, mock_game_actions, mock_game_players, mock_stats, mock_players, [])
    with pytest.raises(KeyError):
        get_game_detail_by_game_id(session, "game_id")


def test_get_game_detail_by_game_id_raise_exception_if_game_not_found(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mock_game_actions = _create_game_actions()
    mock_game_players = _create_game_players()
    mock_stats = _create_stats()
    mock_players = _create_players()
    mock_teams = _create_teams()
    mocker_patch(mocker, None, mock_game_actions, mock_game_players, mock_stats, mock_players, mock_teams)
    with pytest.raises(ValueError):
        get_game_detail_by_game_id(session, "game_id")
