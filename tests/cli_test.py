from __future__ import annotations

import os
from unittest import mock

from pytest import MonkeyPatch

import packaged
import packaged.cli


def test_cli(monkeypatch: MonkeyPatch) -> None:
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
        False,
        ["setup.py"],
    )

    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(
            ["./baz", "pip install baz", "python -m baz", "--python-version=3.10"]
        )

    # specified python version
    mocked.assert_called_with(
        None,
        "./baz",
        "pip install baz",
        "python -m baz",
        "3.10",
        False,
        False,
        ["setup.py"],
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
        False,
        ["setup.py"],
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
        False,
        ["setup.py"],
    )

    # Test --quiet when CI is true, regardless of if the flag is passed
    monkeypatch.setattr(os, "environ", {"CI": "1"})
    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(["./some", "pip install some", "python some.py", "./some.bin"])

    # quiet is True
    mocked.assert_called_with(
        mock.ANY,
        "./some",
        "pip install some",
        "python some.py",
        packaged.DEFAULT_PYTHON_VERSION,
        True,
        False,
        ["setup.py"],
    )
    monkeypatch.setattr(os, "environ", {"CI": "1"})
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
        False,
        ["setup.py"],
    )

    # unset CI
    monkeypatch.setattr(os, "environ", {})
    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(
            ["./some", "pip install some", "python some.py", "./some.bin", "--pyc"]
        )

    # pyc is True
    mocked.assert_called_with(
        mock.ANY,
        "./some",
        "pip install some",
        "python some.py",
        packaged.DEFAULT_PYTHON_VERSION,
        False,
        True,
        ["setup.py"],
    )

    with mock.patch.object(packaged.cli, "create_package") as mocked:
        packaged.cli.cli(
            [
                "./some",
                "pip install some",
                "python some.py",
                "./some.bin",
                "--pyc",
                "--ignore-file-patterns",
                "foo.py",
                "test/*.py",
            ]
        )

    # pyc is True and ignore_file_patterns is ['foo.py', 'test/*.py']
    mocked.assert_called_with(
        mock.ANY,
        "./some",
        "pip install some",
        "python some.py",
        packaged.DEFAULT_PYTHON_VERSION,
        False,
        True,
        ["foo.py", "test/*.py"],
    )
