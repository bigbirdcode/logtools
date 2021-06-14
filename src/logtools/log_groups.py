"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


from .log_group import LogGroup


class LogGroups:

    """
    Collection of log groups
    """

    def __init__(self, log_data):
        self.log_data = log_data
        self.groups = []
        self.act = LogGroup(self.log_data, num=len(self.groups) + 1)

    def new_group(self, name):
        """
        Start a new group
        """
        self.act.finalize()
        if self.act.lines:
            # do not add empty
            self.groups.append(self.act)
        self.act = LogGroup(self.log_data, num=len(self.groups) + 1, name=name)

    def add_line(self, line):
        """
        Add a new line to the actual group or start a new one when needed
        """
        for pattern in self.log_data.patterns.get_block_starts():
            if match := pattern.search(line, -1):
                self.new_group(match[1])
            break
        self.act.add(line)

    def finalize(self):
        """
        Finalize the collection of log groups
        In fact same actions as creating new group,
        new self.act will be there, but don't hurt anything
        """
        self.new_group("")
