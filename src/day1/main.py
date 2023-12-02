"""
### Part 1:

--- Day 1: Trebuchet?! ---

Something is wrong with global snow production, and you've been selected to take
a look. The Elves have even given you a map; on it, they've used stars to mark
the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you
need to check all **fifty stars** by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the Advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants **one star**. Good luck!

You try to ask why they can't just use a **weather machine** ("not powerful
enough") and where they're even sending you ("the sky") and why your map looks
mostly blank ("you sure ask a lot of questions") and hang on did you just say
the sky ("of course, where do you think snow comes from") when you realize that
the Elves are already loading you into a **trebuchet** ("please hold still, we
need to strap you in").

As they're making the final adjustments, they discover that their calibration
document (your puzzle input) has been **amended** by a very young Elf who was
apparently just excited to show off her art skills. Consequently, the Elves are
having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line
originally contained a specific **calibration value** that the Elves now need to
recover. On each line, the calibration value can be found by combining the
**first digit** and the **last digit** (in that order) to form a single
**two-digit number**.
"""

from functools import partial
import logging
import re
from typing import Iterable


def test_part1() -> None:
    """
    For example:
    """

    example = """\
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet"""  # pycco needs this comment

    lines = example.splitlines()

    """
    In this example, the calibration values of these four lines are `12`, `38`,
    `15`, and `77`.
    """
    line_iter = iter(lines)
    assert get_line_value(next(line_iter)) == 12
    assert get_line_value(next(line_iter)) == 38
    assert get_line_value(next(line_iter)) == 15
    assert get_line_value(next(line_iter)) == 77

    """
    Adding these together produces **`142`**.
    """
    assert get_calibration_sum(lines) == 142


"""
Consider your entire calibration document. **What is the sum of all of the
calibration values?**
"""

# === Part 1 Solution: ===

"""
Since this problem involves scanning through text searching for strings, I
immediately am looking into using `re.findall()`. For part 1, this is super
straightforward since the pattern is just `"\\d"` to grab just the digit
characters.

Since my part 2 solution is so intertwined with the part 1 solution, I'll just
go straight into the part 2 description.
"""

"""
### Part 2:

Your calculation isn't quite right. It looks like some of the digits are
actually **spelled out with letters**: `one`, `two`, `three`, `four`, `five`,
`six`, `seven`, `eight`, and `nine` also count as valid "digits".
"""

digit_dict: dict[str, str] = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

"""
Equipped with this new information, you now need to find the real first and last
digit on each line.
"""


def test_part2() -> None:
    """
    For example:
    """

    example = """\
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen"""  # pycco needs this comment

    lines = example.splitlines()

    """
    In this example, the calibration values are `29`, `83`, `13`, `24`, `42`,
    `14`, and `76`.
    """
    line_iter = iter(lines)
    assert get_line_value(next(line_iter), use_words=True) == 29
    assert get_line_value(next(line_iter), use_words=True) == 83
    assert get_line_value(next(line_iter), use_words=True) == 13
    assert get_line_value(next(line_iter), use_words=True) == 24
    assert get_line_value(next(line_iter), use_words=True) == 42
    assert get_line_value(next(line_iter), use_words=True) == 14
    assert get_line_value(next(line_iter), use_words=True) == 76

    """
    Adding these together produces **`281`**.
    """
    assert get_calibration_sum(lines, use_words=True) == 281


"""
**What is the sum of all of the calibration values?**
"""

# === Part 2 Solution: ===

"""
The key different with part 2 is that the strings being searched for can now be
multiple characters long. Thankfully, this will also be pretty simple to
accomplish using regex. All of the enlish word versions of the digits will be
added to the pattern and then translated to their digit equivalent.

To still be able to run the part 1 and part 2 versions of the functions, an
optional keyword `use_words` will be used to enable the part 2 behavior.
"""


# The substrings that need to be found are the digit words and the digit characters
digit_list = list(digit_dict.keys())
digit_list.extend("0123456789")

# All the possible values should be in the regex pattern separated by a pipe
# (`|`) to designate them all as alternatives
all_digits = "|".join(digit_list)

# Then all the pattern of all possible digit substrings should be put in a
# zero-width positive lookahead group. This is a little trick to allow for one
# capture group to overlap with another. The prompt was not specific about if
# this should be allowed, but experimentation proved that it was required to
# complete the puzzle.
digit_pattern = re.compile(f"(?=({all_digits}))")


def get_line_digits(line: str, use_words: bool = False) -> list[str]:
    """
    Take a line of text and return all the digit substrings found within it.
    """
    if not use_words:
        # For part 1, just return each digit character
        return re.findall(r"\d", line)
    else:
        # For part 2, use the compiled digit pattern
        return re.findall(digit_pattern, line)


def test_get_line_digits() -> None:
    """
    Here are some extra tests for the `get_line_digits()` function to debug the
    parsing it does.
    """

    # - Test cases for part 1
    assert get_line_digits("1abc2") == ["1", "2"]
    assert get_line_digits("pqr3stu8vwx") == ["3", "8"]
    assert get_line_digits("a1b2c3d4e5f") == ["1", "2", "3", "4", "5"]
    assert get_line_digits("treb7uchet") == ["7"]

    # - Test cases for part 2
    assert get_line_digits("two1nine", use_words=True) == ["two", "1", "nine"]
    assert get_line_digits("eightwothree", use_words=True) == ["eight", "two", "three"]
    assert get_line_digits("abcone2threexyz", use_words=True) == ["one", "2", "three"]
    assert get_line_digits("xtwone3four", use_words=True) == [
        "two",
        "one",
        "3",
        "four",
    ]
    assert get_line_digits("4nineeightseven2", use_words=True) == [
        "4",
        "nine",
        "eight",
        "seven",
        "2",
    ]
    assert get_line_digits("zoneight234", use_words=True) == [
        "one",
        "eight",
        "2",
        "3",
        "4",
    ]
    assert get_line_digits("7pqrstsixteen", use_words=True) == ["7", "six"]


def get_line_value(line: str, use_words: bool = False) -> int:
    """
    This function takes the digits that are parsed from a line and creates the
    value of the trebuchet calibration, that being the first and last digit
    interpreted as a two digit number.
    """
    digits = get_line_digits(line, use_words=use_words)

    logging.debug(digits)

    if use_words:
        # If spelled out digits are being used, then replace all the english
        # word versions of the digits to single digit characters here.
        digits = [digit_dict.get(d, d) for d in digits]
        logging.debug(digits)

    return int(digits[0] + digits[-1], 10)


def get_calibration_sum(lines: Iterable[str], use_words: bool = False) -> int:
    """
    To get the full calibration sum, just find the calibration value of each
    line and add them up.
    """
    return sum(map(partial(get_line_value, use_words=use_words), lines))


def part1(lines: Iterable[str]) -> None:
    """
    Part 1 just gets the normal calibration sum.
    """
    print("Part1:", get_calibration_sum(lines))


def part2(lines: Iterable[str]) -> None:
    """
    Part 2 just gets the normal calibration sum with spelled out digits
    included.
    """
    print("Part2:", get_calibration_sum(lines, use_words=True))


if __name__ == "__main__":
    with open("input.txt") as f:
        part1(f)

    with open("input.txt") as f:
        part2(f)
