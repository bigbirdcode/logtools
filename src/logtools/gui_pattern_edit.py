"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


from __future__ import annotations

from typing import Any

import wx
import wx.lib.sized_controls as sc
import wx.lib.colourselect as csel

from .log_pattern import LogPattern


def color_to_wx(color: str) -> Any:
    """
    Translate color from the hex representation to the wx representation
    """
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    return wx.Colour(r, g, b)


class PatternEditDialog(sc.SizedDialog):  # pylint: disable=too-many-ancestors

    """Dialog to edit a pattern"""

    def __init__(self, parent: Any, pattern: LogPattern) -> None:

        sc.SizedDialog.__init__(
            self, parent, -1, "Edit Pattern", style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        )

        pane = self.GetContentsPane()
        pane.SetSizerType("form")

        wx.StaticText(pane, -1, "Name:")
        self.p_name = wx.TextCtrl(pane, -1, pattern.name)
        self.p_name.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, "Pattern:")
        self.p_pattern = wx.TextCtrl(pane, -1, pattern.raw_pattern, size=(300, -1))
        self.p_pattern.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, "Block start:")
        self.p_block_start = wx.CheckBox(pane, -1)
        self.p_block_start.SetValue(pattern.block_start)

        wx.StaticText(pane, -1, "Needed:")
        self.p_needed = wx.CheckBox(pane, -1)
        self.p_needed.SetValue(pattern.needed)

        wx.StaticText(pane, -1, "Property:")
        self.p_property = wx.TextCtrl(pane, -1, pattern.property)
        self.p_property.SetSizerProps(expand=True)

        wx.StaticText(pane, -1, "Style:")
        wx.StaticText(pane, -1, "")

        wx.StaticText(pane, -1, "Bold:")
        self.p_s_bold = wx.CheckBox(pane, -1)
        self.p_s_bold.SetValue("bold" in pattern.style)

        wx.StaticText(pane, -1, "Italic:")
        self.p_s_italic = wx.CheckBox(pane, -1)
        self.p_s_italic.SetValue("italic" in pattern.style)

        wx.StaticText(pane, -1, "Underline:")
        self.p_s_under = wx.CheckBox(pane, -1)
        self.p_s_under.SetValue("underline" in pattern.style)

        wx.StaticText(pane, -1, "Color:")
        colors = [s for s in pattern.style if s not in ("bold", "italic", "underline")]
        assert len(colors) <= 1
        self.color = "000000" if not colors else colors[0]
        self.p_s_color = csel.ColourSelect(pane, -1, "Choose...", color_to_wx(self.color))
        self.p_s_color.Bind(csel.EVT_COLOURSELECT, self.on_select_color)

        wx.StaticText(pane, -1, "Visible:")
        self.p_visible = wx.CheckBox(pane, -1)
        self.p_visible.SetValue(pattern.visible)

        # add dialog buttons
        self.SetButtonSizer(self.CreateStdDialogButtonSizer(wx.OK | wx.CANCEL))

        self.Fit()

    def on_select_color(self, event: Any) -> None:
        """
        Handle color selection
        """
        c = event.GetValue()
        self.color = c.GetAsString(wx.C2S_HTML_SYNTAX)[1:]
        event.Skip()

    def get_pattern(self) -> LogPattern:
        """
        Get the pattern data set by the user as a new pattern

        It will have modified state
        """
        pattern_name = self.p_name.GetValue()
        pattern_data = {
            "pattern": self.p_pattern.GetValue(),
            "block_start": self.p_block_start.GetValue(),
            "needed": self.p_needed.GetValue(),
            "property": self.p_property.GetValue(),
            "style": [],
            "visible": self.p_visible.GetValue(),
        }
        if self.p_s_bold.GetValue():
            pattern_data["style"].append("bold")
        if self.p_s_italic.GetValue():
            pattern_data["style"].append("italic")
        if self.p_s_under.GetValue():
            pattern_data["style"].append("underline")
        if self.color != "000000":
            pattern_data["style"].append(self.color)
        pattern = LogPattern(pattern_name, pattern_data)
        pattern.modified = True
        return pattern
