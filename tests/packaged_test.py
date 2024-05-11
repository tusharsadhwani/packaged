import contextlib
import os
import subprocess
from typing import Iterator

import packaged


TEST_PACKAGES = os.path.join(os.path.dirname(__file__), "test_packages")


@contextlib.contextmanager
def build_package(
    source_directory: str | None,
    output_path: str,
    build_command: str,
    startup_command: str,
) -> Iterator[None]:
    """Builds the package, but also delete it afterwards."""
    try:
        packaged.create_package(
            source_directory, output_path, build_command, startup_command
        )
        yield
    finally:
        if os.path.exists(output_path):
            os.remove(output_path)


def get_output(path: str) -> str:
    """Runs the executable with `--nox11` so that it still works as a subprocess."""
    return subprocess.check_output([path, "--nox11"]).decode()


def test_just_python() -> None:
    """Packages `just_python` to test packaging with no dependencies."""
    package_path = os.path.join(TEST_PACKAGES, "just_python")
    executable_path = "./just_python.bin"
    with build_package(package_path, executable_path, "", "python foo.py"):
        assert "Although practicality beats purity." in get_output(executable_path)


def test_numpy_pandas() -> None:
    """Packages `numpy_pandas` to test packaging the math stack."""
    package_path = os.path.join(TEST_PACKAGES, "numpy_pandas")
    executable_path = "./numpy_pandas.bin"
    with build_package(
        package_path,
        executable_path,
        "pip install numpy pandas",
        "python somefile.py",
    ):
        assert "0   -2.222222\ndtype: float64" in get_output(executable_path)
