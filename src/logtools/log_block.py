"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

from datetime import datetime, timedelta

from logtools.log_pattern import LogPattern
from logtools.log_patterns import LogPatterns


LOG_LEVELS = {
    "DEBUG": "D",
    "INFO": "I",
    "WARN": "W",
    "ERROR": "E",
    "FATAL": "F",
}


def format_timedelta(delta: timedelta) -> str:
    """
    Format a timedelta object to a string in the format 'hh:mm:ss'.
    """
    total_seconds = int(delta.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"


def extract_datetime(line: str) -> datetime | None:
    """
    Try to get a timestamp from the line. Return empty string when not found.
    """
    parts = line.split()
    try:
        time_stamp = parts[1]
    except IndexError:
        return None
    try:
        return datetime.fromisoformat(time_stamp)
    except ValueError:
        return None


def calculate_delta(start: datetime | None, end: datetime | None) -> str:
    """
    Calculate the time difference in hh:mm:ss format
    """
    if start is None or end is None:
        return "unknown"
    try:
        delta = end - start
    except ValueError:
        return "unknown"
    return format_timedelta(delta)


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
        self.start: datetime | None = None
        self.end: datetime | None = None
        self.duration = ""
        self.props = [f"Name: {self.name}"]
        self.lines: list[str] = []
        self.pattern_lines: dict[str, list[int]] = {pattern.name: [] for pattern in self.patterns}

    def add(self, line: str) -> None:
        """
        Add a line
        """
        self.lines.append(line)

    def get_first_datetime(self) -> datetime | None:
        """
        Get the first valid datetime from the log lines
        """
        for line in self.lines:
            if d_t := extract_datetime(line):
                return d_t
        return None

    def get_last_datetime(self) -> datetime | None:
        """
        Get the last valid datetime from the log lines
        """
        for line in reversed(self.lines):
            if d_t := extract_datetime(line):
                return d_t
        return None

    def finalize(self) -> None:
        """
        Close this group, collect data
        """
        if not self.lines:
            return
        self.start = self.get_first_datetime()
        self.end = self.get_last_datetime()
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

    def alter_line(self, line: str) -> str:
        """
        Change how lines are displayed.

        At first change type to letter code and timestamp to delta
        """
        parts = line.split()
        if len(parts) < 2:
            return line
        try:
            parts[0] = LOG_LEVELS[parts[0]]
        except KeyError:
            return line
        if self.start is not None:
            try:
                delta = datetime.fromisoformat(parts[1]) - self.start
            except ValueError:
                return " ".join(parts)
            # str(delta) result something like '0:07:05.258000'
            parts[1] = str(delta)[:-3]
        return " ".join(parts)

    def get_text(self) -> str:
        """
        Return all lines to display
        """
        # this change will have a button on the UI later
        if False:
            return "\n".join(self.alter_line(line) for line in self.lines)
        return "\n".join(self.lines)

    def get_props(self) -> str:
        """
        Return the collected data
        """
        return "\n".join(self.props)
