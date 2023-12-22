"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
import logging
from functools import reduce
from itertools import pairwise, starmap
from pathlib import Path
from typing import Iterable, TextIO


def test_part1() -> None:
    """For example:"""
    example = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""" #

    sequences = iter(parse(io.StringIO(example)))
    assert next(sequences) == [0, 3, 6, 9, 12, 15]
    assert next(sequences) == [1, 3, 6, 10, 15, 21]
    assert next(sequences) == [10, 13, 16, 21, 30, 45]

    assert diff_sequence([0, 3, 6, 9, 12, 15]) == [3, 3, 3, 3, 3]

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == 114


"""
<end of problem description>
"""

# === Part 1 Solution: ===


def parse(puzzle_input: TextIO) -> Iterable[list[int]]:
    for line in puzzle_input:
        yield [int(i) for i in line.strip().split()]


def diff_sequence(sequence: list[int]) -> list[int]:
    return list(starmap(lambda a,b: b - a, pairwise(sequence)))


def diff_sequences(sequence: list[int]) -> Iterable[list[int]]:
    while True:
        yield sequence
        if all(i == 0 for i in sequence):
            break
        sequence = diff_sequence(sequence)


def predicted_next_value(sequence: list[int]) -> int:
    return sum(seq[-1] for seq in diff_sequences(sequence))


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    sequences = parse(puzzle_input)

    return sum(map(predicted_next_value, sequences))


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""" #

    assert predicted_prev_value([10, 13, 16, 21, 30, 45]) == 5
    assert predicted_prev_value([0, 3, 6, 9, 12, 15]) == -3
    logging.debug(diff_sequence([1, 3, 6, 10, 15, 21]))
    assert predicted_prev_value([1, 3, 6, 10, 15, 21]) == 0


    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 2


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def predicted_prev_value(sequence: list[int]) -> int:
    firsts = [seq[0] for seq in diff_sequences(sequence)]
    return reduce(lambda a,b: b - a, reversed(firsts), 0)


def part2(puzzle_input: TextIO) -> int:
    """<solve part 2>"""
    sequences = parse(puzzle_input)

    return sum(map(predicted_prev_value, sequences))


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
