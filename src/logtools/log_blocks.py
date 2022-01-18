"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


from __future__ import annotations

from collections import UserList

from .log_block import LogBlock
from .log_patterns import LogPatterns


class LogBlocks(UserList):

    """
    Collection of log blocks
    """

    def __init__(self, patterns: LogPatterns) -> None:
        super().__init__()
        self.patterns = patterns
        self.act = LogBlock(self.patterns, num=1)

    def new_block(self, name: str) -> None:
        """
        Start a new block
        """
        self.finalize()
        self.act = LogBlock(self.patterns, num=len(self.data) + 1, name=name)

    def add_line(self, line: str) -> None:
        """
        Add a new line to the actual block or start a new one when needed
        """
        for pattern in self.patterns.get_block_starts():
            if match := pattern.search(line):
                self.new_block(match[1])
            break
        self.act.add(line)

    def finalize(self) -> None:
        """
        Finalize the collection of the actual block
        """
        self.act.finalize()
        if self.act.lines:
            # do not add empty
            self.data.append(self.act)
