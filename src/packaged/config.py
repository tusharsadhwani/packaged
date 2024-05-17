from __future__ import annotations

from dataclasses import dataclass
import os
import sys

if sys.version_info < (3, 11):
    import tomli as tomllib
else:
    import tomllib


class ConfigValidationError(Exception):
    """Raised when the toml config has some problem."""

    def __init__(self, key: str) -> None:
        super().__init__(key)
        self.key = key


@dataclass
class Config:
    source_directory: str | None
    output_path: str
    build_command: str
    startup_command: str
    python_version: str


CONFIG_NAME = "./packaged.toml"


def config_file_exists(source_directory: str) -> bool:
    """Returns true if `packaged.toml` exists in current directory."""
    return os.path.isfile(os.path.join(source_directory, CONFIG_NAME))


def parse_config(source_directory: str) -> Config:
    """
    Parses the config file according to this format:

    source_directory = "."
    output_path = "myproject.bin"
    build_command = "pip install ."
    startup_command = "python -m myproject"
    """
    with open(os.path.join(source_directory, CONFIG_NAME), "rb") as config_file:
        config_data = tomllib.load(config_file)

    try:
        config = Config(
            os.path.abspath(source_directory),
            config_data["output_path"],
            config_data["build_command"],
            config_data["startup_command"],
            config_data.get("python_version", "3.12"),
        )
    except KeyError as exc:
        key = exc.args[0]
        raise ConfigValidationError(key)

    return config
