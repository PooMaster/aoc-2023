"""
### Part 1:

You take the boat and find the gardener right where you were told he would be:
managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow
Island isn't receiving any water.

"Oh, we had to stop the water because we **ran out of sand** to filter it with!
Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand
soon; we only turned off the water a few days... weeks... oh no." His face sinks
into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot
to check why we stopped getting more sand! There's a ferry leaving soon that is
headed over in that direction - it's much faster than your boat. Could you
please go check it out?"

You barely have time to agree to this request when he brings up another. "While
you wait for the ferry, maybe you can help us with our **food production
problem.** The latest Island Island Almanac just arrived and we're having
trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted.
It also lists what type of soil to use with each kind of seed, what type of
fertilizer to use with each kind of soil, what type of water to use with each
kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is
identified with a number, but numbers are reused by each category - that is,
soil `123` and fertilizer `123` aren't necessarily related to each other.
"""
from __future__ import annotations

import bisect
import io
from itertools import pairwise
import logging
from pathlib import Path
from typing import Iterable, NamedTuple, TextIO, overload

from more_itertools import chunked


def test_part1() -> None:
    """For example:"""
    example = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""  # pycco needs this

    almanac = parse_almanac(io.StringIO(example))

    # The almanac starts by listing which seeds need to be planted: seeds `79`,
    # `14`, `55`, and `13`.
    assert almanac.seeds == [79, 14, 55, 13]

    """
    The rest of the almanac contains a list of **maps** which describe how to
    convert numbers from a **source category** into numbers in a **destination
    category**. That is, the section that starts with `seed-to-soil map:`
    describes how to convert a **seed number** (the source) to a **soil number**
    (the destination). This lets the gardener and his team know which soil to
    use with which seeds, which water to use with which fertilizer, and so on.

    Rather than list every source number and its corresponding destination
    number one by one, the maps describe entire **ranges** of numbers that can
    be converted. Each line within a map contains three numbers: the
    **destination range start**, the **source range start**, and the **range
    length**.

    Consider again the example `seed-to-soil map:`

        50 98 2
        52 50 48
    """

    seed_to_soil = almanac.maps[("seed", "soil")]

    # The first line has a destination range start of `50`, a **source range
    # start** of `98`, and a **range length** of `2`.
    first_line = IntervalOffset.from_line("50 98 2")

    # This line means that the source range starts at `98` and contains two
    # values: `98` and `99`.
    assert list(first_line.interval) == [98, 99]

    # The destination range is the same length, but it starts at `50`, so its
    # two values are `50` and `51`. With this information, you know that seed
    # number `98` corresponds to soil number `50` and that seed number `99`
    # corresponds to soil number `51`.
    assert seed_to_soil.get(98) == 50
    assert seed_to_soil.get(99) == 51

    # The second line means that the source range starts at `50` and contains `48`
    # values: `50`, `51`, ..., `96`, `97`.
    second_line = IntervalOffset.from_line("52 50 48")
    assert list(second_line.interval[:2]) == [50, 51]
    assert list(second_line.interval[-2:]) == [96, 97]

    # This corresponds to a destination range starting at `52` and also
    # containing `48` values: `52`, `53`, ..., `98`, `99`. So, seed number `53`
    # corresponds to soil number `55`.
    assert seed_to_soil.get(53) == 55

    # Any source numbers that **aren't mapped** correspond to the **same**
    # destination number. So, seed number 10 corresponds to soil number 10.
    assert seed_to_soil.get(10) == 10

    """
    So, the entire list of seed numbers and their corresponding soil numbers looks like this:

        seed  soil
        0     0
        1     1
        ...   ...
        48    48
        49    49
        50    52
        51    53
        ...   ...
        96    98
        97    99
        98    50
        99    51
    """

    # With this map, you can look up the soil number required for each initial seed number:

    # > Seed number 79 corresponds to soil number 81.
    assert seed_to_soil.get(79) == 81

    # > Seed number 14 corresponds to soil number 14.
    assert seed_to_soil.get(14) == 14

    # > Seed number 55 corresponds to soil number 57.
    assert seed_to_soil.get(55) == 57

    # > Seed number 13 corresponds to soil number 13.
    assert seed_to_soil.get(13) == 13

    # The gardener and his team want to get started as soon as possible, so
    # they'd like to know the closest location that needs a seed. Using these
    # maps, find **the lowest location number that corresponds to any of the
    # initial seeds**. To do this, you'll need to convert each seed number
    # through other categories until you can find its corresponding **location
    # number**. In this example, the corresponding types are:

    # > Seed `79`, soil `81`, fertilizer `81`, water `81`, light `74`, temperature `78`, humidity `78`, location `82`.
    assert walk_maps("seed", 79, almanac.maps) == {
        "seed": 79,
        "soil": 81,
        "fertilizer": 81,
        "water": 81,
        "light": 74,
        "temperature": 78,
        "humidity": 78,
        "location": 82,
    }

    # > Seed `14`, soil `14`, fertilizer `53`, water `49`, light `42`, temperature `42`, humidity `43`, location `43`.
    assert walk_maps("seed", 14, almanac.maps) == {
        "seed": 14,
        "soil": 14,
        "fertilizer": 53,
        "water": 49,
        "light": 42,
        "temperature": 42,
        "humidity": 43,
        "location": 43,
    }

    # > Seed `55`, soil `57`, fertilizer `57`, water `53`, light `46`, temperature `82`, humidity `82`, location `86`.
    assert walk_maps("seed", 55, almanac.maps) == {
        "seed": 55,
        "soil": 57,
        "fertilizer": 57,
        "water": 53,
        "light": 46,
        "temperature": 82,
        "humidity": 82,
        "location": 86,
    }

    # > Seed `13`, soil `13`, fertilizer `52`, water `41`, light `34`, temperature `34`, humidity `35`, location `35`.
    assert walk_maps("seed", 13, almanac.maps) == {
        "seed": 13,
        "soil": 13,
        "fertilizer": 52,
        "water": 41,
        "light": 34,
        "temperature": 34,
        "humidity": 35,
        "location": 35,
    }

    # So, the lowest location number in this example is 35.
    assert part1(io.StringIO(example)) == 35


