# aoc-2023
Advent of Code 2023 Solutions
https://adventofcode.com/2023

See Pycco rendered versions of the solutions on [my GitHub Pages](https://poomaster.github.io/aoc-2023/).

I want to take the opportunity to try out following at least some of this some of [this guide on modern Python devops
processes](https://cjolowicz.github.io/posts/hypermodern-python-01-setup/). Also, I'd like to try embedding the problem
descriptions and development notes in a literate programming style using [Pycco](https://pycco-docs.github.io/pycco/).

To test and run each solution, run each of these steps from inside each day's folder.

- `poetry run flake8 .`
- `poetry run xdoctest .`
- `poetry run pytest *.py`
- `poetry run mypy .`
- `poetry run python main.py`

Project-wide checks can be run using `nox`:

- `nox -rs lint`
- `nox -rs mypy`
- `nox -rs xdoctest`

Or for all check types:

- `nox`
