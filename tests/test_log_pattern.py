"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

# ruff: noqa: D103 -  Missing docstring in public function

import copy
import re
from typing import Any

import pytest

from logtools.log_pattern import LogPattern


GOOD_PATTERN = {
    "pattern": "My Pattern",
    "block_start": True,
    "needed": False,
    "property": "\\1",
    "style": ["bold", "green"],
    "visible": True,
}


pattern_fixture = dict[str, Any]


@pytest.fixture
def pattern() -> pattern_fixture:
    return copy.deepcopy(GOOD_PATTERN)


def test_good_pattern(pattern: pattern_fixture) -> None:
    lpat = LogPattern("My Name", pattern)
    assert lpat.name == "My Name"
    assert isinstance(lpat.pattern, re.Pattern)
    assert lpat.block_start is True
    assert lpat.needed is False
    assert lpat.property == "\\1"
    assert lpat.style == ["bold", "green"]
    assert lpat.visible is True
    assert lpat.modified is False
    assert lpat.style_num == -1


def test_missing_pattern(pattern: pattern_fixture) -> None:
    del pattern["pattern"]
    with pytest.raises(KeyError):
        _ = LogPattern("My Name", pattern)


def test_get_data(pattern: pattern_fixture) -> None:
    lpat = LogPattern("My Name", pattern)
    data = lpat.get_data()
    assert data == pattern


def test_search(pattern: pattern_fixture) -> None:
    lpat = LogPattern("My Name", pattern)
    assert lpat.search("x My Pattern x")
    assert not lpat.search("x My xx Pattern x")
