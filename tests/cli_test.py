from __future__ import annotations

from unittest import mock

from pytest import MonkeyPatch

import packaged.cli


def test_cli(monkeypatch: MonkeyPatch) -> None:
    """Ensures that CLI passes args to `create_package()` properly."""
    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(["./foo", "pip install foo", "python -m foo"])

    # source_directory is None
    mocked.assert_called_with(None, "./foo", "pip install foo", "python -m foo")

    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(
            [
                "./bar",
                "pip install -rrequirements.txt",
                "python src/mypackage/cli.py",
                "./mypackage",
            ]
        )

    # source_directory is `./mypackage`
    mocked.assert_called_with(
        mock.ANY,
        "./bar",
        "pip install -rrequirements.txt",
        "python src/mypackage/cli.py",
    )
    args = mocked.call_args[0]
    assert args[0].endswith("/mypackage")
