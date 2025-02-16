"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

import pathlib

import pytest


@pytest.fixture
def test_resources() -> pathlib.Path:
    """Provides the resources folder in the tests."""
    return pathlib.Path(__file__).parent / "test_resources"


@pytest.fixture
def src_samples() -> pathlib.Path:
    """Provides the samples folder packed with sources."""
    return pathlib.Path(__file__).parent.parent / "src" / "logtools" / "samples"
