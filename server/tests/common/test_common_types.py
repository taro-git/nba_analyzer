import pytest

from common.types import Conference, Division


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
