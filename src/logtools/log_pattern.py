"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import re
from typing import Any, Optional


class LogPattern:
    """
    A log pattern attached to a log, holding also the line references
    """

    def __init__(self, name: str, pattern_data: dict[str, Any]) -> None:
        # Required attributes
        self.name = name
        self.raw_pattern = pattern_data["pattern"]
        self.pattern = re.compile(self.raw_pattern)
        self.block_start = pattern_data["block_start"]
        self.needed = pattern_data["needed"]
        self.property = pattern_data["property"]
        self.style = pattern_data["style"]
        self.visible = pattern_data["visible"]
        self.modified = False
        # Will be assigned by the display
        self.style_num = -1

    def search(self, line: str) -> Optional[re.Match]:
        """
        Search the pattern as regex, return match
        """
        match = self.pattern.search(line)
        return match

    def get_data(self) -> dict[str, Any]:
        """
        Build back a dict of the pattern details
        """
        pattern_data = {
            "pattern": self.raw_pattern,
            "block_start": self.block_start,
            "needed": self.needed,
            "property": self.property,
            "style": self.style,
            "visible": self.visible,
        }
        return pattern_data


def create_empty_pattern() -> LogPattern:
    """
    Create an empty pattern object that can be filled later
    """
    pattern_data = {
        "pattern": "",
        "block_start": False,
        "needed": False,
        "property": "",
        "style": [],
        "visible": True,
    }
    return LogPattern("", pattern_data)
