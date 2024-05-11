"""CLI interface for packaged."""

from __future__ import annotations

import argparse
import os.path
import platform
import sys

from packaged import SourceDirectoryNotFound, ensure_makeself, create_package
from packaged.config import (
    Config,
    ConfigValidationError,
    config_file_exists,
    parse_config,
)


def error(message: str) -> None:
    """Print error message"""
    print(f"\033[1;31mError:\033[m {message}")


def cli(argv: list[str] | None = None) -> int:
    """CLI interface."""
    # Manually set argv from sys.argv, as we need to check its length to
    # choose to parse config instead.
    if argv is None:
        argv = sys.argv[1:]

    if platform.system() == "Windows":
        error("Sorry, Windows is not supported yet. Ask for it on GitHub!")
        return 2

    if len(argv) == 1 and config_file_exists(argv[0]):
        # Use values from config file instead
        try:
            config = parse_config(argv[0])
        except ConfigValidationError as exc:
            error(f"Expected key {exc.key!r} in config")
            return 3

        source_directory, output_path, build_command, startup_command = (
            config.source_directory,
            config.output_path,
            config.build_command,
            config.startup_command,
        )

    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("output_path", help="Filename for the generated binary")
        parser.add_argument(
            "build_command", help="Python command to run when building the package"
        )
        parser.add_argument(
            "startup_command", help="Command to run when the script starts"
        )
        parser.add_argument(
            "source_directory",
            help="Folder containing your python source to package",
            type=os.path.abspath,
            nargs="?",
            default=None,
        )
        args = parser.parse_args(argv, namespace=Config)

        source_directory, output_path, build_command, startup_command = (
            args.source_directory,
            args.output_path,
            args.build_command,
            args.startup_command,
        )

    ensure_makeself()
    try:
        create_package(source_directory, output_path, build_command, startup_command)
    except SourceDirectoryNotFound as exc:
        error(f"Folder {exc.directory_path!r} does not exist.")

    return 0
