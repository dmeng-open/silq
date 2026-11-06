from importlib.metadata import version

import silq


def test_installed_package_version_matches_module_version() -> None:
    assert silq.__version__ == version("silq")
