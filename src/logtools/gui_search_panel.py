"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

import re
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
        self.texts: dict[str, wx.TextCtrl] = {}

        self.sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, -1, "Patterns:")
        font = label.GetFont()
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        label.SetFont(font)
        self.sizer.Add(label, 0, wx.EXPAND)

        patterns_name = self.app_data.patterns.file_path.stem
        label = wx.StaticText(self, -1, f"    {patterns_name}")
        self.sizer.Add(label, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "Properties")
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

        label = wx.StaticText(self, -1, "Free search")
        label.SetFont(font)
        self.sizer.Add(label, 0, wx.EXPAND)

        pattern_row = self.create_pattern_row("free", "", free_search=True)
        self.sizer.Add(pattern_row, 0, wx.EXPAND)

        label = wx.StaticText(self, -1, "Searches")
        label.SetFont(font)
        self.sizer.Add(label, 0, wx.EXPAND)

        for pattern in self.app_data.patterns.get_yaml_patterns():
            pattern_row = self.create_pattern_row(pattern.p_id, pattern.name)
            self.sizer.Add(pattern_row, 0, wx.EXPAND)

        new_id = self.app_data.patterns.get_next_p_id()
        pattern_row = self.create_pattern_row(new_id, "<add new>")
        self.sizer.Add(pattern_row, 0, wx.EXPAND)

        self.update()
        self.SetSizer(self.sizer)
        self.SetVirtualSize(self.sizer.GetMinSize())
        self.SetScrollRate(0, 20)
        self.FitInside()

    def create_pattern_row(self, p_id: str, name: str, free_search: bool = False) -> Any:
        """
        Create a row to display pattern name, number and controls
        """
        sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
        text = wx.TextCtrl(
            self,
            -1,
            value=name,
            style=wx.TE_PROCESS_ENTER if free_search else wx.TE_READONLY,
            size=(200, -1),
            name=p_id,
        )
        text.SetMinSize((20, -1))
        if free_search:
            text.Bind(wx.EVT_TEXT_ENTER, self.on_enter_free_search)
        else:
            text.Bind(wx.EVT_LEFT_DOWN, self.on_click_edit)
        self.texts[p_id] = text
        btn_prev = wx.Button(self, -1, "<", size=(25, 25), name="<" + p_id)
        btn_next = wx.Button(self, -1, ">", size=(25, 25), name=">" + p_id)
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
        for pattern in self.app_data.log_block.patterns.get_yaml_patterns():
            num = len(self.app_data.log_block.pattern_lines[pattern.p_id])
            name = f"{pattern.name}: {num}"
            self.texts[pattern.p_id].SetValue(name)

    def on_click_search(self, event: Any) -> None:
        """
        Handle search prev or next clicks
        """
        obj_name = event.GetEventObject().GetName()
        direction = obj_name[0]
        p_id = obj_name[1:]
        self.GetParent().log_panel.find_line(direction, p_id)
        event.Skip()

    def on_click_edit(self, event: Any) -> None:
        """
        Handle pattern edit clicks
        """
        obj_name = event.GetEventObject().GetName()
        new_pattern = False
        pattern = self.app_data.patterns.get_pattern(obj_name)
        if pattern is None:
            new_pattern = True
            pattern = create_empty_pattern()
            pattern.p_id = obj_name
        dlg = PatternEditDialog(self, pattern)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            pattern = dlg.get_pattern()
            if new_pattern:
                self.app_data.patterns.add_pattern(pattern)
                sub_sizer = self.create_pattern_row(
                    self.app_data.patterns.get_next_p_id(), "<add new>"
                )
                self.sizer.Add(sub_sizer, 0, wx.EXPAND)
                self.SetVirtualSize(self.sizer.GetMinSize())
                self.FitInside()
            else:
                self.app_data.patterns.update_pattern(pattern)
            self.GetParent().log_panel.update()
            self.update()
            self.app_data.yaml_modified = True
        dlg.Destroy()

    def on_enter_free_search(self, event: Any) -> None:
        """
        Handle free search enter
        """
        raw_search = event.GetEventObject().GetValue()
        free_search = self.app_data.patterns.free_search
        free_search.raw_pattern = raw_search
        free_search.pattern = re.compile(raw_search)
        free_search.modified = True
        self.GetParent().log_panel.update()
        self.update()
