from functools import partial
import logging
import re
from typing import Iterable

# logging.basicConfig(level=logging.DEBUG)


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

digit_list = list(digit_dict.keys())
digit_list.extend("0123456789")

all_digits = "|".join(digit_list)
digit_pattern = re.compile(f"(?=({all_digits}))")


def get_line_digits(line: str, strict: bool = True) -> list[str]:
    if strict:
        return re.findall(r"\d", line)
    else:
        return re.findall(digit_pattern, line)


def test_get_line_digits() -> None:
    # Part 1
    assert get_line_digits("1abc2") == ["1", "2"]
    assert get_line_digits("pqr3stu8vwx") == ["3", "8"]
    assert get_line_digits("a1b2c3d4e5f") == ["1", "2", "3", "4", "5"]
    assert get_line_digits("treb7uchet") == ["7"]

    # Part 2
    assert get_line_digits("two1nine", strict=False) == ["two", "1", "nine"]
    assert get_line_digits("eightwothree", strict=False) == ["eight", "two", "three"]
    assert get_line_digits("abcone2threexyz", strict=False) == ["one", "2", "three"]
    assert get_line_digits("xtwone3four", strict=False) == ["two", "one", "3", "four"]
    assert get_line_digits("4nineeightseven2", strict=False) == [
        "4",
        "nine",
        "eight",
        "seven",
        "2",
    ]
    assert get_line_digits("zoneight234", strict=False) == [
        "one",
        "eight",
        "2",
        "3",
        "4",
    ]
    assert get_line_digits("7pqrstsixteen", strict=False) == ["7", "six"]


def get_line_value(line: str, strict: bool = True) -> int:
    digits = get_line_digits(line, strict=strict)

    logging.debug(digits)

    if not strict:
        digits = [digit_dict.get(d, d) for d in digits]
        logging.debug(digits)

    return int(digits[0] + digits[-1], 10)


def test_get_line_value() -> None:
    # Part 1
    assert get_line_value("1abc2") == 12
    assert get_line_value("pqr3stu8vwx") == 38
    assert get_line_value("a1b2c3d4e5f") == 15
    assert get_line_value("treb7uchet") == 77

    # Part 2
    assert get_line_value("two1nine", strict=False) == 29
    assert get_line_value("eightwothree", strict=False) == 83
    assert get_line_value("abcone2threexyz", strict=False) == 13
    assert get_line_value("xtwone3four", strict=False) == 24
    assert get_line_value("4nineeightseven2", strict=False) == 42
    assert get_line_value("zoneight234", strict=False) == 14
    assert get_line_value("7pqrstsixteen", strict=False) == 76


def get_calibration_sum(lines: Iterable[str], strict: bool = True) -> int:
    return sum(map(partial(get_line_value, strict=strict), lines))


def test_get_calibration_sum() -> None:
    example = """\
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet"""
    assert get_calibration_sum(example.splitlines()) == 142

    example = """\
        two1nine
        eightwothree
        abcone2threexyz
        xtwone3four
        4nineeightseven2
        zoneight234
        7pqrstsixteen"""
    assert get_calibration_sum(example.splitlines(), strict=False) == 281


def part1(lines: Iterable[str]) -> None:
    print("Part1:", get_calibration_sum(lines))


def part2(lines: Iterable[str]) -> None:
    print("Part2:", get_calibration_sum(lines, strict=False))


if __name__ == "__main__":
    with open("input.txt") as f:
        part1(f)

    with open("input.txt") as f:
        part2(f)
