"""
### Part 1:

<paste in problem description here>
"""

from __future__ import annotations

import io
import logging
import operator
import re
from collections import Counter
from enum import Enum, auto
from functools import reduce
from pathlib import Path
from typing import Iterable, TextIO


def test_part1() -> None:
    """For example:"""
    example = """
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""  # pycco needs this comment

    games = parse_input(io.StringIO(example))
    logging.debug(list(games))

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == 8


"""
<end of problem description>
"""

# === Part 1 Solution: ===

class Cube(Enum):
    blue = auto()
    red = auto()
    green = auto()

Turn = Counter[Cube]
GameId = int
Game = tuple[GameId, list[Turn]]

bag_cubes = Counter({Cube.red: 12, Cube.green: 13, Cube.blue: 14})


def parse_input(puzzle_input: TextIO) -> Iterable[Game]:
    """Turn a text description of a set of games into Game objects."""
    for line in puzzle_input:
        if m := re.search(r"Game (\d+): (.*)", line):
            game_id, turns = m.groups()
            turns = [parse_turn(turn) for turn in turns.split("; ")]
            yield int(game_id), turns


def parse_turn(turn_str: str) -> Turn:
    """Turn a text description of a turn into a Turn object."""
    def color_count(color_str: str) -> int:
        if m := re.search(rf"(\d+) {color_str}", turn_str):
            return int(m.group(1))
        return 0

    return Counter({color: color_count(color.name) for color in Cube})


def turn_is_valid(turn: Turn, bag: Counter[Cube]) -> bool:
    """Return true iff the given Turn could occur with the given Bag."""
    return len(turn - bag) == 0


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    games = parse_input(puzzle_input)
    total = 0
    for game_id, turns in games:
        if all(turn_is_valid(t, bag_cubes) for t in turns):
            total += game_id
    return total


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""  # pycco needs this comment

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 2286


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def get_min_bag(turns: list[Turn]) -> Counter[Cube]:
    """Get the minimum bag of cubes for which the given turns would be valid."""
    bag: Counter[Cube] = Counter()
    for turn in turns:
        bag |= turn
    return bag


def cubes_power(bag: Counter[Cube]) -> int:
    """Return the power of a set of cubes."""
    return reduce(operator.mul, (bag.get(color, 0) for color in Cube))


def part2(puzzle_input: TextIO) -> int:
    """<solve part 2>"""
    games = parse_input(puzzle_input)
    total = 0
    for _, turns in games:
        min_bag = get_min_bag(turns)
        total += cubes_power(min_bag)
    return total


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
