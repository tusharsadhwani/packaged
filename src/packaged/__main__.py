"""Support executing the CLI by doing `python -m packaged`."""
from __future__ import annotations

from packaged.cli import cli

if __name__ == "__main__":
    raise SystemExit(cli())
