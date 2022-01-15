"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


from wx import stc


class LogDisplay(stc.StyledTextCtrl):

    """
    The log display
    """

    styles = {
        "bold": "bold",
        "italic": "italic",
        "red": "fore:#FF0000",
        "green": "fore:#00FF00",
        "blue": "fore:#0000FF",
    }

    def __init__(self, parent, log_group):
        super().__init__(parent, -1)
        self.log_group = log_group
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 50)
        base_style = "size:10,face:Courier New"
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, base_style)
        for i, pattern in enumerate(self.log_group.patterns.get_patterns()):
            p_style_list = [base_style] + [self.styles[p] for p in pattern.style]
            self.StyleSetSpec(i + 1, ",".join(p_style_list))
        self.SetText(self.log_group.get_text())
        for i, pattern in enumerate(self.log_group.patterns.get_patterns()):
            for line in pattern.lines:
                self.StartStyling(self.PositionFromLine(line))
                self.SetStyling(len(self.log_group.lines[line]), i + 1)
        self.GotoLine(0)
        self.SetCaretLineVisible(True)
        self.SetCaretLineVisibleAlways(True)

    def find_line(self, direction, pattern_num):
        """
        Find the previous or next line
        """
        pattern = self.log_group.patterns.patterns[pattern_num]
        act_line = self.GetCurrentLine()
        next_line = act_line
        if direction == ">":
            for line in pattern.lines:
                if line > act_line:
                    next_line = line
                    break
        else:
            prev = -1
            for line in pattern.lines:
                if line >= act_line:
                    break
                prev = line
            if prev > -1:
                next_line = prev
        self.GotoLine(next_line)
