"""
### Part 1:

--- Day 2: Cube Conundrum ---

You're launched high into the atmosphere! The apex of your trajectory just
barely reaches the surface of a large island floating in the sky. You gently
land in a fluffy pile of leaves. It's quite cold, but you don't see much snow.
An Elf runs over to greet you.

The Elf explains that you've arrived at **Snow Island** and apologizes for the
lack of snow. He'll be happy to explain the situation, but it's a bit of a walk,
so you have some time. They don't get many visitors up here; would you like to
play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red,
green, or blue. Each time you play this game, he will hide a secret number of
cubes of each color in the bag, and your goal is to figure out information about
the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach
into the bag, grab a handful of random cubes, show them to you, and then put
them back in the bag. He'll do this a few times per game.
"""

from __future__ import annotations

import io
import math
import re
from collections import Counter
from enum import Enum, auto
from pathlib import Path
from typing import Iterable, TextIO


# You play several games and record the information from each game (your puzzle
# input). Each game is listed with its ID number (like the `11` in `Game 11:
# ...`) followed by a semicolon-separated list of subsets of cubes that were
# revealed from the bag (like `3 red, 5 green, 4 blue`).
class Cube(Enum):
    blue = auto()
    red = auto()
    green = auto()

Turn = Counter[Cube]
GameId = int
Game = tuple[GameId, list[Turn]]


def test_part1() -> None:
    """For example, the record of a few games might look like this:"""
    example = """\
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""  # pycco needs this comment

    # In game 1, three sets of cubes are revealed from the bag (and then put
    # back again). The first set is 3 blue cubes and 4 red cubes; the second set
    # is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2
    # green cubes.
    games = list(parse_input(io.StringIO(example)))
    _, sets = games[0]
    assert sets[0] == Counter({Cube.blue: 3, Cube.red: 4})
    assert sets[1] == Counter({Cube.red: 1, Cube.green: 2, Cube.blue: 6})
    assert sets[2] == Counter({Cube.green: 2})

    # The Elf would first like to know which games would have been possible if
    # the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

    # In the example above, games 1, 2, and 5 would have been possible if the
    # bag had been loaded with that configuration. However, game 3 would have
    # been impossible because at one point the Elf showed you 20 red cubes at
    # once; similarly, game 4 would also have been impossible because the Elf
    # showed you 15 blue cubes at once. If you add up the IDs of the games that
    # would have been possible, you get 8.
    assert part1(io.StringIO(example)) == 8


"""
Determine which games would have been possible if the bag had been loaded with
only 12 red cubes, 13 green cubes, and 14 blue cubes. **What is the sum of the
IDs of those games?**
"""

bag_cubes = Counter({Cube.red: 12, Cube.green: 13, Cube.blue: 14})


# === Part 1 Solution: ===


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
        """Return the count of the given color."""
        if m := re.search(rf"(\d+) {color_str}", turn_str):
            return int(m.group(1))
        return 0

    return Counter({color: color_count(color.name) for color in Cube})


def turn_is_valid(turn: Turn, bag: Counter[Cube]) -> bool:
    """Return true iff the given Turn could occur with the given Bag."""
    return len(turn - bag) == 0


def part1(puzzle_input: TextIO) -> int:
    """
    Identify which games are composed of all valid turns and return the sum of
    the ID numbers of those valid games.
    """
    games = parse_input(puzzle_input)
    total = 0
    for game_id, turns in games:
        if all(turn_is_valid(t, bag_cubes) for t in turns):
            total += game_id
    return total


"""
### Part 2:

--- Part Two ---

The Elf says they've stopped producing snow because they aren't getting any
**water**! He isn't sure why the water stopped; however, he can show you how to
get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you
played, what is the **fewest number of cubes of each color** that could have
been in the bag to make the game possible?
"""


def test_part2() -> None:
    """Again consider the example games from earlier:"""
    example = """\
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""  # pycco needs this comment

    games = parse_input(io.StringIO(example))
    game_iter = iter(games)

    # - In game 1, the game could have been played with as few as 4 red, 2
    #   green, and 6 blue cubes. If any color had even one fewer cube, the game
    #   would have been impossible.
    assert get_min_bag(next(game_iter)[1]) == Counter({Cube.red: 4, Cube.green: 2, Cube.blue: 6})

    # - Game 2 could have been played with a minimum of 1 red, 3 green, and 4
    #   blue cubes.
    assert get_min_bag(next(game_iter)[1]) == Counter({Cube.red: 1, Cube.green: 3, Cube.blue: 4})

    # - Game 3 must have been played with at least 20 red, 13 green, and 6 blue
    #   cubes.
    assert get_min_bag(next(game_iter)[1]) == Counter({Cube.red: 20, Cube.green: 13, Cube.blue: 6})

    # - Game 4 required at least 14 red, 3 green, and 15 blue cubes.
    assert get_min_bag(next(game_iter)[1]) == Counter({Cube.red: 14, Cube.green: 3, Cube.blue: 15})

    # - Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
    assert get_min_bag(next(game_iter)[1]) == Counter({Cube.red: 6, Cube.green: 3, Cube.blue: 2})

    # The **power** of a set of cubes is equal to the numbers of red, green, and
    # blue cubes multiplied together. The power of the minimum set of cubes in
    # game 1 is `48`. In games 2-5 it was `12`, `1560`, `630`, and `36`,
    # respectively. Adding up these five powers produces the sum **`2286`**.
    assert part2(io.StringIO(example)) == 2286


"""
For each game, find the minimum set of cubes that must have been present. **What
is the sum of the power of these sets?**
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
    return math.prod(bag.get(color, 0) for color in Cube)


def part2(puzzle_input: TextIO) -> int:
    """
    Determine the minimum valid bag for each game and sum up the product of the
    counts of each cube type.
    """
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
