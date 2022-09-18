import wx


class LabeledListCtrl(wx.Panel):
    def __init__(
        self,
        parrent: wx.Window,
        label_text: str,
        label_style: int = wx.ALIGN_CENTER_HORIZONTAL,
        listctrl_style: int = wx.LC_REPORT,
    ):
        """
        It creates a panel with a label and a listctrl

        @param parrent
        @param label_text The text to be displayed in the label.
        @param label_style wx.ALIGN_CENTER_HORIZONTAL
        @param listctrl_style This is the style of the listctrl.  The default is wx.LC_REPORT.  You can use any of the wx.ListCtrl styles.
        """
        super().__init__(parrent)
        self.sizer: wx.BoxSizer = wx.BoxSizer()
        self.label: wx.StaticText = wx.StaticText(
            self, label=label_text, style=label_style
        )
        self.sizer.Add(self.label, 1, wx.ALIGN_LEFT | wx.EXPAND)
        self.listctrl: wx.ListCtrl = wx.ListCtrl(self, style=listctrl_style)
        self.sizer.Add(self.textctrl, 1, wx.ALIGN_LEFT | wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)
