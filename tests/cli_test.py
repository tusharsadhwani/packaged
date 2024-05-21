from __future__ import annotations

from unittest import mock

import packaged
import packaged.cli


def test_cli() -> None:
    """Ensures that CLI passes args to `create_package()` properly."""
    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(["./foo", "pip install foo", "python -m foo"])

    # source_directory is None
    mocked.assert_called_with(
        None,
        "./foo",
        "pip install foo",
        "python -m foo",
        packaged.DEFAULT_PYTHON_VERSION,
        False,
    )

    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(
            ["./baz", "pip install baz", "python -m baz", "--python-version=3.10"]
        )

    # specified python version
    mocked.assert_called_with(
        None, "./baz", "pip install baz", "python -m baz", "3.10", False
    )

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
        packaged.DEFAULT_PYTHON_VERSION,
        False,
    )
    args = mocked.call_args[0]
    assert args[0].endswith("/mypackage")

    # Test --quiet
    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(
            ["./some", "pip install some", "python some.py", "./some.bin", "--quiet"]
        )

    # quiet is True
    mocked.assert_called_with(
        mock.ANY,
        "./some",
        "pip install some",
        "python some.py",
        packaged.DEFAULT_PYTHON_VERSION,
        True,
    )
