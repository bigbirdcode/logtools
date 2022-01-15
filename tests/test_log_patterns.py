"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

# pragma pylint: disable=missing-docstring,unused-argument,redefined-outer-name


import pathlib

import pytest
from strictyaml import YAMLValidationError

from logtools.log_patterns import LogPatterns, parse_yml


TEST_PATTERNS_YML = pathlib.Path("tests/test_patterns.yml")


def test_parse_yml_ok():
    yml = """
    - App start:
        pattern: \\[InitializeApplication\\] Initialized Application ([0-9.]+)
        block_start: True
        needed: False
        property: \\1
        style:
          - bold
          - green
        visible: True
    """
    result = parse_yml(yml)
    assert len(result) == 1
    assert result[0].name == "App start"


def test_parse_yml_wrong_bool():
    yml = """
    - App start:
        pattern: \\[InitializeApplication\\] Initialized Application ([0-9.]+)
        block_start: NonBool
        needed: False
        property: \\1
        style:
          - bold
          - green
        visible: True
    """
    with pytest.raises(YAMLValidationError):
        _ = parse_yml(yml)


def test_parse_yml_wrong_missing():
    yml = """
    - App start:
        pattern: \\[InitializeApplication\\] Initialized Application ([0-9.]+)
        needed: False
        property: \\1
        style:
          - bold
          - green
        visible: True
    """
    with pytest.raises(YAMLValidationError):
        _ = parse_yml(yml)


def test_read_yml():
    lps = LogPatterns(TEST_PATTERNS_YML)
    assert list(lps.get_names()) == ["App start", "App end"]


def test_get_block_starts():
    lps = LogPatterns(TEST_PATTERNS_YML)
    patterns = list(lps.get_block_starts())
    assert len(patterns) == 1
    assert patterns[0].name == "App start"


def test_get_patterns():
    lps = LogPatterns(TEST_PATTERNS_YML)
    patterns = list(lps.get_patterns())
    assert len(patterns) == 2
    assert patterns[0].name == "App start"
    assert patterns[1].name == "App end"


def test_create_from_existing():
    lps = LogPatterns(TEST_PATTERNS_YML)
    lps.patterns[0].count = 5
    lps2 = lps.get_clean_copy()
    assert list(lps2.get_names()) == ["App start", "App end"]
    assert lps2.patterns[0].count == 0
