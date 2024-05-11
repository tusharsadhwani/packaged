"""CLI interface for packaged."""

from __future__ import annotations

import argparse
import os.path
import platform

from packaged import SourceDirectoryNotFound, ensure_makeself, create_package


class CLIArgs:
    source_directory: str
    output_path: str
    build_command: str
    startup_command: str


def error(message: str) -> None:
    """Print error message"""
    print(f"\033[1;31mError:\033[m {message}")


def cli(argv: list[str] | None = None) -> int:
    """CLI interface."""
    parser = argparse.ArgumentParser()
    parser.add_argument("output_path", help="Filename for the generated binary")
    parser.add_argument(
        "build_command", help="Python command to run when building the package"
    )
    parser.add_argument("startup_command", help="Command to run when the script starts")
    parser.add_argument(
        "source_directory",
        help="Folder containing your python source to package",
        type=os.path.abspath,
        nargs="?",
        default=None,
    )
    args = parser.parse_args(argv, namespace=CLIArgs)

    if platform.system() == "Windows":
        error("Sorry, Windows is not supported yet. Ask for it on GitHub!")
        return 2

    ensure_makeself()
    try:
        create_package(
            args.source_directory,
            args.output_path,
            args.build_command,
            args.startup_command,
        )
    except SourceDirectoryNotFound as exc:
        error(f"Folder {exc.directory_path!r} does not exist.")

    return 0
