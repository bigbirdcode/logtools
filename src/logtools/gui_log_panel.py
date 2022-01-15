"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


import wx
from wx.lib.agw import aui

from logtools.gui_log_display import LogDisplay


class LogPanel(wx.Panel):

    """
    Tabbed panel to display the log displays
    """

    def __init__(self, parent, log_data):
        super().__init__(parent, -1)

        self.log_data = log_data

        self.anb = aui.AuiNotebook(self)

        for log_group in self.log_data.log_groups.groups:
            page = LogDisplay(self.anb, log_group)
            self.anb.AddPage(page, log_group.name)

        self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CHANGING, self.on_anb_change, self.anb)

        sizer = wx.BoxSizer()
        sizer.Add(self.anb, 1, wx.EXPAND)
        self.SetSizer(sizer)
        wx.CallAfter(self.anb.SendSizeEvent)

    def on_anb_change(self, event):
        """
        Handle tab selection change
        """
        text = self.anb.GetPageText(event.GetSelection())
        num = int(text[0:2]) - 1
        self.log_data.set_group(num)
        search_terms = self.GetParent().search_terms
        search_terms.update()
        log_prop = self.GetParent().log_prop
        log_prop.SetValue(self.log_data.log_group.get_props())
        event.Skip()

    def find_line(self, direction, pattern_num):
        """
        Find line command is forwarded to the actual log displayed
        """
        self.anb.GetCurrentPage().find_line(direction, pattern_num)
