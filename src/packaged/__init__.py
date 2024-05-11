"""packaged - The easiest way to ship python applications."""

from __future__ import annotations

import os.path
import shutil
import subprocess
import tempfile
import urllib.request

import yen


MAKESELF_VERSION = "2.5.0"
MAKESELF_DOWNLOAD_URL = (
    "https://github.com/megastep/makeself/releases/download/"
    f"release-{MAKESELF_VERSION}/makeself-{MAKESELF_VERSION}.run"
)
MAKESELF_DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), ".build_deps")
MAKESELF_PATH = os.path.join(
    MAKESELF_DOWNLOAD_PATH, f"makeself-{MAKESELF_VERSION}", "makeself.sh"
)


class SourceDirectoryNotFound(Exception):
    """Raised when provided directory to package does not exist."""

    def __init__(self, directory_path: str) -> None:
        super().__init__(directory_path)
        self.directory_path = directory_path


def ensure_makeself() -> None:
    """If `makeself.sh` doesn't exist, downloads it."""
    if os.path.exists(MAKESELF_PATH):
        return

    if not os.path.exists(MAKESELF_DOWNLOAD_PATH):
        os.mkdir(MAKESELF_DOWNLOAD_PATH)

    makeself_run_path = os.path.join(MAKESELF_DOWNLOAD_PATH, "makeself.run")
    urllib.request.urlretrieve(MAKESELF_DOWNLOAD_URL, makeself_run_path)

    os.chmod(makeself_run_path, 0o777)
    subprocess.check_call(
        [makeself_run_path, "--nox11"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=MAKESELF_DOWNLOAD_PATH,
    )


def create_package(
    source_directory: str | None,
    output_path: str,
    build_command: str,
    startup_command: str,
) -> None:
    """Create the makeself executable, with the startup script in it."""
    if source_directory is None:
        source_directory = tempfile.mkdtemp()

    if not os.path.isdir(source_directory):
        raise SourceDirectoryNotFound(source_directory)

    startup_script_name = "_packaged_startup.sh"
    startup_script_path = os.path.join(source_directory, startup_script_name)

    packaged_python_path = os.path.join(source_directory, ".packaged_python")
    if os.path.exists(packaged_python_path):
        shutil.rmtree(packaged_python_path)

    try:
        # Use `yen` to ensure a portable Python is present on the system
        python_version, yen_python_bin_path = yen.ensure_python("3.11")
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
