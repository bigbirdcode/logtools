"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

# ruff: noqa: D103 -  Missing docstring in public function

import pathlib

import pytest
from strictyaml import YAMLValidationError

from logtools.log_pattern import create_empty_pattern
from logtools.log_patterns import LogPatterns, parse_yaml


@pytest.fixture
def test_patterns(test_resources: pathlib.Path) -> LogPatterns:
    return LogPatterns(test_resources / "test_patterns.yml")


def test_parse_yml_ok() -> None:
    yml = """
    App start:
        pattern: \\[InitializeApplication\\] Initialized Application ([0-9.]+)
        block_start: True
        needed: False
        property: 1
        style:
          - bold
          - 00FF00
        visible: True
    """
    result = parse_yaml(yml)
    assert len(result) == 1
    assert result[0].name == "App start"


def test_parse_yml_wrong_bool() -> None:
    yml = """
    App start:
        pattern: \\[InitializeApplication\\] Initialized Application ([0-9.]+)
        block_start: NonBool
        needed: False
        property: \\1
        style:
          - bold
          - 00FF00
        visible: True
    """
    with pytest.raises(YAMLValidationError):
        _ = parse_yaml(yml)


def test_parse_yml_wrong_missing() -> None:
    yml = """
    App start:
        pattern: \\[InitializeApplication\\] Initialized Application ([0-9.]+)
        needed: False
        property: \\1
        style:
          - bold
          - 00FF00
        visible: True
    """
    with pytest.raises(YAMLValidationError):
        _ = parse_yaml(yml)


def test_read_yml(test_patterns: LogPatterns) -> None:
    assert list(test_patterns.get_names()) == ["App start", "App end"]


def test_get_block_starts(test_patterns: LogPatterns) -> None:
    patterns = list(test_patterns.get_block_starts())
    assert len(patterns) == 1
    assert patterns[0].name == "App start"


def test_get_names(test_patterns: LogPatterns) -> None:
    names = list(test_patterns.get_names())
    assert len(names) == 2
    assert names[0] == "App start"
    assert names[1] == "App end"


def test_get_all_patterns(test_patterns: LogPatterns) -> None:
    patterns = list(test_patterns.get_all_patterns())
    assert len(patterns) == 3
    assert patterns[0].name == "App start"
    assert patterns[1].name == "App end"
    assert patterns[2].name == "Free search"


def test_get_yaml_patterns(test_patterns: LogPatterns) -> None:
    patterns = list(test_patterns.get_yaml_patterns())
    assert len(patterns) == 2
    assert patterns[0].name == "App start"
    assert patterns[1].name == "App end"


def test_get_next_p_id(test_patterns: LogPatterns) -> None:
    assert test_patterns.get_next_p_id() == "2"


def test_get_pattern(test_patterns: LogPatterns) -> None:
    pattern = test_patterns.get_pattern("0")
    assert pattern is not None
    assert pattern.name == "App start"


def test_get_free_search_pattern(test_patterns: LogPatterns) -> None:
    pattern = test_patterns.get_pattern("free")
    assert pattern is not None
    assert pattern.name == "Free search"


def test_add_pattern(test_patterns: LogPatterns) -> None:
    pattern = create_empty_pattern()
    pattern.name = "New pattern"
    test_patterns.add_pattern(pattern)
    patterns = list(test_patterns.get_all_patterns())
    assert len(patterns) == 4
    assert patterns[0].name == "App start"
    assert patterns[1].name == "App end"
    assert patterns[2].name == "New pattern"
    assert patterns[3].name == "Free search"


def test_update_pattern(test_patterns: LogPatterns) -> None:
    pattern = create_empty_pattern()
    pattern.name = "New pattern"
    pattern.p_id = "1"
    test_patterns.update_pattern(pattern)
    patterns = list(test_patterns.get_all_patterns())
    assert len(patterns) == 3
    assert patterns[0].name == "App start"
    assert patterns[1].name == "New pattern"
    assert patterns[2].name == "Free search"
