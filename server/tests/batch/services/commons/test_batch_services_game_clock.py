import pytest

from batch.services.commons.game_clock import (
    convert_from_clock_str_to_seconds,
    convert_from_playtime_str_to_ms,
    create_elapsed_ms_from_clock_and_period,
)
from common.settings import NBA_ORVERTIME_SECONDS, NBA_PERIOD_SECONDS

# --- convert_from_clock_str_to_seconds ---


@pytest.mark.parametrize(
    "clock_str, expected",
    [
        ("000:00", 0),
        ("", 0),
        ("DNP", 0),
        ("0", 0),
        ("001:00", 60),
        ("012:00", 720),
        ("000:30", 30),
        ("010:30", 630),
    ],
)
def test_convert_from_clock_str_to_seconds(clock_str: str, expected: int) -> None:
    assert convert_from_clock_str_to_seconds(clock_str) == expected


# --- convert_from_playtime_str_to_ms ---


@pytest.mark.parametrize(
    "playtime_str, expected_ms",
    [
        ("PT00M00.00S", 0),
        ("PT01M00.00S", 60_000),
        ("PT12M00.00S", 720_000),
        ("PT00M30.00S", 30_000),
        ("PT10M30.50S", (10 * 60 + 30.5) * 1000),
        ("PT00M00.00S", 0),
        ("PT48M00.00S", 48 * 60 * 1000),
    ],
)
def test_convert_from_playtime_str_to_ms(playtime_str: str, expected_ms: float) -> None:
    assert convert_from_playtime_str_to_ms(playtime_str) == int(expected_ms)


def test_convert_from_playtime_str_to_ms_error_on_invalid_format() -> None:
    with pytest.raises(ValueError):
        convert_from_playtime_str_to_ms("invalid")


# --- create_elapsed_ms_from_clock_and_period ---


@pytest.mark.parametrize(
    "clock, period, expected_ms",
    [
        # ピリオド開始直後（残り12分）
        ("PT12M00.00S", 1, 0),
        # ピリオド終了直前（残り0秒）
        ("PT00M00.00S", 1, NBA_PERIOD_SECONDS * 1000),
        # 第2ピリオド開始直後
        ("PT12M00.00S", 2, NBA_PERIOD_SECONDS * 1000),
        # 第4ピリオド終了
        ("PT00M00.00S", 4, 4 * NBA_PERIOD_SECONDS * 1000),
        # 延長第1ピリオド開始直後（残り5分）
        ("PT05M00.00S", 5, 4 * NBA_PERIOD_SECONDS * 1000),
        # 延長第1ピリオド終了
        ("PT00M00.00S", 5, (4 * NBA_PERIOD_SECONDS + NBA_ORVERTIME_SECONDS) * 1000),
        # 延長第2ピリオド終了
        ("PT00M00.00S", 6, (4 * NBA_PERIOD_SECONDS + 2 * NBA_ORVERTIME_SECONDS) * 1000),
    ],
)
def test_create_elapsed_ms_from_clock_and_period(clock: str, period: int, expected_ms: int) -> None:
    assert create_elapsed_ms_from_clock_and_period(clock, period) == expected_ms
