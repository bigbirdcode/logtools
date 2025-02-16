"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

from typing import Any

import wx
from wx.lib.agw import aui

from logtools.gui_log_display import LogDisplay
from logtools.log_data import LogData


# mypy: allow-subclassing-any
class LogDisplays(wx.Panel):
    """
    Tabbed panel to display the log displays
    """

    def __init__(self, parent: Any, app_data: LogData) -> None:
        super().__init__(parent, -1)

        self.app_data = app_data
        self.log_displays = []

        self.anb = aui.AuiNotebook(self)

        for log_block in self.app_data.log_blocks:
            display = LogDisplay(self.anb, log_block)
            self.log_displays.append(display)
            self.anb.AddPage(display, log_block.name)

        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.on_anb_change, self.anb)

        sizer = wx.BoxSizer()
        sizer.Add(self.anb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.anb.SendSizeEvent)

    def on_anb_change(self, event: Any) -> None:
        """
        Handle tab selection change
        """
        text = self.anb.GetPageText(event.GetSelection())
        num = int(text[0:2]) - 1
        self.app_data.set_block(num)
        self.GetParent().search_panel.update()
        log_prop = self.GetParent().search_panel.log_prop
        log_prop.SetValue(self.app_data.log_block.get_props())
        event.Skip()

    def find_line(self, direction: str, p_id: int) -> None:
        """
        Find line command is forwarded to the actual log displayed
        """
        self.anb.GetCurrentPage().find_line(direction, p_id)

    def update(self) -> None:
        """
        Propagate update event to all displays
        """
        for page in self.log_displays:
            page.update()
        self.app_data.patterns.clear_modified()
