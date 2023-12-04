"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
import logging
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, NamedTuple, TextIO


def test_part1() -> None:
    """For example:"""
    example = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""  # pycco needs this

    cards = parse_cards(io.StringIO(example))
    logging.debug(list(cards))

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == 13


"""
<end of problem description>
"""

# === Part 1 Solution: ===


class Card(NamedTuple):
    number: int
    winning_numbers: set[int]
    have_numbers: set[int]


line_pattern = re.compile(r"Card +(\d+): ([\d ]+) \| ([\d ]+)")

def parse_cards(puzzle_input: TextIO) -> Iterable[Card]:
    for line in puzzle_input:
        if m := line_pattern.fullmatch(line.strip()):
            yield Card(
                number=int(m.group(1)),
                winning_numbers={int(num) for num in m.group(2).split()},
                have_numbers={int(num) for num in m.group(3).split()},
            )
        else:
            raise ValueError(line)


def card_win_count(card: Card) -> int:
    return len(card.winning_numbers & card.have_numbers)


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    cards = parse_cards(puzzle_input)
    win_count = (card_win_count(c) for c in cards)
    points = ((0 if wc == 0 else 2 ** (wc-1)) for wc in win_count)

    return sum(points)


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""  # pycco needs this

    cards = parse_cards(io.StringIO(example))

    card_it = iter(cards)
    assert card_copy_winnings(next(card_it)) == Counter([2, 3, 4, 5])
    assert card_copy_winnings(next(card_it)) == Counter([3, 4])
    assert card_copy_winnings(next(card_it)) == Counter([4, 5])

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 30


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def card_copy_winnings(card: Card) -> Counter[int]:
    wins = card_win_count(card)
    return Counter(range(card.number + 1, card.number + wins + 1))


def counter_multiply(counter: Counter[int], multiplier: int) -> Counter[int]:
    return Counter({k: count*multiplier for k, count in counter.items()})


def part2(puzzle_input: TextIO) -> int:
    card_counts: Counter[int] = Counter()

    for card in parse_cards(puzzle_input):
        # Received the original card
        card_counts.setdefault(card.number, 0)
        card_counts[card.number] += 1

        won_cards = card_copy_winnings(card)
        card_counts += counter_multiply(won_cards, card_counts[card.number])

    """<solve part 2>"""
    return card_counts.total()


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
