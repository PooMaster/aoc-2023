"""Controls the running of nox."""

import tempfile
from pathlib import Path
from typing import Any

import nox
from nox.sessions import Session

nox.options.sessions = "lint", "mypy", "xdoctest"

locations = "noxfile.py", "make_pycco_pages.py", "src"
packages = Path("src").glob("day*")


@nox.session(python=["3.10"])
def lint(session: Session) -> None:
    """Perform linting."""
    args = session.posargs or locations
    install_with_constraints(
        session,
        "ruff",
    )
    session.run("ruff", *args)


@nox.session(python=["3.10"])
def mypy(session: Session) -> None:
    """Check types with mypy."""
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
    install_with_constraints(session, "xdoctest", "pygments")
    for package in packages:
        session.run("python", "-m", "xdoctest", str(package), *args)


def install_with_constraints(
    session: Session,
    *args: str,
    **kwargs: Any,  # noqa: ANN401
) -> None:
    """Install given modules in constrained environment."""
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

    Path(requirements.name).unlink()
