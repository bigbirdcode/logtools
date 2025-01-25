"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import pathlib
from collections import UserList

import strictyaml as sy

from logtools.log_pattern import LogPattern


# yaml patterns are read according to this schema
# nearly all field processed runtime, but when block_start changes
# then the application need to be restarted
SCHEMA = sy.MapPattern(
    sy.Str(),  # name of the pattern
    sy.Map(
        {
            "pattern": sy.Str(),  # regexp string to search
            "block_start": sy.Bool(),  # indication of a new bog block
            "needed": sy.Bool(),  # when missing consider as crash
            "property": sy.Str(),  # extract value from the regexp
            "style": sy.Seq(sy.Regex(r"bold|italic|underline|[0-9A-F]{6}")),  # style and color
            "visible": sy.Bool(),  # display the line or not
        }
    ),
)


def parse_yaml(text: str) -> list[LogPattern]:
    """
    Parse yaml input into a list of log pattern objects
    """
    result: list[LogPattern] = []
    input_data = sy.load(text, SCHEMA).data
    for k, v in input_data.items():
        try:
            pattern = LogPattern(k, v)
        except Exception as exc:
            raise RuntimeError("Parse error at " + str(k)) from exc
        else:
            result.append(pattern)
    return result


class LogPatterns(UserList):
    """
    Class to hold a list of log pattern objects for a log
    """

    def __init__(self, file_path: pathlib.Path) -> None:
        super().__init__()
        self.file_path = file_path
        self.data = parse_yaml(file_path.read_text())

    def write_yaml(self) -> None:
        """
        Write out the patterns to a new yaml file, backup the previous one
        """
        self.file_path.replace(self.file_path.with_suffix(".bkp"))
        result = {pattern.name: pattern.get_data() for pattern in self.data}
        self.file_path.write_text(sy.as_document(result, SCHEMA).as_yaml())

    def get_block_starts(self):
        """
        Get the patterns that can start a new log group
        """
        for pattern in self.data:
            if pattern.block_start:
                yield pattern

    def get_modified(self):
        """
        Get all the patterns
        """
        for pattern in self.data:
            if pattern.modified:
                yield pattern

    def get_names(self):
        """
        Get all the pattern names
        """
        for pattern in self.data:
            yield pattern.name

    def clear_modified(self) -> None:
        """
        Clear all modified flags
        """
        for pattern in self.data:
            pattern.modified = False
