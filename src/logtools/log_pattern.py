"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


import re
from typing import Dict, Any


class LogPattern:

    """
    A log pattern attached to a log, holding also the line references
    """

    def __init__(self, name, pattern_data: Dict[str, Any]) -> None:
        # Required attributes
        self.name = name
        self.raw_pattern = pattern_data["pattern"]
        self.pattern = re.compile(self.raw_pattern)
        self.block_start = pattern_data["block_start"]
        self.needed = pattern_data["needed"]
        self.property = pattern_data["property"]
        self.style = pattern_data["style"]
        self.visible = pattern_data["visible"]
        # Generated attributes
        self.count = 0
        self.lines = []

    def search(self, line, line_num):
        """
        Search the pattern as regex, store the number, return match
        """
        match = self.pattern.search(line)
        if match:
            self.lines.append(line_num)
        return match

    def has_line(self, line_num):
        """
        Check that line is in the found and stored lines
        """
        return line_num in self.lines

    def get_data(self):
        """
        Build back a dict to copy data
        """
        pattern_data = {
            "pattern": self.raw_pattern,
            "block_start": self.block_start,
            "needed": self.needed,
            "property": self.property,
            "style": self.style,
            "visible": self.visible,
        }
        return self.name, pattern_data

    def name_and_num(self):
        """
        Return a sting with name and found number to display
        """
        return f"{self.name} : {len(self.lines)}"

    def get_clean_copy(self):
        """
        Create a copy of self without the line data
        """
        name, pattern_data = self.get_data()
        return LogPattern(name, pattern_data)
