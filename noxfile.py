import os
from pathlib import Path
import tempfile
from typing import Any

import nox
from nox.sessions import Session


nox.options.sessions = "lint", "mypy", "xdoctest"

locations = "noxfile.py", "make_pycco_pages.py", "src"
packages = Path("src").glob("day*")


@nox.session(python=["3.10"])
def lint(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(
        session,
        "ruff",
    )
    session.run("ruff", *args)


@nox.session(python=["3.10"])
def mypy(session: Session) -> None:
    args = session.posargs or locations
    install_with_constraints(
        session,
        "mypy",
    )
    session.run("mypy", *args)


@nox.session(python=["3.10"])
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    # session.run("poetry", "install", "--only", "main", external=True)
    install_with_constraints(session, "xdoctest", "pygments")
    for package in packages:
        session.run("python", "-m", "xdoctest", str(package), *args)


def install_with_constraints(
    session: Session,
    *args: str,
    **kwargs: Any,  # noqa: ANN401
) -> None:
    with tempfile.NamedTemporaryFile(delete=False) as requirements:
        session.run(
            "poetry",
            "export",
            "--with",
            "dev",
            "--without-hashes",
            "--format=requirements.txt",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)

    os.unlink(requirements.name)
