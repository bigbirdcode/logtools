"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


import fileinput
import os
import sys

import wx
import wx.lib.agw.aui as aui
import wx.stc as stc

# This file is the starting point of the Cliptools app.
# Python has 2 types of calls:
#  - direct call, like: python main.py
#  - package call, like: python -m cliptools
# Below quite ugly code will handle that
if __name__ == "__main__" and __package__ is None:
    # This was a direct call
    # package information is missing, and relative imports will fail
    # this hack imitates the package behavior and add outer dir to the path
    __package__ = "logtools"  # pylint: disable=redefined-builtin
    logtools_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if logtools_dir not in sys.path:
        sys.path.insert(0, logtools_dir)
    del logtools_dir  # clean up global name space

# Now relative import is ok
# pylint: disable=wrong-import-position
from .log_groups import LogGroups
from .log_patterns import LogPatterns


class MyFrame(wx.Frame):

    """
    Frame with AUI manager to manage tabs easily
    """

    def __init__(
        self,
        parent,
        log_data,
        id=-1,
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
        self._mgr.AddPane(
            self.search_terms, aui.AuiPaneInfo().Left().Caption("Search Terms")
        )
        self._mgr.AddPane(
            self.log_prop, aui.AuiPaneInfo().Left().Caption("Selected Panel Properties")
        )
        self._mgr.AddPane(self.log_panel, aui.AuiPaneInfo().CenterPane())

        # tell the manager to "commit" all the changes just made
        self._mgr.Update()

        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        """
        Deinitialize the frame manager
        """
        self._mgr.UnInit()
        event.Skip()


class SearchPanel(wx.Panel):

    """
    Panel that will show the search patterns to quickly reach them
    """

    def __init__(self, parent, log_data):
        super().__init__(parent, -1)
        self.log_data = log_data
        self.texts = []

        sizer = wx.BoxSizer(wx.VERTICAL)

        for i, pattern in enumerate(self.log_data.log_group.patterns.get_patterns()):
            num_name = str(i)
            sub_sizer = wx.BoxSizer(wx.HORIZONTAL)
            text = wx.TextCtrl(
                self,
                -1,
                pattern.name_and_num(),
                style=wx.TE_READONLY,
                size=(200, -1),
                name=num_name,
            )
            self.texts.append(text)
            btn_prev = wx.Button(self, -1, "<", size=(25, 25), name="<" + num_name)
            btn_next = wx.Button(self, -1, ">", size=(25, 25), name=">" + num_name)
            self.Bind(wx.EVT_BUTTON, self.on_click, btn_prev)
            self.Bind(wx.EVT_BUTTON, self.on_click, btn_next)
            sub_sizer.Add(text, 1, wx.EXPAND)
            sub_sizer.Add(btn_prev, 0, wx.CENTER)
            sub_sizer.Add(btn_next, 0, wx.CENTER)
            sizer.Add(sub_sizer, 0, wx.EXPAND)

        self.SetSizer(sizer)
        self.Fit()

    def update(self):
        """
        Update pattern texts with numbers for the selected log
        """
        for i, pattern in enumerate(self.log_data.log_group.patterns.get_patterns()):
            self.texts[i].SetValue(pattern.name_and_num())

    def on_click(self, event):
        """
        Handle search prev or next clicks
        """
        obj_name = event.GetEventObject().GetName()
        direction = obj_name[0]
        pattern_num = int(obj_name[1:])
        self.Parent.log_panel.find_line(direction, pattern_num)
        event.Skip()


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
        search_terms = self.Parent.search_terms
        search_terms.update()
        log_prop = self.Parent.log_prop
        log_prop.SetValue(self.log_data.log_group.get_props())
        event.Skip()

    def find_line(self, direction, pattern_num):
        """
        Find line command is forwarded to the actual log displayed
        """
        self.anb.GetCurrentPage().find_line(direction, pattern_num)


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


class LogData:

    """
    Parent class for the data, components will reach the data through this
    """

    def __init__(self):
        self.patterns = LogPatterns()
        self.log_groups = LogGroups(self)
        self.log_group = None

    def set_group(self, num):
        """
        Set a shortcut to the actual selected log
        """
        self.log_group = self.log_groups.groups[num]


def main():
    """
    Main function, starting point as usual
    """
    if len(sys.argv) < 2:
        print("Must have a filename")
        sys.exit(1)
    log_data = LogData()
    log_groups = log_data.log_groups
    for line in fileinput.input(openhook=fileinput.hook_encoded("latin2")):
        log_groups.add_line(line)
    log_groups.finalize()
    log_data.set_group(0)

    # Making GUI
    app = wx.App(0)
    frame = MyFrame(None, log_data)
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
