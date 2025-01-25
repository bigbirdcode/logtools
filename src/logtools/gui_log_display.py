"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

from typing import Any

from wx import stc

from logtools.log_block import LogBlock


def translate_style(style_in: str) -> str:
    """
    Change the given style to the STC format
    """
    if style_in in ("bold", "italic", "underline"):
        return style_in
    return f"fore:#{style_in}"  # color


# mypy: allow-subclassing-any
class LogDisplay(stc.StyledTextCtrl):
    """
    The log display that is in the tabbed pages of the GUI
    """

    def __init__(self, parent: Any, log_block: LogBlock) -> None:
        super().__init__(parent, -1)
        self.log_block = log_block
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 50)
        self.SetWrapMode(1)
        self.base_style = "size:10,face:Courier New"
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, self.base_style)
        self.create_pattern_styles()
        self.SetText(self.log_block.get_text())
        self.apply_pattern_styles()
        self.GotoLine(0)
        self.SetCaretLineVisible(True)
        self.SetCaretLineVisibleAlways(True)

    def create_pattern_styles(self) -> None:
        """
        Create styles from the pattern details
        Styles are referenced by numbers, starting from 1
        """
        self.StyleClearAll()
        for i, pattern in enumerate(self.log_block.patterns, stc.STC_STYLE_LASTPREDEFINED + 1):
            if i > stc.STC_STYLE_MAX:
                err_msg = "Too many patterns"
                raise ValueError(err_msg)
            pattern.style_num = i
            p_style_list = [self.base_style] + [translate_style(p) for p in pattern.style]
            p_style = ",".join(p_style_list)
            self.StyleSetSpec(i, p_style)

    def apply_pattern_styles(self) -> None:
        """
        Apply the pattern style information to the log lines
        """
        self.ClearDocumentStyle()
        for pattern in self.log_block.patterns:
            for line in self.log_block.pattern_lines[pattern.name]:
                self.StartStyling(self.PositionFromLine(line))
                self.SetStyling(len(self.log_block.lines[line]), pattern.style_num)

    def update(self) -> None:
        """
        When a pattern changes find the new lines and apply styles

        Note: currently everything is processed, later it will check modified states
        """
        self.log_block.search_patterns()
        self.create_pattern_styles()
        self.apply_pattern_styles()

    def find_line(self, direction: str, pattern_num: int) -> None:
        """
        Find the previous or next line
        """
        pattern = self.log_block.patterns[pattern_num]
        act_line = self.GetCurrentLine()
        next_line = act_line
        if direction == ">":
            for line in self.log_block.pattern_lines[pattern.name]:
                if line > act_line:
                    next_line = line
                    break
        else:
            prev = -1
            for line in self.log_block.pattern_lines[pattern.name]:
                if line >= act_line:
                    break
                prev = line
            if prev > -1:
                next_line = prev
        self.GotoLine(next_line)
