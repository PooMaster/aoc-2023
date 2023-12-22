"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, NamedTuple, TextIO, TypeVar

if TYPE_CHECKING:
    from _typeshed import SupportsRichComparison


def test_part1() -> None:
    """For example:"""
    example = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF
""" #

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == 4


"""
<end of problem description>
"""

# === Part 1 Solution: ===


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self: Pos, other: Pos) -> Pos:  # type: ignore[override]
        return Pos(self.x + other.x, self.y + other.y)


class Dir(Enum):
    up = Pos(0, -1)
    down = Pos(0, 1)
    left = Pos(-1, 0)
    right = Pos(1, 0)

    def opposite(self) -> Dir:
        match self:
            case Dir.up:
                return Dir.down
            case Dir.down:
                return Dir.up
            case Dir.left:
                return Dir.right
            case Dir.right:
                return Dir.left


# This will be used to very simply iterate through the pipe links
class Step(NamedTuple):
    pos: Pos
    move_dir: Dir


class Pipe(Enum):
    up_down = "|"
    left_right = "-"
    up_right = "L"
    up_left = "J"
    down_left = "7"
    down_right = "F"


class Grid(NamedTuple):
    start: Pos
    pipe_map: dict[Pos, Pipe]
    pipe_steps: dict[Step, Step]


def parse(puzzle_input: TextIO) -> Grid:
    start = None
    pipe_map = {}
    pipe_steps = {}

    def add_steps(my_pos: Pos, dir1: Dir, dir2: Dir) -> None:
        """
        Update pipe_steps with appropriate entries for this pipe. Each pipe has
        a position and two entrance/exits.
        """
        nonlocal pipe_steps
        pipe_steps[Step(my_pos + dir1.value, dir1.opposite())] = Step(my_pos, dir2)
        pipe_steps[Step(my_pos + dir2.value, dir2.opposite())] = Step(my_pos, dir1)

    for y, line in enumerate(puzzle_input):
        for x, char in enumerate(line.rstrip()):
            # Ignore empty ground
            if char == ".":
                continue

            # Something is here
            pos = Pos(x, y)

            # Save starting position
            if char == "S":
                start = pos
                continue

            # Build up the pipe step network
            pipe = Pipe(char)
            pipe_map[pos] = pipe
            match pipe:
                case Pipe.up_down:
                    add_steps(pos, Dir.up, Dir.down)
                case Pipe.left_right:
                    add_steps(pos, Dir.left, Dir.right)
                case Pipe.up_right:
                    add_steps(pos, Dir.up, Dir.right)
                case Pipe.up_left:
                    add_steps(pos, Dir.up, Dir.left)
                case Pipe.down_right:
                    add_steps(pos, Dir.down, Dir.right)
                case Pipe.down_left:
                    add_steps(pos, Dir.down, Dir.left)


    assert start is not None
    return Grid(start, pipe_map, pipe_steps)


def iterate_loop(start_pos: Pos, start_dir: Dir, pipe_steps: dict[Step, Step]) -> Iterable[Step]:
    next_step = Step(start_pos, start_dir)

    while True:
        yield next_step
        if (next_step.pos + next_step.move_dir.value) == start_pos:
            break
        next_step = pipe_steps[next_step]


def find_loop(grid: Grid) -> list[Step]:
    # Find a direction from starting position to start the loop from
    start_dir = next(d for d in Dir if Step(grid.start, d) in grid.pipe_steps)
    return list(iterate_loop(grid.start, start_dir, grid.pipe_steps))


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    grid = parse(puzzle_input)

    loop_steps = find_loop(grid)

    return len(loop_steps) // 2


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""" #

    assert part2(io.StringIO(example)) == 4

    example2 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
""" #

    assert part2(io.StringIO(example2)) == 8

    example2 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""" #

    assert part2(io.StringIO(example2)) == 10


"""
<end of problem description>
"""

# === Part 2 Solution: ===


if TYPE_CHECKING:
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


def get_plug_pipe(dir1: Dir, dir2: Dir) -> Pipe:
    dirs = {dir1, dir2}

    if dirs == {Dir.up, Dir.down}:
        return Pipe.up_down

    if dirs == {Dir.left, Dir.right}:
        return Pipe.left_right

    if dirs == {Dir.up, Dir.right}:
        return Pipe.up_right

    if dirs == {Dir.up, Dir.left}:
        return Pipe.up_left

    if dirs == {Dir.down, Dir.left}:
        return Pipe.down_left

    if dirs == {Dir.down, Dir.right}:
        return Pipe.down_right

    raise ValueError


def plug_hole(loop_steps: list[Step], grid: Grid) -> dict[Pos, Pipe]:
    first_step, last_step = loop_steps[0], loop_steps[-1]

    plugged_map = grid.pipe_map.copy()
    plugged_map[grid.start] = get_plug_pipe(first_step.move_dir, last_step.move_dir.opposite())
    return plugged_map


def loop_area(loop: list[Step], pipe_map: dict[Pos, Pipe]) -> int:
    # Really wish there was a closed form solution like using the calculus
    # polygon area algo. Maybe scan the lines with only the loop and count
    # toggle from out to in when hitting a boundary? -- but there are tricky
    # cases like: ".|L-7.F-J|."  (all outside)

    # We are rasterizing!
    area = 0

    # First, find the extent of our loop
    x_min, x_max = extent(step.pos.x for step in loop)
    y_min, y_max = extent(step.pos.y for step in loop)

    # Make a set of all positions that contain loop pipes to allow for quick
    # loop pipe or empty check.
    loop_positions = {step.pos for step in loop}

    in_loop: bool = False  # True if raster has passed inside of the loop
    section_head: Pipe | None = None  # The type of pipe at the beginning of this pipe section

    # Rasterize line by line
    for y in range(y_min, y_max + 1):
        # Area for each line can be calculated separately
        for x in range(x_min, x_max + 1):
            pos = Pos(x, y)

            # If this is not a pipe, skip it
            # Also, if we are currently inside the loop, increment area
            if pos not in loop_positions:
                if in_loop:
                    area += 1
                continue

            pipe = pipe_map[pos]
            match pipe:
                case Pipe.up_down:
                    # Immediate cross loop boundary
                    in_loop = not in_loop

                case Pipe.up_right:
                    # Entering pipe section
                    section_head = pipe

                case Pipe.down_right:
                    # Entering pipe section
                    section_head = pipe

                case Pipe.left_right:
                    # Traversing pipe section, just skip
                    pass

                case Pipe.up_left:
                    # Ending pipe section
                    if section_head == Pipe.down_right:
                        in_loop = not in_loop
                    section_head = None

                case Pipe.down_left:
                    # Ending pipe section
                    if section_head == Pipe.up_right:
                        in_loop = not in_loop
                    section_head = None

    return area


def part2(puzzle_input: TextIO) -> int:
    """<solve part 2>"""
    grid = parse(puzzle_input)

    loop_steps = find_loop(grid)
    plugged_map = plug_hole(loop_steps, grid)

    return loop_area(loop_steps, plugged_map)


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
