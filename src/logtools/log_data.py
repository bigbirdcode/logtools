"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


from __future__ import annotations

import pathlib

from .log_blocks import LogBlocks
from .log_patterns import LogPatterns


class LogData:

    """
    Parent class for the data, components will reach the data through this
    """

    def __init__(self, patterns: LogPatterns, log_files: list[pathlib.Path]) -> None:
        self.patterns = patterns
        self.log_blocks = LogBlocks(patterns)
        for log_file in sorted(log_files, key=lambda path: path.stat().st_mtime):
            txt = log_file.read_text(encoding="latin2")
            for line in txt.splitlines():
                self.log_blocks.add_line(line)
        self.log_blocks.finalize()
        self.log_block = self.log_blocks[0]
        self.yaml_modified = False

    def set_block(self, num: int) -> None:
        """
        Set a shortcut to the actual selected log
        """
        self.log_block = self.log_blocks[num]
