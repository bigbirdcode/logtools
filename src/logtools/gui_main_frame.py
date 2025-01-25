"""
LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""

from __future__ import annotations

from typing import Any

import wx
from wx.lib.agw import aui

from logtools.gui_log_displays import LogDisplays
from logtools.gui_search_panel import SearchPanel
from logtools.log_data import LogData


# mypy: allow-subclassing-any
class MainFrame(wx.Frame):
    """
    Frame with AUI manager to manage tabs easily
    """

    def __init__(self, app_data: LogData) -> None:
        wx.Frame.__init__(
            self,
            parent=None,
            id=-1,
            title="Log Tools",
            pos=wx.DefaultPosition,
            size=(1200, 800),
            style=wx.DEFAULT_FRAME_STYLE,
        )

        self.app_data = app_data

        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        # create several panes
        self.search_panel = SearchPanel(self, self.app_data)

        self.log_prop = wx.TextCtrl(
            self,
            -1,
            "",
            wx.DefaultPosition,
            wx.Size(200, 150),
            wx.NO_BORDER | wx.TE_MULTILINE,
        )
        self.log_prop.SetValue(self.app_data.log_block.get_props())

        self.log_panel = LogDisplays(self, self.app_data)

        # add the panes to the manager
        self._mgr.AddPane(
            self.search_panel, aui.AuiPaneInfo().Left().Caption("Search Terms").CloseButton(False)
        )
        self._mgr.AddPane(
            self.log_prop,
            aui.AuiPaneInfo().Left().Caption("Selected Panel Properties").CloseButton(False),
        )
        self._mgr.AddPane(self.log_panel, aui.AuiPaneInfo().CenterPane())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.on_close)

        self.Maximize(True)

    def on_close(self, event: Any) -> None:
        """
        Close the frame manager
        """
        if self.app_data.yaml_modified:
            self.app_data.patterns.write_yaml()
        self._mgr.UnInit()
        event.Skip()
