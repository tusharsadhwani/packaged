import os
import packaged


def test_ensure_makeself() -> None:
    """Tests greet() from the package."""
    packaged.ensure_makeself()
    assert os.path.exists(packaged.MAKESELF_PATH)
