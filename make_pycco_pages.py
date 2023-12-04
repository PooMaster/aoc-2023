"""Creates HTML pages from Python sources files using Pycco."""

import argparse
from pathlib import Path
from shutil import rmtree
from typing import Iterator, Sequence

import pycco


def main(include: Sequence[str], exclude: Sequence[str], *, force: bool) -> None:
    """
    Generate Pycco HTML file tree out of a specific subset of sources. The
    subset is controlled by explicit include and exclude patterns.
    """
    build_dest = Path("./pages")
    if build_dest.exists():
        rmtree(build_dest)
    build_dest.mkdir()

    if not include:
        include = ["*.py"]

    all_exclude = Path(".gitignore").read_text().splitlines()
    all_exclude.extend([".git", ".gitignore", ".github"])
    all_exclude.extend(exclude)

    source_files = find_files(Path(), include=include, exclude=all_exclude, force=force)

    pycco.process(
        sources=[str(f) for f in source_files],
        outdir=str(build_dest),
        index=True,
    )


def find_files(path: Path, include: Sequence[str], exclude: Sequence[str] = (), *, force: bool) -> Iterator[Path]:
    """
    Find all files in a path that match one of the include patterns while not
    matching any of the exclude patterns at any level.
    """
    for item in path.iterdir():
        # Exclude some files and dirs
        if any(item.match(pattern) for pattern in exclude):
            continue

        # Ignore any branches that have a ".dontpublish" file
        if (item.parent / ".dontpublish").is_file() and not force:
            continue

        if item.is_dir():
            # Recursively look for files
            yield from find_files(item, include, exclude, force=force)

        elif any(item.match(pattern) for pattern in include):
            # Yield any file that matches the include patterns
            yield item


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include",
        help="Comma separated list of file patterns to include",
    )
    parser.add_argument(
        "--exclude",
        default="day_template,make_pycco_pages.py,noxfile.py,__init__.py",
        help="Comma separated list of file patterns to exclude",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Comma separated list of file patterns to exclude",
    )
    args = parser.parse_args()

    print(args.force)

    include = args.include.split(",") if args.include else []
    exclude = args.exclude.split(",") if args.exclude else []
    main(include, exclude, force=args.force)
