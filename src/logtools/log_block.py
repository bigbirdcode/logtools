"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


from __future__ import annotations

import datetime
import re

from .log_pattern import LogPattern
from .log_patterns import LogPatterns

TIMESTAMP_FORMAT = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}")


def extract_timestamp(line: str) -> str:
    """
    Try to get a timestamp from the line. Return empty string when not found.
    """
    parts = line.split()
    try:
        time_stamp = parts[1]
    except IndexError:
        return ""
    if TIMESTAMP_FORMAT.match(time_stamp):
        return time_stamp
    return ""


def calculate_delta(start: str, end: str) -> str:
    """
    Calculate the time difference in hh:mm:ss format
    """
    result = ""
    try:
        delta = datetime.datetime.fromisoformat(end) - datetime.datetime.fromisoformat(start)
    except ValueError:
        return result
    seconds = delta.total_seconds() % 60
    minutes = int((delta.total_seconds() // 60) % 60)
    hours = int((delta.total_seconds() // 3600))
    return f"{hours:0>2d}:{minutes:0>2d}:{seconds:0>6.3f}"

class LogBlock:

    """
    A log group, i.e. lines of log that belong to an execution
    These groups are separated by lines matched by starting patterns
    """

    def __init__(self, patterns: LogPatterns, num: int = 0, name: str = "") -> None:
        self.patterns = patterns
        self.num = num
        self.name = name if name else "unknown"
        self.has_needed = False
        self.start = ""
        self.end = ""
        self.duration = ""
        self.props = [f"Name: {self.name}"]
        self.lines = []
        self.pattern_lines = {pattern.name: [] for pattern in self.patterns}

    def add(self, line: str) -> None:
        """
        Add a line
        """
        self.lines.append(line)

    def get_first_timestamp(self) -> str:
        """
        Get the first valid timestamp from the log lines
        """
        for line in self.lines:
            if time_stamp := extract_timestamp(line):
                return time_stamp
        return ""

    def get_last_timestamp(self) -> str:
        """
        Get the last valid timestamp from the log lines
        """
        for line in reversed(self.lines):
            if time_stamp := extract_timestamp(line):
                return time_stamp
        return ""

    def finalize(self) -> None:
        """
        Close this group, collect data
        """
        if not self.lines:
            return
        self.start = self.get_first_timestamp()
        self.end = self.get_last_timestamp()
        self.duration = calculate_delta(self.start, self.end)
        self.search_patterns()
        self.has_needed = self.check_needed()
        suffix = "OK" if self.has_needed else "Crash"
        self.props.append(f"Start: {self.start}")
        self.props.append(f"End: {self.end}")
        self.props.append(f"Duration: {self.duration}")
        self.props.append(f"Lines: {len(self.lines)}")
        self.props.append(f"Result: {suffix}")
        self.name = f"{self.num:0>2d} {self.name} {suffix}"

    def search_patterns(self) -> None:
        """
        Search the lines for all the patterns and record line numbers
        """
        for pattern in self.patterns:
            self.search_pattern(pattern)

    def search_pattern(self, pattern: LogPattern) -> None:
        """
        Search the lines for a pattern and record line numbers
        """
        lines = []
        for num, line in enumerate(self.lines):
            if pattern.search(line):
                lines.append(num)
        self.pattern_lines[pattern.name] = lines

    def check_needed(self) -> bool:
        """
        Check whether all the needed patterns were found or not
        """
        for pattern in self.patterns:
            if pattern.needed:
                if not self.pattern_lines[pattern.name]:
                    return False
        return True

    def get_text(self) -> str:
        """
        Return all lines to display
        """
        return "".join(self.lines)

    def get_props(self) -> str:
        """
        Return the collected data
        """
        return "\n".join(self.props)
