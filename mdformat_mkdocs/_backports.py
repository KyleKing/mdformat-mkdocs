"""Backport of Python 3.11 StrEnum.

From: https://github.com/clbarnes/backports.strenum/blame/fd9a25dacd7161c172e07e4bd673916f85db2cb5/src/backports/strenum/strenum.py

"""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """Enum where members are also (and must be) strings"""

    def __new__(cls, *values: str) -> 'StrEnum':
        if len(values) > 3:  # noqa: PLR2004
            raise TypeError(
                "too many arguments for str(): %r" % (values,),  # noqa: UP031
            )
        if len(values) == 1:
            # it must be a string
            if not isinstance(values[0], str):
                raise TypeError("%r is not a string" % (values[0],))  # noqa: UP031
        elif len(values) >= 2:  # noqa: PLR2004
            # check that encoding argument is a string
            if not isinstance(values[1], str):
                raise TypeError(
                    "encoding must be a string, not %r" % (values[1],),  # noqa: UP031
                )
        # check that errors argument is a string
        elif len(values) == 3 and not isinstance(values[2], str):  # noqa: PLR2004
            raise TypeError(
                "errors must be a string, not %r" % (values[2]),
            )

        value = str(*values)
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    __str__ = str.__str__

    @staticmethod
    def _generate_next_value_(
        name: str,
        start: int,  # noqa: ARG004
        count: int,  # noqa: ARG004
        last_values: list[str],  # noqa: ARG004
    ) -> str:
        """Return the lower-cased version of the member name."""
        return name.lower()
