"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
import math
from pathlib import Path
from typing import NamedTuple, TextIO


def test_part1() -> None:
    """For example:"""
    example = """\
Time:      7  15   30
Distance:  9  40  200"""  #

    races = parse_races(io.StringIO(example))
    assert winning_range(races[0]) == range(2, 6)
    assert winning_range(races[1]) == range(4, 12)
    assert races[2] == (30, 200)
    assert winning_range(races[2]) == range(11, 20)

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == 288


"""
<end of problem description>
"""

# === Part 1 Solution: ===


class Race(NamedTuple):
    time: int
    distance: int


def parse_races(puzzle_input: TextIO) -> list[Race]:
    times = map(int, next(puzzle_input).removeprefix("Time:").strip().split())
    distances = map(int, next(puzzle_input).removeprefix("Distance:").strip().split())

    return [Race(t, d) for t, d in zip(times, distances)]


def winning_range(race: Race) -> range:
    determinant = race.time ** 2 - 4 * race.distance
    if determinant < 0:
        return range(0)

    high_tie = (-race.time - math.sqrt(determinant)) / -2
    low_tie = (-race.time + math.sqrt(determinant)) / -2

    high_win = int(high_tie) - 1 if high_tie.is_integer() else math.floor(high_tie)
    low_win = int(low_tie) + 1 if low_tie.is_integer() else math.ceil(low_tie)

    return range(low_win, high_win + 1)


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    races = parse_races(puzzle_input)
    race_ways_to_win = (len(winning_range(r)) for r in races)
    return math.prod(race_ways_to_win)


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
Time:      7  15   30
Distance:  9  40  200"""  #

    race = parse_races_keming(io.StringIO(example))
    assert race == (71530, 940200)
    assert winning_range(race) == range(14, 71517)

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 71503


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def parse_races_keming(puzzle_input: TextIO) -> Race:
    time = int(next(puzzle_input).removeprefix("Time:").strip().replace(" ", ""))
    distance = int(next(puzzle_input).removeprefix("Distance:").strip().replace(" ", ""))

    return Race(time, distance)


def part2(puzzle_input: TextIO) -> int:
    """<solve part 2>"""
    race = parse_races_keming(puzzle_input)
    return len(winning_range(race))


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
