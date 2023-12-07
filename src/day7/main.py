"""
### Part 1:

<paste in problem description here>
"""
from __future__ import annotations

import io
import logging
from collections import Counter
from enum import IntEnum
from itertools import count
from pathlib import Path
from typing import Iterable, Iterator, NamedTuple, NewType, TextIO


def test_score_kinds() -> None:
    # Every hand is exactly one type. From strongest to weakest, they are:

    def score(hand_str: str) -> HandScore:
        return score_hand(Hand.from_str(hand_str))

    # > **Five of a kind**, where all five cards have the same label: `AAAAA`
    assert score("AAAAA").kind == HandKind.five_of_a_kind

    # > **Four of a kind**, where four cards have the same label and one card
    # > has a different label: `AA8AA`
    assert score("AA8AA").kind == HandKind.four_of_a_kind

    # > **Full house**, where three cards have the same label, and the remaining
    # > two cards share a different label: `23332`
    assert score("23332").kind == HandKind.full_house

    # > **Three of a kind**, where three cards have the same label, and the
    # > remaining two cards are each different from any other card in the hand:
    # > `TTT98`
    assert score("TTT98").kind == HandKind.three_of_a_kind

    # > **Two pair**, where two cards share one label, two other cards share a
    # > second label, and the remaining card has a third label: `23432`
    assert score("23432").kind == HandKind.two_pair

    # > **One pair**, where two cards share one label, and the other three cards
    # > have a different label from the pair and each other: `A23A4`
    assert score("A23A4").kind == HandKind.one_pair

    # > **High card**, where all cards' labels are distinct: `23456`
    assert score("23456").kind == HandKind.high_card