"""
<end of problem description>
"""

# === Part 1 Solution: ===


class IntervalOffset(NamedTuple):
    interval: range
    offset: int

    @classmethod
    def from_line(cls, line: str) -> IntervalOffset:
        destination_range_start, source_range_start, range_length = (int(num) for num in line.strip().split())

        return cls(
            interval=range(source_range_start, source_range_start + range_length),
            offset=destination_range_start - source_range_start,
        )


class IntervalMap:
    """
    Maps an integer from one domain to another. This mapping is defined by a set
    of interval offset. Each of these consists of an interval in the domain and
    an offset that must be added to map that interval to the domain.
    """

    def __init__(self, interval_offsets: Iterable[IntervalOffset]):
        # Keep the interval offsets sorted so that binary search can be used.
        self.interval_offsets = sorted(interval_offsets, key=lambda io: io.interval.start)

    @overload
    def get(self, value: int) -> int:
        ...

    @overload
    def get(self, value: MultiInterval) -> MultiInterval:
        ...

    def get(self, value):
        """Map integer to new domain according to the interval offsets."""
        if isinstance(value, MultiInterval):
            return self._multi_interval_get(value)

        # First, find which interval offset this value may possibly fall in to.
        interval_index = bisect.bisect(self.interval_offsets, value, key=lambda io: io.interval.start)
        interval_offset = self.interval_offsets[interval_index - 1]  # If this goes -1, then no big deal.

        # If the value falls in to the interval, apply the offset and return.
        if value in interval_offset.interval:
            return value + interval_offset.offset

        # Otherwise, no interval matches so return the value unchanged.
        return value

    def _multi_interval_get(self, value: MultiInterval) -> MultiInterval:
        # First, chop up all of the intervals falling on mapper boundaries
        logging.debug("Before chopping: %r", value.intervals)

        chop_points = [io.interval.start for io in self.interval_offsets]
        chop_points.append(self.interval_offsets[-1].interval.stop)
        chopped_intervals = list(self._chopped_intervals(value.intervals, chop_points))

        logging.debug("After chopping: %r", list(chopped_intervals))

        # Then, map all the chopped intervals to their new values
        mapped_intervals = [(self.get(start), self.get(stop - 1) + 1) for start, stop in chopped_intervals]

        logging.debug("After mapping: %r", list(mapped_intervals))

        return MultiInterval(mapped_intervals)

    @staticmethod
    def _chopped_intervals(intervals: list[tuple[int, int]], boundaries: list[int]) -> Iterable[tuple[int, int]]:
        """Chop up the given intervals on the given boundaries."""
        for start, stop in intervals:
            chop_points = [b for b in boundaries if start < b < stop]
            yield from pairwise([start, *chop_points, stop])


