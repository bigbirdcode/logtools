"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

# ruff: noqa: D103 -  Missing docstring in public function

import pathlib

from logtools import user_files


def test_direct_pattern_read(test_resources: pathlib.Path) -> None:
    p = user_files.get_patterns("test_patterns", [], test_resources)
    assert p.file_path.name == "test_patterns.yml"


def test_rule_match(test_resources: pathlib.Path) -> None:
    files = [pathlib.Path("a.yyy")]
    p = user_files.get_patterns(None, files, test_resources)
    assert p.file_path.name == "test_patterns_2.yml"
