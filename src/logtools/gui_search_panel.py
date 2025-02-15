"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

from typing import Any

import wx

from logtools.gui_pattern_edit import PatternEditDialog
from logtools.log_data import LogData
from logtools.log_pattern import create_empty_pattern


# mypy: allow-subclassing-any
class SearchPanel(wx.ScrolledWindow):
    """
    Panel that will show the search patterns to quickly reach them
    """

    def __init__(self, parent: Any, app_data: LogData) -> None:
        super().__init__(parent, -1, style=wx.VSCROLL | wx.ALWAYS_SHOW_SB)
        self.app_data = app_data
        self.texts: list[wx.TextCtrl] = []

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Properties")
        font = label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        self.sizer.Add(label, 0, wx.EXPAND)

        self.log_prop = wx.TextCtrl(
            self,
            -1,
            "",
            wx.DefaultPosition,
            wx.Size(200, 150),
            wx.NO_BORDER | wx.TE_MULTILINE,
        )
        self.log_prop.SetValue(self.app_data.log_block.get_props())
        self.sizer.Add(self.log_prop, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "Searches")
        label.SetFont(font)
        self.sizer.Add(label, 0, wx.EXPAND)

        for i, pattern in enumerate(self.app_data.patterns):
            num_name = str(i)
            sub_sizer = self.create_pattern_row(num_name, pattern.name)
            self.sizer.Add(sub_sizer, 0, wx.EXPAND)

        sub_sizer = self.create_pattern_row(str(len(self.app_data.patterns)), "<add new>")
        self.sizer.Add(sub_sizer, 0, wx.EXPAND)

        self.update()
        self.SetSizer(self.sizer)
        self.SetVirtualSize(self.sizer.GetMinSize())
        self.SetScrollRate(0, 20)
        self.FitInside()

    def create_pattern_row(self, num_name: str, name: str) -> Any:
        """
        Create a row to display pattern name, number and controls
        """
        sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.TextCtrl(
            self,
            -1,
            name,
            style=wx.TE_READONLY,
            size=(200, -1),
            name=num_name,
        )
        text.SetMinSize((20, -1))
        text.Bind(wx.EVT_LEFT_DOWN, self.on_click_edit)
        self.texts.append(text)
        btn_prev = wx.Button(self, -1, "<", size=(25, 25), name="<" + num_name)
        btn_next = wx.Button(self, -1, ">", size=(25, 25), name=">" + num_name)
        self.Bind(wx.EVT_BUTTON, self.on_click_search, btn_prev)
        self.Bind(wx.EVT_BUTTON, self.on_click_search, btn_next)
        sub_sizer.Add(text, 1, wx.EXPAND)
        sub_sizer.Add(btn_prev, 0, wx.CENTER)
        sub_sizer.Add(btn_next, 0, wx.CENTER)
        return sub_sizer

    def update(self) -> None:
        """
        Update pattern texts names with the found line numbers for the selected log
        """
        for i, pattern in enumerate(self.app_data.log_block.patterns):
            num = len(self.app_data.log_block.pattern_lines[pattern.name])
            name = f"{pattern.name}: {num}"
            self.texts[i].SetValue(name)

    def on_click_search(self, event: Any) -> None:
        """
        Handle search prev or next clicks
        """
        obj_name = event.GetEventObject().GetName()
        direction = obj_name[0]
        pattern_num = int(obj_name[1:])
        if pattern_num < len(self.app_data.patterns):
            self.GetParent().log_panel.find_line(direction, pattern_num)
        event.Skip()

    def on_click_edit(self, event: Any) -> None:
        """
        Handle pattern edit clicks
        """
        obj_name = event.GetEventObject().GetName()
        pattern_num = int(obj_name)
        new_pattern = len(self.app_data.patterns) == pattern_num
        if new_pattern:
            pattern = create_empty_pattern()
        else:
            pattern = self.app_data.patterns[pattern_num]
        dlg = PatternEditDialog(self, pattern)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            pattern = dlg.get_pattern()
            if new_pattern:
                self.app_data.patterns.append(pattern)
                sub_sizer = self.create_pattern_row(str(len(self.app_data.patterns)), "<add new>")
                self.sizer.Add(sub_sizer, 0, wx.EXPAND)
                self.SetVirtualSize(self.sizer.GetMinSize())
                self.FitInside()
            else:
                self.app_data.patterns[pattern_num] = pattern
            self.GetParent().log_panel.update()
            self.update()
            self.app_data.yaml_modified = True
        dlg.Destroy()
