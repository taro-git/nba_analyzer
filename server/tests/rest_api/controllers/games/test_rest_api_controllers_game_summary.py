from datetime import datetime, timezone

import pytest
from pytest_mock import MockerFixture
from sqlmodel import Session

from common.models.games.games import Game
from common.models.teams.teams import TeamProperty
from common.types import Conference, Division, GameCategory, GameStatus
from rest_api.controllers.games.game_summary import get_game_summaries_by_start_datetime
from rest_api.schemas.games.game_summaries import (
    GameCategory as GameCategorySchema,
)
from rest_api.schemas.games.game_summaries import (
    GameStatus as GameStatusSchema,
)
from rest_api.schemas.games.game_summaries import (
    GameSummarySchema,
)
from rest_api.schemas.teams.regular_season import Team


def mocker_patch(mocker: MockerFixture, mock_games: list[Game], mock_team: list[TeamProperty]) -> None:
    mocker.patch(
        "rest_api.controllers.games.game_summary.get_games_by_start_datetime",
        return_value=mock_games,
    )

    mocker.patch(
        "rest_api.controllers.games.game_summary.get_team_properties_by_ids",
        return_value=mock_team,
    )


def _create_games(season: int) -> list[Game]:
    game_dates = [datetime(season, 1, 1 + i, tzinfo=timezone.utc) for i in range(5)]
    return [
        Game(
            game_id=f"002{season % 100:02d}{i:05d}",
            season=season,
            start_epoc_sec=int(game_date.timestamp()),
            elapsed_sec=0,
            status=GameStatus.scheduled,
            category=GameCategory.regular_season,
            home_team_id=1,
            away_team_id=2,
            home_score=0,
            away_score=0,
            playoff_label=None,
        )
        for i, game_date in enumerate(game_dates)
    ]


def _create_teams(season: int) -> list[TeamProperty]:
    return [
        TeamProperty(
            team_id=1,
            season=season,
            team_name="Team A",
            team_tricode="AAA",
            team_city="City A",
            conference=Conference.east,
            division=Division.atlantic,
        ),
        TeamProperty(
            team_id=2,
            season=season,
            team_name="Team B",
            team_tricode="BBB",
            team_city="City B",
            conference=Conference.east,
            division=Division.central,
        ),
    ]


@pytest.fixture
def mock_success_case(mocker: MockerFixture) -> list[GameSummarySchema]:
    mock_games = _create_games(2023)
    mock_teams = _create_teams(2023)
    mocker_patch(mocker, mock_games, mock_teams)
    team_map = {t.team_id: t for t in mock_teams}
    return [
        GameSummarySchema(
            game_id=game.game_id,
            status=GameStatusSchema(game.status.value),
            category=GameCategorySchema(game.category.value),
            start_datetime=datetime.fromtimestamp(game.start_epoc_sec, tz=timezone.utc),
            elapsed_sec=game.elapsed_sec,
            home_team=Team(
                team_id=game.home_team_id,
                team_name=team_map.get(game.home_team_id, Team).team_name,
                team_tricode=team_map.get(game.home_team_id, Team).team_tricode,
                team_logo=f"https://cdn.nba.com/logos/nba/{game.home_team_id}/global/L/logo.svg",
            ),
            away_team=Team(
                team_id=game.away_team_id,
                team_name=team_map.get(game.away_team_id, Team).team_name,
                team_tricode=team_map.get(game.away_team_id, Team).team_tricode,
                team_logo=f"https://cdn.nba.com/logos/nba/{game.away_team_id}/global/L/logo.svg",
            ),
            home_team_score=game.home_score,
            away_team_score=game.away_score,
            playoff_label=game.playoff_label,
        )
        for game in mock_games
    ]


def test_get_game_summaries_by_start_datetime_return_matched(
    session: Session,
    mock_success_case: list[GameSummarySchema],
) -> None:
    from_datetime = datetime(2023, 1, 1, tzinfo=timezone.utc)
    to_datetime = datetime(2023, 1, 5, tzinfo=timezone.utc)

    result_ids = [g.game_id for g in get_game_summaries_by_start_datetime(session, from_datetime, to_datetime)]
    expected_ids = [
        g.game_id for g in mock_success_case if g.start_datetime >= from_datetime and g.start_datetime <= to_datetime
    ]

    assert sorted(result_ids) == sorted(expected_ids)


def test_get_game_summaries_by_start_datetime_return_empty_if_no_matched(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mocker_patch(mocker, [], _create_teams(2023))

    from_datetime = datetime(2023, 1, 1, tzinfo=timezone.utc)
    to_datetime = datetime(2023, 1, 5, tzinfo=timezone.utc)

    result_ids = [g.game_id for g in get_game_summaries_by_start_datetime(session, from_datetime, to_datetime)]
    assert result_ids == []


def test_get_game_summaries_by_start_datetime_error_if_missing_team(
    session: Session,
    mocker: MockerFixture,
) -> None:
    mocker_patch(mocker, _create_games(2023), [])

    from_datetime = datetime(2023, 1, 1, tzinfo=timezone.utc)
    to_datetime = datetime(2023, 1, 5, tzinfo=timezone.utc)

    with pytest.raises(KeyError):
        get_game_summaries_by_start_datetime(session, from_datetime, to_datetime)
