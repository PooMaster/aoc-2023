"""
### Part 1:

<paste in problem description here>
"""

import io
from pathlib import Path
from typing import TextIO


def test_part1() -> None:
    """For example:"""
    example = """\
""" #

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == ...


"""
<end of problem description>
"""

# === Part 1 Solution: ===


def part1(puzzle_input: TextIO) -> ...:
    """<solve part 1>"""
    return puzzle_input


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
""" #

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == ...


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def part2(puzzle_input: TextIO) -> ...:
    """<solve part 2>"""
    return puzzle_input


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