def test_part1() -> None:
    def score(hand_str: str) -> HandScore:
        return score_hand(Hand.from_str(hand_str))

    # So, `33332` and `2AAAA` are both four of a kind hands, but `33332` is
    # stronger because its first card is stronger.
    assert score("33332").kind is HandKind.four_of_a_kind
    assert score("2AAAA").kind is HandKind.four_of_a_kind
    assert score("33332") > score("2AAAA")

    # Similarly, `77888` and `77788` are both a full house, but `77888` is
    # stronger because its third card is stronger (and both hands have the same
    # first and second card).
    assert score("77888").kind is HandKind.full_house
    assert score("77788").kind is HandKind.full_house
    assert score("77888") > score("77788")

    """For example:"""
    example = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""" #

    assert score("32T3K") < score("KTJJT") < score("KK677") < score("T55J5") < score("QQQJA")

    # > `""` results in  `...`.
    assert part1(io.StringIO(example)) == 6440


"""
<end of problem description>
"""

# === Part 1 Solution: ===


CARD_LABELS = "23456789TJQKA"


Card = NewType("Card", int)


# Mapping of card label to card value
cards: dict[str, Card] = dict(zip(CARD_LABELS, map(Card, count(2))))


class Hand:
    def __init__(self, cards: Iterable[Card]):
        self.cards = list(cards)
        assert len(self.cards) == 5

    @classmethod
    def from_str(cls, hand_str: str) -> Hand:
        return cls([cards[label] for label in hand_str])

    def __iter__(self) -> Iterator[Card]:
        yield from self.cards

    def __repr__(self) -> str:
        cards_str = "".join(CARD_LABELS[c-2] for c in self.cards)
        return f"Hand({cards_str!r})"


# Enumeration of all possible hand types.
class HandKind(IntEnum):
    five_of_a_kind = 7
    four_of_a_kind = 6
    full_house = 5
    three_of_a_kind = 4
    two_pair = 3
    one_pair = 2
    high_card = 1


# This type is designed to hold the score of a handle that should be
# appropriately comparable to any other hand score. First, there is the kind of
# hand. Second, there is a list of card values from most significant to tie
# breaking to least.
class HandScore(NamedTuple):
    kind: HandKind
    cards: list[Card]


def score_hand(hand: Hand, *, use_jokers: bool = False) -> HandScore:  # noqa: PLR0911
    if use_jokers:
        # Swap jacks with jokers
        hand = Hand(Card(1) if card == Card(11) else card for card in hand)

    cards = Counter(hand)

    if Card(1) in cards:
        # Add joker count to the next common card type
        joker_count = cards.pop(Card(1))
        if cards:
            most_common_card, _ = cards.most_common()[0]
            cards[most_common_card] += joker_count
        else:
            # It's all jokers
            cards[Card(1)] = joker_count


    match cards.most_common():
        case [(_, 5)]:
            return HandScore(HandKind.five_of_a_kind, list(hand))

        case [(_, 4), (_, 1)]:
            return HandScore(HandKind.four_of_a_kind, list(hand))

        case [(_, 3), (_, 2)]:
            return HandScore(HandKind.full_house, list(hand))

        case [(_, 3), (_, 1), (_, 1)]:
            return HandScore(HandKind.three_of_a_kind, list(hand))

        case [(_, 2), (_, 2), (_, 1)]:
            return HandScore(HandKind.two_pair, list(hand))

        case [(_, 2), (_, 1), (_, 1), (_, 1)]:
            return HandScore(HandKind.one_pair, list(hand))

        case _:
            return HandScore(HandKind.high_card, list(hand))


def score_hand_sane(hand: Hand) -> HandScore:  # noqa: PLR0911
    match Counter(hand).most_common():
        case [(five, 5)]:
            return HandScore(HandKind.five_of_a_kind, [five])

        case [(four, 4), (single, 1)]:
            return HandScore(HandKind.four_of_a_kind, [four, single])

        case [(three, 3), (pair, 2)]:
            return HandScore(HandKind.full_house, [three, pair])

        case [(three, 3), (single1, 1), (single2, 1)]:
            return HandScore(HandKind.three_of_a_kind, [three, *sorted([single1, single2], reverse=True)])

        case [(pair1, 2), (pair2, 2), (single, 1)]:
            return HandScore(HandKind.two_pair, [*sorted([pair1, pair2], reverse=True), single])

        case [(pair, 2), (single1, 1), (single2, 1), (single3, 1)]:
            return HandScore(HandKind.one_pair, [pair, *sorted([single1, single2, single3], reverse=True)])

        case _:
            cards = sorted(hand, reverse=True)
            return HandScore(HandKind.high_card, cards)


class Play(NamedTuple):
    hand: Hand
    bid: int


def parse(puzzle_input: TextIO) -> Iterable[Play]:
    for line in puzzle_input:
        hand, bid = line.strip().split()
        yield Play(Hand.from_str(hand), int(bid))


def part1(puzzle_input: TextIO) -> int:
    """<solve part 1>"""
    plays = parse(puzzle_input)
    ranked_plays = sorted(plays, key=lambda p: score_hand(p.hand))
    return sum(rank * play.bid for rank, play in enumerate(ranked_plays, start=1))


"""
### Part 2:

<paste in problem description here>
"""


def test_part2() -> None:
    """For example:"""
    example = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""" #

    def score(hand_str: str) -> HandScore:
        return score_hand(Hand.from_str(hand_str), use_jokers=True)

    logging.debug(score("KTJJT"))

    assert score("32T3K") < score("KK677")
    assert score("KK677") < score("T55J5")
    assert score("T55J5") < score("QQQJA")
    assert score("QQQJA") < score("KTJJT")

    # > `""` results in  `...`.
    assert part2(io.StringIO(example)) == 5905


"""
<end of problem description>
"""

# === Part 2 Solution: ===


def part2(puzzle_input: TextIO) -> int:
    """<solve part 2>"""
    plays = parse(puzzle_input)
    ranked_plays = sorted(plays, key=lambda p: score_hand(p.hand, use_jokers=True))
    return sum(rank * play.bid for rank, play in enumerate(ranked_plays, start=1))


if __name__ == "__main__":
    # Print out part 1 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 1:", part1(puzzle_input))

    # Print out part 2 solution
    with Path("input.txt").open() as puzzle_input:
        print("Part 2:", part2(puzzle_input))
