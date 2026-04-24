import re

from common.settings import NBA_ORVERTIME_SECONDS, NBA_PERIOD_SECONDS


def convert_from_clock_str_to_seconds(str: str) -> int:
    """
    MMM:SSS 形式の文字列を秒に変換します.
    """
    if str == "" or str == "DNP" or str == "0":
        return 0
    minutes_str, seconds_str = str.split(":")
    minutes = int(minutes_str)
    seconds = int(seconds_str)
    return minutes * 60 + seconds


def convert_from_playtime_str_to_ms(str: str) -> int:
    """
    PTxxMxx.xx 形式の文字列をミリ秒に変換します.
    """
    match = re.match(r"PT(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?", str)
    if not match:
        raise ValueError(f"invalid clock {str}")
    minutes = int(match.group(1)) if match.group(1) else 0
    seconds = float(match.group(2)) if match.group(2) else 0.0
    return int((minutes * 60 + seconds) * 1000)


def create_elapsed_ms_from_clock_and_period(clock: str, period: int) -> int:
    """
    PTxxMxx.xx 形式のゲームクロックとピリオドを指定して、試合の経過時間（ミリ秒）を返します.
    """
    if period <= 4:
        return int(period * NBA_PERIOD_SECONDS * 1000 - convert_from_playtime_str_to_ms(clock))
    return int(
        (4 * NBA_PERIOD_SECONDS + (period - 4) * NBA_ORVERTIME_SECONDS) * 1000 - convert_from_playtime_str_to_ms(clock)
    )
