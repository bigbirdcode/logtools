"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


class LogGroup:

    """
    A log group, i.e. lines of log that belong to an execution
    These groups are separated by lines matched by starting patterns
    """

    def __init__(self, log_data, num=0, name=""):
        self.log_data = log_data
        self.patterns = log_data.patterns.get_clean_copy()
        self.num = num
        self.name = name if name else "unknown"
        self.has_needed = False
        self.start = ""
        self.end = ""
        self.props = [f"Name: {self.name}"]
        self.lines = []
        self.count = 0

    def add(self, line):
        """
        Add and process a line
        """
        if not line.strip():
            return
        parts = line.split()
        try:
            time_stamp = parts[1]
        except IndexError:
            pass
        else:
            if self.start == "":
                self.start = time_stamp
            self.end = time_stamp

        for pattern in self.patterns.get_patterns():
            if pattern.search(line, self.count):
                if pattern.needed:
                    self.has_needed = True
        self.lines.append(line)
        self.count += 1

    def set_name(self, new_name):
        """
        Set the name of this group
        """
        self.name = new_name

    def finalize(self):
        """
        Close this group, collect data
        """
        suffix = "OK" if self.has_needed else "Crash"
        self.props.append(f"Start: {self.start}")
        self.props.append(f"End: {self.end}")
        self.props.append(f"Lines: {self.count}")
        self.props.append(f"Result: {suffix}")
        self.name = f"{self.num:0>2d} {self.name} {suffix}"

    def get_text(self):
        """
        Return all lines to display
        """
        return "".join(self.lines)

    def get_props(self):
        """
        Return the collected data
        """
        return "\n".join(self.props)
