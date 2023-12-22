"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
import sys
from bisect import bisect_left
from itertools import combinations
from pathlib import Path
from typing import Iterable, TextIO

sys.path.append("..")
from utils import Pos, pos_extent  # noqa: E402


def test_part1() -> None:
    """For example:"""
    example = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""" #

    galaxies = list(parse(io.StringIO(example)))

    expanded_galaxies = list(expand_space(galaxies))
    assert set(expanded_galaxies) == set(parse(io.StringIO("""\
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
"""))) #

    assert path_length(expanded_galaxies[4], expanded_galaxies[8]) == 9

    assert path_length(expanded_galaxies[0], expanded_galaxies[6]) == 15
    assert path_length(expanded_galaxies[2], expanded_galaxies[5]) == 17
    assert path_length(expanded_galaxies[7], expanded_galaxies[8]) == 5

    assert part1(io.StringIO(example)) == 374


"""
<end of problem description>
"""

# === Part 1 Solution: ===


def parse(puzzle_input: TextIO) -> Iterable[Pos]:
    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line.strip()):
            if char == "#":
                yield Pos(x, y)


def unparse(galaxies: Iterable[Pos], file: io.TextIOWrapper | None = None) -> None:
    galaxies = set(galaxies)
    x_range, y_range = pos_extent(galaxies)
    for y in y_range:
        for x in x_range:
            print("#" if Pos(x, y) in galaxies else ".", end="", file=file)
        print(file=file)


def expand_space(galaxies: Iterable[Pos], factor: int = 2) -> Iterable[Pos]:
    galaxy_set = set(galaxies)
    x_range, y_range = pos_extent(galaxies)

    # Find empty columns
    galaxy_xs = {pos.x for pos in galaxy_set}
    empty_xs = [x for x in x_range if x not in galaxy_xs]

    # Find empty rows
    galaxy_ys = {pos.y for pos in galaxy_set}
    empty_ys = [y for y in y_range if y not in galaxy_ys]

    for pos in galaxies:
        expanded_x = pos.x + bisect_left(empty_xs, pos.x) * (factor - 1)
        expanded_y = pos.y + bisect_left(empty_ys, pos.y) * (factor - 1)
        yield Pos(expanded_x, expanded_y)


def path_length(pos1: Pos, pos2: Pos) -> int:
    return abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y)


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    galaxies = parse(puzzle_input)
    expanded_galaxies = expand_space(set(galaxies))

    return sum(path_length(a, b) for a, b in combinations(expanded_galaxies, 2))


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""" #

    assert part2(io.StringIO(example), factor=10) == 1030
    assert part2(io.StringIO(example), factor=100) == 8410


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def part2(puzzle_input: TextIO, factor: int = 1_000_000) -> int:
    """<solve part 2>"""
    galaxies = parse(puzzle_input)
    expanded_galaxies = expand_space(set(galaxies), factor=factor)

    return sum(path_length(a, b) for a, b in combinations(expanded_galaxies, 2))


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
