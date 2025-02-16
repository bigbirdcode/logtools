"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

# ruff: noqa: D103 -  Missing docstring in public function

import pathlib

import pytest
from strictyaml import YAMLValidationError

from logtools.log_patterns import LogPatterns, parse_yaml


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


def test_read_yml(test_resources: pathlib.Path) -> None:
    lps = LogPatterns(test_resources / "test_patterns.yml")
    assert list(lps.get_names()) == ["App start", "App end"]


def test_get_block_starts(test_resources: pathlib.Path) -> None:
    lps = LogPatterns(test_resources / "test_patterns.yml")
    patterns = list(lps.get_block_starts())
    assert len(patterns) == 1
    assert patterns[0].name == "App start"


def test_get_names(test_resources: pathlib.Path) -> None:
    lps = LogPatterns(test_resources / "test_patterns.yml")
    names = list(lps.get_names())
    assert len(names) == 2
    assert names[0] == "App start"
    assert names[1] == "App end"
