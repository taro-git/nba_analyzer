import re
from typing import Type

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema


class Season(str):
    """
    パラメータや戻り値に使用するシーズンの型を示します.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        _source: Type[object],
        _handler: GetCoreSchemaHandler,
    ) -> core_schema.AfterValidatorFunctionSchema:
        return core_schema.no_info_after_validator_function(
            cls.validate,
            core_schema.str_schema(),
        )

    @classmethod
    def validate(cls, season: str) -> str:
        match = re.fullmatch(r"(\d{4})-(\d{2})", season)
        if not match:
            raise ValueError("season must be YYYY-YY format and >= 1970-71")

        year_str, suffix = match.groups()
        year = int(year_str)
        expected_suffix = f"{(year + 1) % 100:02d}"

        if year < 1970 or suffix != expected_suffix:
            raise ValueError("season must be YYYY-YY format and >= 1970-71")
        return season