Category = str


class Almanac(NamedTuple):
    seeds: list[int]
    maps: dict[tuple[Category, Category], IntervalMap]


def parse_almanac(puzzle_input: TextIO) -> Almanac:
    def read_stripped() -> str:
        return puzzle_input.readline().strip()

    # The first line has our seed numbers.
    seed_numbers = [int(num) for num in read_stripped().removeprefix("seeds: ").split()]
    read_stripped()  # Skip blank line after seeds line.

    maps = {}

    # _I'm so tempted to turn this into a monster dictionary comprehension._
    for map_title_line in puzzle_input:
        map_name = map_title_line.split()[0]
        source_category, destination_category = map_name.split("-to-")
        maps[source_category, destination_category] = IntervalMap(
            IntervalOffset.from_line(line) for line in iter(read_stripped, "")
        )

    return Almanac(seed_numbers, maps)


@overload
def walk_maps(category: str, value: int, maps: dict[tuple[Category, Category], IntervalMap]) -> dict[str, int]:
    ...


@overload
def walk_maps(
    category: str, value: MultiInterval, maps: dict[tuple[Category, Category], IntervalMap]
) -> dict[str, MultiInterval]:
    ...


def walk_maps(category, value, maps):
    """
    Build up a dictionary of keys and values by traversing the given maps using
    their names and interval maps. A dictonary of categories and values is
    started with a given category and value. Then applicable category mappings
    are discovered and followed successively to build up the dictionary with as
    much information as possible. Once no further info can be added, the
    dictionary is retruned.
    """
    # Start the info dictionary with the given category info.
    info = {category: value}

    # Find another category we can map to from the current category.
    while next_category := next((dest for src, dest in maps if src == category), None):
        # Map the current value into the new category's associated value.
        value = maps[(category, next_category)].get(value)

        # Add this category value to the info dictionary.
        info[next_category] = value

        # Recurse into the next category.
        category = next_category

    return info


def part1(puzzle_input: TextIO) -> ...:
    """<solve part 1>"""
    almanac = parse_almanac(puzzle_input)

    return min(walk_maps("seed", seed, almanac.maps)["location"] for seed in almanac.seeds)


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""  # pycco needs this

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 46


"""
<end of problem description>
"""

# === Part 2 Solution: ===


class MultiInterval:
    """Representation of many intervals."""

    def __init__(self, intervals: Iterable[tuple[int, int]]):
        self.intervals = list(self._simplified_intervals(intervals))

    @staticmethod
    def _simplified_intervals(intervals: Iterable[tuple[int, int]]) -> Iterable[tuple[int, int]]:
        intervals = sorted(
            (start, stop)
            for start, stop in intervals
            if start < stop  # Dump any empty intervals
        )
        if not intervals:
            return

        start, stop = intervals[0]

        for next_start, next_stop in intervals[1:]:
            # There there is a gap in the intervals, yield what you've got.
            if next_start > stop:
                yield start, stop
                start, stop = next_start, next_stop
                continue

            # Combine overlapping intervals
            stop = max(stop, next_stop)

        yield start, stop

    def __eq__(self, other: MultiInterval) -> bool:
        return self.intervals == other.intervals

    def __repr__(self) -> str:
        return f"{self.__class__.__qualname__}({self.intervals})"

    def min_value(self) -> int:
        return self.intervals[0][0]


def test_multi_interval() -> None:
    multi_interval = MultiInterval([(1, 3), (1, 1), (1, 2), (5, 6)])
    assert multi_interval.intervals == [(1, 3), (5, 6)]

    assert multi_interval.min_value() == 1

    seeds = MultiInterval([(79, 79 + 20)])
    mapper = IntervalMap([IntervalOffset.from_line("50 98 2"), IntervalOffset.from_line("52 50 48")])
    assert mapper.get(seeds) == MultiInterval([(50, 51), (81, 100)])
    assert mapper.get(MultiInterval([(79, 105)])) == MultiInterval([(50, 52), (81, 105)])


def part2(puzzle_input: TextIO) -> int:
    """<solve part 2>"""
    almanac = parse_almanac(puzzle_input)

    seeds = [MultiInterval([(start, start + count)]) for start, count in chunked(almanac.seeds, 2)]
    return min(walk_maps("seed", seed, almanac.maps)["location"].min_value() for seed in seeds)


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
