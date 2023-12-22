"""
Code that I want to use for multiple days, but don't want to get that's day's
source all messy by copy and pasting it.
"""  # noqa: INP001

from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, NamedTuple, TypeVar


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self: Pos, other: Pos) -> Pos:  # type: ignore[override]
        return Pos(self.x + other.x, self.y + other.y)


if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison
    T = TypeVar("T", bound=SupportsRichComparison)

def extent(iterable: Iterable[T]) -> tuple[T, T]:
    it = iter(iterable)

    try:
        first_item = next(it)
    except StopIteration:
        raise ValueError from None

    min_extent = first_item
    max_extent = first_item

    for i in it:
        min_extent = min(min_extent, i)
        max_extent = max(max_extent, i)

    return min_extent, max_extent


def pos_extent(positions: Iterable[Pos]) -> tuple[range, range]:
    positions = list(positions)

    x_min, x_max = extent(pos.x for pos in positions)
    y_min, y_max = extent(pos.y for pos in positions)

    return range(x_min, x_max + 1), range(y_min, y_max + 1)
