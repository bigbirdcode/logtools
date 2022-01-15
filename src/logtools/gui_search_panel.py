"""LogTools Log viewer application

By BigBird who like to Code
https://github.com/bigbirdcode/logtools
"""


import wx


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
        self.GetParent().log_panel.find_line(direction, pattern_num)
        event.Skip()
