import pytest

from common.types import Conference, Division, GameCategory, GameStatus


@pytest.mark.parametrize(
    "value, expected",
    [
        ("East", Conference.east),
        ("east", Conference.east),
        ("E", Conference.east),
        ("Eastern Conference", Conference.east),
        ("West", Conference.west),
        ("west", Conference.west),
        ("W", Conference.west),
        ("Western Conference", Conference.west),
    ],
)
def test_conference_from_str_success(value: str, expected: Conference) -> None:
    assert Conference.from_str(value) is expected


@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        "North",
        "South",
        "abc",
        "1",
    ],
)
def test_conference_from_str_invalid(invalid_value: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        Conference.from_str(invalid_value)

    assert "Invalid conference_str" in str(exc_info.value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("atlantic", Division.atlantic),
        ("Atlantic", Division.atlantic),
        ("A", Division.atlantic),
        ("Atlantic Division", Division.atlantic),
        ("central", Division.central),
        ("Central", Division.central),
        ("C", Division.central),
        ("Central Division", Division.central),
        ("southeast", Division.southeast),
        ("Southeast", Division.southeast),
        ("SE", Division.southeast),
        ("Southeast Division", Division.southeast),
        ("northwest", Division.northwest),
        ("Northwest", Division.northwest),
        ("N", Division.northwest),
        ("Northwest Division", Division.northwest),
        ("pacific", Division.pacific),
        ("Pacific", Division.pacific),
        ("P", Division.pacific),
        ("Pacific Division", Division.pacific),
        ("southwest", Division.southwest),
        ("Southwest", Division.southwest),
        ("SW", Division.southwest),
        ("Southwest Division", Division.southwest),
        ("midwest", Division.midwest),
        ("MouthWest", Division.midwest),
        ("MW", Division.midwest),
        ("Midwest Division", Division.midwest),
    ],
)
def test_division_from_str_success(value: str, expected: Division) -> None:
    assert Division.from_str(value) is expected


@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        "division",
        "S",
        "hogehoge",
        "1",
    ],
)
def test_division_from_str_invalid(invalid_value: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        Division.from_str(invalid_value)

    assert "Invalid division_str" in str(exc_info.value)


@pytest.mark.parametrize(
    "value, expected",
    [
        ("0012500001", GameCategory.preseason),
        ("0092500009", GameCategory.preseason),
        ("0022500002", GameCategory.regular_season),
        ("0032500003", GameCategory.all_star),
        ("0042500004", GameCategory.playoffs),
        ("0052500005", GameCategory.playin_tournament),
        ("0062500006", GameCategory.nba_cup),
    ],
)
def test_game_category_from_game_id_success(value: str, expected: GameCategory) -> None:
    assert GameCategory.from_game_id(value) is expected


@pytest.mark.parametrize(
    "invalid_value",
    [
        "0072500007",
        "0082500008",
        "",
        "invalid",
        "00",
    ],
)
def test_game_category_from_game_id_invalid(invalid_value: str) -> None:
    with pytest.raises(ValueError) as exc_info:
        GameCategory.from_game_id(invalid_value)

    assert "Invalid game_id" in str(exc_info.value)


@pytest.mark.parametrize(
    "value, expected",
    [
        (1, GameStatus.scheduled),
        (2, GameStatus.live),
        (3, GameStatus.final),
    ],
)
def test_game_status_from_status_id_success(value: int, expected: GameStatus) -> None:
    assert GameStatus.from_status_id(value) is expected


@pytest.mark.parametrize(
    "invalid_value",
    [
        0,
        4,
    ],
)
def test_game_category_from_status_id_invalid(invalid_value: int) -> None:
    with pytest.raises(ValueError) as exc_info:
        GameStatus.from_status_id(invalid_value)

    assert "Invalid status_id" in str(exc_info.value)
