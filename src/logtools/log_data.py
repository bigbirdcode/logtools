"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


import pathlib

from logtools.log_groups import LogGroups
from logtools.log_patterns import LogPatterns


class LogData:

    """
    Parent class for the data, components will reach the data through this
    """

    def __init__(self, log_patterns: LogPatterns, log_files: list[pathlib.Path]):
        self.patterns = log_patterns
        self.log_groups = LogGroups(self)
        for log_file in log_files:
            with log_file.open(encoding="latin2") as f:
                for line in f:
                    self.log_groups.add_line(line)
        self.log_groups.finalize()
        self.log_group = self.log_groups.groups[0]

    def set_group(self, num):
        """
        Set a shortcut to the actual selected log
        """
        self.log_group = self.log_groups.groups[num]
