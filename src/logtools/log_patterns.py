"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import pathlib
from collections.abc import Iterator

import strictyaml as sy

from logtools.log_pattern import LogPattern, create_empty_pattern
from logtools.utils import LogToolsError


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
    for i, (k, v) in enumerate(input_data.items()):
        try:
            pattern = LogPattern(k, str(i), v)
        except Exception as exc:
            raise LogToolsError("Parse error at " + str(k)) from exc
        else:
            result.append(pattern)
    return result


class LogPatterns:
    """
    Class to hold a list of log pattern objects for a log
    """

    def __init__(self, file_path: pathlib.Path) -> None:
        self.file_path = file_path
        self.data = parse_yaml(file_path.read_text())
        self.free_search = create_empty_pattern()
        self.free_search.p_id = "free"
        self.free_search.name = "Free search"
        self.free_search.style = ["bold"]

    def write_yaml(self) -> None:
        """
        Write out the patterns to a new yaml file, backup the previous one
        """
        self.file_path.replace(self.file_path.with_suffix(".bkp"))
        result = {pattern.name: pattern.get_data() for pattern in self.data}
        self.file_path.write_text(sy.as_document(result, SCHEMA).as_yaml())

    def get_all_patterns(self) -> Iterator[LogPattern]:
        """
        Get all the patterns
        """
        yield from self.data
        yield self.free_search

    def get_yaml_patterns(self) -> Iterator[LogPattern]:
        """
        Get the patterns defined in the yaml user file
        """
        yield from self.data

    def get_pattern(self, p_id: str) -> LogPattern | None:
        """
        Get a pattern by index number or the name for the free text search
        """
        if p_id == "free":
            return self.free_search
        try:
            return self.data[int(p_id)]
        except (IndexError, ValueError):
            return None

    def get_next_p_id(self) -> str:
        """
        Get the next pattern id
        """
        return str(len(self.data))

    def add_pattern(self, pattern: LogPattern) -> None:
        """
        Add a new pattern to the list
        """
        p_id = str(len(self.data))
        if pattern.p_id:
            assert pattern.p_id == p_id
        else:
            pattern.p_id = p_id
        self.data.append(pattern)

    def update_pattern(self, pattern: LogPattern) -> None:
        """
        Update a pattern in the list
        """
        self.data[int(pattern.p_id)] = pattern

    def get_block_starts(self) -> Iterator[LogPattern]:
        """
        Get the patterns that can start a new log group
        """
        for pattern in self.data:
            if pattern.block_start:
                yield pattern

    def get_modified(self) -> Iterator[LogPattern]:
        """
        Get all the patterns
        """
        for pattern in self.data:
            if pattern.modified:
                yield pattern

    def get_names(self) -> Iterator[str]:
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
