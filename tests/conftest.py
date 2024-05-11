import os
import time

import pytest
import yen

import packaged


def pytest_sessionstart(session: pytest.Session) -> None:
    """
    Makeself and yen Pythons need to exist before any other test runs,
    so this runs before the tests get collected, while also testing
    `ensure_makeself()`.
    """
    # Taken from https://github.com/pytest-dev/pytest-xdist/issues/271
    if getattr(session.config, "workerinput", None) is not None:
        # This is a worker process, wait for main to finish working.
        while not os.path.exists(packaged.MAKESELF_PATH):
            time.sleep(1)
        while not os.path.exists(yen.PYTHON_INSTALLS_PATH):
            time.sleep(1)

        return

    packaged.ensure_makeself()
    assert os.path.exists(packaged.MAKESELF_PATH)
    yen.ensure_python("3.11")
    assert os.path.exists(yen.PYTHON_INSTALLS_PATH)
