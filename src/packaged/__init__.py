"""packaged - The easiest way to ship python applications."""

from __future__ import annotations

import os.path
import shutil
import subprocess
import urllib.request

import yen

STARTUP_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "startup.template.sh")

MAKESELF_VERSION = "2.5.0"
MAKESELF_DOWNLOAD_URL = (
    "https://github.com/megastep/makeself/releases/download/"
    f"release-{MAKESELF_VERSION}/makeself-{MAKESELF_VERSION}.run"
)
MAKESELF_DOWNLOAD_PATH = os.path.join(os.path.dirname(__file__), ".build_deps")
MAKESELF_PATH = os.path.join(
    MAKESELF_DOWNLOAD_PATH, f"makeself-{MAKESELF_VERSION}", "makeself.sh"
)


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
    source_directory: str, output_file: str, build_command: str, startup_command: str
) -> None:
    """Create the makeself executable, with the startup script in it."""
    startup_script_name = "_packaged_startup.sh"

    packaged_python_path = os.path.join(source_directory, ".packaged_python")
    if os.path.exists(packaged_python_path):
        shutil.rmtree(packaged_python_path)

    try:
        python_version, python_bin_path = yen.ensure_python("3.11")
        python_path = os.path.join(yen.PYTHON_INSTALLS_PATH, python_version)
        python_bin_relpath = os.path.relpath(python_bin_path, python_path)

        # Copy the startup script to the source directory
        startup_script_path = shutil.copyfile(
            STARTUP_TEMPLATE_PATH, os.path.join(source_directory, startup_script_name)
        )

        # Put a standalone python interpreter inside the package
        shutil.copytree(python_path, packaged_python_path)

        # Get the bin folder path relative to source directory
        python_bin_folder = os.path.join(
            packaged_python_path, os.path.dirname(python_bin_relpath)
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

        # Add the startup command right at the end of the startup script
        with open(startup_script_path, "a") as startup_file:
            startup_file.write(f"PATH={python_bin_folder_relpath}:$PATH\n")
            startup_file.write(startup_command)

        os.chmod(startup_script_path, 0o777)

        subprocess.check_call(
            [
                MAKESELF_PATH,
                source_directory,
                output_file,
                output_file,
                # makeself wants the startup script path to be a relative path
                os.path.join(".", startup_script_name),
            ],
        )
    finally:
        # Cleanup the packaged python and startup script
        if os.path.exists(startup_script_path):
            os.remove(startup_script_path)
        if os.path.exists(packaged_python_path):
            shutil.rmtree(packaged_python_path)
