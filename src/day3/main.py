"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
import logging
import operator
import re
from functools import reduce
from itertools import chain, product
from pathlib import Path
from typing import Iterable, NamedTuple, TextIO


def test_part1() -> None:
    """For example:"""
    small_example = """\
467.
...*
..35
"""  # pycco needs this

    schematic = parse_schematic(io.StringIO(small_example))
    logging.debug(schematic)

    example = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""  # pycco needs this

    schematic = parse_schematic(io.StringIO(example))
    logging.debug(schematic)

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == 4361


"""
<end of problem description>
"""

# === Part 1 Solution: ===


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self: Pos, other: Pos) -> Pos:
        return Pos(self.x + other.x, self.y + other.y)


class Label(NamedTuple):
    number: int
    pos: set[Pos]


class Symbol(NamedTuple):
    character: str
    pos: Pos


def parse_schematic(puzzle_input: TextIO) -> tuple[list[Label], list[Symbol]]:
    labels: list[Label] = []
    symbols: list[Symbol] = []

    for line_number, line in enumerate(puzzle_input):
        # Find all labels
        for label_match in re.finditer(r"\d+", line):
            labels.append(Label(  # noqa: PERF401
                number=int(label_match.group()),
                pos={Pos(loc, line_number) for loc in range(label_match.start(), label_match.end())}
            ))

        # Find all symbols
        for symbol_match in re.finditer(r"[^\s\.\d]", line):
            symbols.append(Symbol(  # noqa: PERF401
                character=symbol_match.group(),
                pos=Pos(symbol_match.start(), line_number)
            ))

    return labels, symbols


adjacents = [
    Pos(x, y) for x, y in product([-1, 0, 1], repeat=2)
    if (x, y) != (0, 0)
]

def pos_adjacencies(pos: Pos) -> Iterable[Pos]:
    yield from (pos + adj for adj in adjacents)


def part1(puzzle_input: TextIO) -> ...:
    """<solve part 1>"""
    labels, symbols = parse_schematic(puzzle_input)

    symbol_adjacencies = set(chain.from_iterable(pos_adjacencies(sym.pos) for sym in symbols))
    matched_labels = [label for label in labels if label.pos & symbol_adjacencies]

    return sum(label.number for label in matched_labels)


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""  # pycco needs this

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 467835


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def part2(puzzle_input: TextIO) -> ...:
    """<solve part 2>"""
    labels, symbols = parse_schematic(puzzle_input)

    gears = (sym for sym in symbols if sym.character == "*")

    gear_ratios = 0

    for gear in gears:
        gear_adjacents = set(pos_adjacencies(gear.pos))
        gear_labels = [label for label in labels if label.pos & gear_adjacents]
        if len(gear_labels) != 2:
            continue
        gear_ratios += reduce(operator.mul, (label.number for label in gear_labels))

    return gear_ratios


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
