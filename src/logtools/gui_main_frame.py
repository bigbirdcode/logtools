"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


import wx
from wx.lib.agw import aui

from logtools.gui_log_panel import LogPanel
from logtools.gui_search_panel import SearchPanel


class MainFrame(wx.Frame):  # pylint: disable=too-many-ancestors

    """
    Frame with AUI manager to manage tabs easily
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent,
        log_data,
        id=-1,  # pylint: disable=redefined-builtin
        title="AUI Test",
        pos=wx.DefaultPosition,
        size=(800, 600),
        style=wx.DEFAULT_FRAME_STYLE,
    ):

        wx.Frame.__init__(self, parent, id, title, pos, size, style)

        self.log_data = log_data

        self._mgr = aui.AuiManager()

        # notify AUI which frame to use
        self._mgr.SetManagedWindow(self)

        # create several panes
        self.search_terms = SearchPanel(self, self.log_data)

        self.log_prop = wx.TextCtrl(
            self,
            -1,
            "",
            wx.DefaultPosition,
            wx.Size(200, 150),
            wx.NO_BORDER | wx.TE_MULTILINE,
        )
        self.log_prop.SetValue(self.log_data.log_groups.groups[0].get_props())

        self.log_panel = LogPanel(self, self.log_data)

        # add the panes to the manager
        self._mgr.AddPane(self.search_terms, aui.AuiPaneInfo().Left().Caption("Search Terms"))
        self._mgr.AddPane(
            self.log_prop, aui.AuiPaneInfo().Left().Caption("Selected Panel Properties")
        )
        self._mgr.AddPane(self.log_panel, aui.AuiPaneInfo().CenterPane())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        self.Maximize(True)

    def OnClose(self, event):  # pylint: disable=invalid-name
        """
        Close the frame manager
        """
        self._mgr.UnInit()
        event.Skip()
