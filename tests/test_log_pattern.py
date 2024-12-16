"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


# WARNING! Test is obsolete, need update!

import copy
import re

import pytest

from logtools.log_pattern import LogPattern


# pragma pylint: disable=missing-docstring,unused-argument,redefined-outer-name,use-implicit-booleaness-not-comparison


GOOD_PATTERN = {
    "pattern": "My Pattern",
    "block_start": True,
    "needed": False,
    "property": "\\1",
    "style": ["bold", "green"],
    "visible": True,
}


@pytest.fixture
def pattern():
    return copy.deepcopy(GOOD_PATTERN)


def test_good_pattern(pattern):
    lpat = LogPattern("My Name", pattern)
    assert lpat.name == "My Name"
    assert isinstance(lpat.pattern, re.Pattern)
    assert lpat.block_start is True
    assert lpat.needed is False
    assert lpat.property == "\\1"
    assert lpat.style == ["bold", "green"]
    assert lpat.visible is True
    assert lpat.count == 0
    assert lpat.lines == []


def test_missing_pattern(pattern):
    del pattern["pattern"]
    with pytest.raises(KeyError):
        _ = LogPattern("My Name", pattern)


def test_get_data(pattern):
    lpat = LogPattern("My Name", pattern)
    name, data = lpat.get_data()
    assert name == "My Name"
    assert data == pattern


def test_get_clean_copy(pattern):
    lpat = LogPattern("My Name", pattern)
    lpat.count = 5
    lpat2 = lpat.get_clean_copy()
    assert lpat2.name == lpat.name
    assert lpat2.count == 0


def test_search(pattern):
    lpat = LogPattern("My Name", pattern)
    assert lpat.search("x My Pattern x", 1)
    assert not lpat.search("x My xx Pattern x", 2)
    assert lpat.has_line(1)
    assert not lpat.has_line(2)
