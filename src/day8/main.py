"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
import itertools
import logging
import math
import re
from functools import reduce
from pathlib import Path
from typing import Iterable, NamedTuple, TextIO

logging.basicConfig(level=logging.DEBUG)


def test_part1() -> None:
    """For example:"""
    example = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""  #

    assert part1(io.StringIO(example)) == 2

    example2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""  #

    assert part1(io.StringIO(example2)) == 6


"""
<end of problem description>
"""

# === Part 1 Solution: ===


class Node(NamedTuple):
    name: str
    left: str
    right: str

    @classmethod
    def from_str(cls, node_str: str) -> Node:
        m = re.match(r"(\w+) = \((\w+), (\w+)\)", node_str)
        if not m:
            raise ValueError
        return cls(*m.groups())


def parse(puzzle_input: TextIO) -> tuple[str, Iterable[Node]]:
    turns = puzzle_input.readline().strip()
    puzzle_input.readline()
    return turns, (Node.from_str(line.strip()) for line in puzzle_input)


def traverse_network(turns: str, node_map: dict[str, Node], *, start: str = "AAA") -> Iterable[str]:
    """
    Continually traverse the network according to the turn list and yield tuples
    of how many times the turns have been repeated and current node name.
    """
    current_node = start
    for turn in itertools.cycle(turns):
        current_node = node_map[current_node].left if turn == "L" else node_map[current_node].right
        yield current_node


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    turns, nodes = parse(puzzle_input)
    node_map = {n.name: n for n in nodes}

    numbered_steps = enumerate(traverse_network(turns, node_map), start=1)
    winning_step, zzz = next(itertools.dropwhile(lambda tup: tup[1] != "ZZZ", numbered_steps))

    return winning_step


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""" #

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 6


"""
<end of problem description>
"""

# === Part 2 Solution: ===

"""
The naive approach is taking more than a few seconds, so I'm going to try
something smarter. My first through is to figure out how often each parallel
ghost path lands on a "Z" node. Then, I can use those parallel loop lengths to
calculate how many steps it would take for all of them to align. A least common
multiple sort of deal.
"""


def get_ghost_loop(turns: str, moves: Iterable[str]) -> tuple[list[str], list[str]]:
    """
    Iterate this ghost path until it loops. Return the list of nodes in the loop
    preceded by any node first non-looped nodes traversed to reach that loop.
    """
    seen_nodes = set()
    one_more = True
    def havent_seen_before(node: tuple[int, str]) -> bool:
        nonlocal one_more

        if not one_more:
            return False

        if node in seen_nodes:
            if one_more:
                one_more = False
                return True
            return False
        seen_nodes.add(node)
        return True

    path_until_loops = list(
        itertools.takewhile(havent_seen_before, zip(itertools.cycle(range(1, len(turns)+1)), moves)))
    looped_to_node = path_until_loops.pop()
    loop_step = path_until_loops.index(looped_to_node)

    def unwrap(crap: list[tuple[int, str]]) -> list[str]:
        return [node for step, node in crap]

    return unwrap(path_until_loops[:loop_step]), unwrap(path_until_loops[loop_step:])


def part2(puzzle_input: TextIO) -> int:
    """<solve part 2>"""
    turns, nodes = parse(puzzle_input)
    node_map = {n.name: n for n in nodes}

    loop_lengths = []
    starting_nodes = [n for n in node_map if n.endswith("A")]
    for s in starting_nodes:
        first_ghost_path = traverse_network(turns, node_map, start=s)
        init_path, looping_path = get_ghost_loop(turns, first_ghost_path)
        logging.info("Init %d, loop %d", len(init_path), len(looping_path))
        winning_loop_steps = [i + 1 + len(init_path) for i, node in enumerate(looping_path) if node.endswith("Z")]

        # In this special case, things are way easier
        if len(winning_loop_steps) == 1:
            assert winning_loop_steps[0] == len(looping_path)
        else:
            wins = len(looping_path) // winning_loop_steps[0]
            assert winning_loop_steps == [i * winning_loop_steps[0] for i in range(1, wins + 1)]

        loop_lengths.append(winning_loop_steps[0])

    return reduce(math.lcm, loop_lengths, 1)


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
