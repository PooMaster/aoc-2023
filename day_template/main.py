"""
### Part 1:

<paste in problem description here>
"""

import io
from typing import TextIO


def test_part1() -> None:
    """For example:"""
    # > `""` results in  `...`.
    assert part1(io.StringIO("")) == ...


"""
<end of problem description>
"""

# === Part 1 Solution: ===


def part1(input: TextIO) -> ...:
    """ """
    return ...


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    # > `""` results in  `...`.
    assert part2(io.StringIO("")) == ...


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def part2(input: TextIO) -> ...:
    """ """
    return ...


if __name__ == "__main__":
    # Print out part 1 solution
    with open("input.txt") as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with open("input.txt") as puzzle_input:
        print("Part 2:", part2(puzzle_input))
