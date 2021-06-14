"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


from __future__ import annotations

from typing import Optional, List, Any

import strictyaml as sy

from .log_pattern import LogPattern


# yaml patterns are read according to this schema
SCHEMA = sy.Seq(
    sy.MapPattern(
        sy.Str(),
        sy.Map(
            {
                "pattern": sy.Str(),
                "block_start": sy.Bool(),
                "needed": sy.Bool(),
                "property": sy.Str(),
                "style": sy.Seq(sy.Str()),
                "visible": sy.Bool(),
            }
        ),
    )
)


def parse_pattern(input_pattern: Any) -> LogPattern:
    """
    Convert a yaml pattern definition to log pattern object
    """
    assert len(input_pattern) == 1
    name, data = input_pattern.popitem()
    return LogPattern(name, data)


def parse_yml(text: str) -> List[LogPattern]:
    """
    Parse yaml input into a list of log pattern objects
    """
    result: list[LogPattern] = []
    input_data = sy.load(text, SCHEMA).data
    for input_pattern in input_data:
        try:
            pattern = parse_pattern(input_pattern)
        except Exception as exc:
            raise RuntimeError("Parse error at " + str(input_pattern)) from exc
        else:
            result.append(pattern)
    return result


def read_yml(file_name: str) -> str:
    """
    Just read in a file
    """
    with open(file_name) as f:
        return f.read()


class LogPatterns:

    """
    Class to hold a list of log pattern objects for a log
    """

    def __init__(
        self, file_name: str = "patterns.yml", patterns: Optional[LogPatterns] = None
    ) -> None:
        self.patterns: list[LogPattern]
        if patterns is None:
            self.patterns = parse_yml(read_yml(file_name))
        else:
            self.patterns = [
                pattern.get_clean_copy() for pattern in patterns.get_patterns()
            ]

    def get_block_starts(self):
        """
        Get the patterns that can start a new log group
        """
        for pattern in self.patterns:
            if pattern.block_start:
                yield pattern

    def get_patterns(self):
        """
        Get all the patterns
        """
        for pattern in self.patterns:
            yield pattern

    def get_names(self):
        """
        Get all the pattern names
        """
        for pattern in self.patterns:
            yield pattern.name

    def get_line_pattern(self, line_num):
        """
        Get the pattern that matched a log line
        """
        for pattern in self.patterns:
            if pattern.has_line(line_num):
                return pattern
        return None

    def get_clean_copy(self):
        """
        Create a copy of self without the line data
        """
        return LogPatterns("", self)
