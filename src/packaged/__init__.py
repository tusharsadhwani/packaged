"""packaged - The easiest way to ship python applications."""

from __future__ import annotations

import os.path
import shutil
import subprocess
import tempfile

import yen.github


MAKESELF_PATH = os.path.join(os.path.dirname(__file__), "makeself.sh")
DEFAULT_PYTHON_VERSION = "3.12"
PACKAGED_PYTHON_FOLDER_NAME = ".packaged_python"


class SourceDirectoryNotFound(Exception):
    """Raised when provided directory to package does not exist."""

    def __init__(self, directory_path: str) -> None:
        super().__init__(directory_path)
        self.directory_path = directory_path


class PythonNotAvailable(Exception):
    """Raised when the Python version asked for is not available for download."""

    def __init__(self, python_version: str) -> None:
        super().__init__(python_version)
        self.python_version = python_version


def create_package(
    source_directory: str | None,
    output_path: str,
    build_command: str,
    startup_command: str,
    python_version: str,
) -> None:
    """Create the makeself executable, with the startup script in it."""
    if source_directory is None:
        source_directory = tempfile.mkdtemp()

    if not os.path.isdir(source_directory):
        raise SourceDirectoryNotFound(source_directory)

    startup_script_name = "_packaged_startup.sh"
    startup_script_path = os.path.join(source_directory, startup_script_name)

    packaged_python_path = os.path.join(source_directory, PACKAGED_PYTHON_FOLDER_NAME)
    if os.path.exists(packaged_python_path):
        shutil.rmtree(packaged_python_path)

    try:
        # Use `yen` to ensure a portable Python is present on the system
        python_version, yen_python_bin_path = ensure_python(python_version)
        yen_python_path = os.path.join(yen.PYTHON_INSTALLS_PATH, python_version)
        yen_python_bin_relpath = os.path.relpath(yen_python_bin_path, yen_python_path)

        # Put a standalone python interpreter inside the package
        shutil.copytree(yen_python_path, packaged_python_path)

        # Get the `python/bin` folder path relative to source directory
        python_bin_folder = os.path.join(
            packaged_python_path, os.path.dirname(yen_python_bin_relpath)
        )
        python_bin_folder_relpath = os.path.relpath(python_bin_folder, source_directory)

        # Run the build command in the source directory, while making sure
        # that `python` and related binaries point to the installed python
        subprocess.check_call(
            [build_command],
            shell=True,
            env={
                "PATH": os.pathsep.join([python_bin_folder, os.environ.get("PATH", "")])
            },
            cwd=source_directory,
        )

        # The startup script is simply the startup command, prepended with a PATH
        # change to ensure that `python` refers to the bundled python.
        with open(startup_script_path, "w") as startup_file:
            startup_file.write(f"PATH={python_bin_folder_relpath}:$PATH\n")
            startup_file.write(startup_command)

        os.chmod(startup_script_path, 0o777)

        # Patch console scripts, replacing the shebang with /usr/bin/env
        for filename in os.listdir(python_bin_folder):
            filepath = os.path.join(python_bin_folder, filename)
            if not os.path.isfile(filepath):
                continue

            with open(filepath, "rb") as file:
                first_two_bytes = file.read(2)
                if first_two_bytes != b"#!":
                    continue

                shebang_command = file.readline()
                first_line = file.readline()
                second_line = file.readline()
                rest_of_file = file.read()

            # Case 1: shebang points to packaged python
            # File looks like this:
            # #!/path/to/.packaged_python/python/bin/python3.12
            # ... rest of python code
            if PACKAGED_PYTHON_FOLDER_NAME.encode() in shebang_command:
                # rewrite this file to have a `env python` shebang
                with open(filepath, "wb") as file:
                    file.write(b"#!/usr/bin/env python\n")
                    file.write(first_line)
                    file.write(second_line)
                    file.write(rest_of_file)
            # Case 2: shebang is /bin/sh, but the script is an `exec`
            # with the shebang to packaged python.
            # File looks like this:
            # #!/bin/sh
            # '''exec' /path/to/.packaged_python/python/bin/python3.12 "$0" "$@"
            # ' '''
            # ... rest of python code
            elif (
                first_line.startswith(b"'''exec' ")
                and PACKAGED_PYTHON_FOLDER_NAME.encode() in first_line
            ):
                # rewrite this file to have a `env python` shebang,
                # and get rid of the first two lines as they're not needed
                assert second_line == b"' '''\n"
                with open(filepath, "wb") as file:
                    file.write(b"#!/usr/bin/env python\n")
                    file.write(rest_of_file)
                first_line
            else:
                continue

        # This uses `makeself` to build the binary
        subprocess.check_call(
            [
                MAKESELF_PATH,
                # Path to package
                source_directory,
                # Filename to output
                output_path,
                # Label for the package, for now it's just the filename
                output_path,
                # The command to run when starting the package.
                # `makeself` wants the startup script path to be a relative path
                os.path.join(".", startup_script_name),
            ],
        )
    finally:
        # Cleanup the packaged python and startup script from source directory
        if os.path.exists(startup_script_path):
            os.remove(startup_script_path)
        if os.path.exists(packaged_python_path):
            shutil.rmtree(packaged_python_path)


def ensure_python(version: str) -> tuple[str, str]:
    """
    Checks that the version of Python we want to use is available on the
    system, and if not, downloads it.
    """
    try:
        return yen.ensure_python(version)
    except yen.github.NotAvailable:
        raise PythonNotAvailable(version)
