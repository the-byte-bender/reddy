import wx

class LabeledTextbox(wx.Panel):
    def __init__(self, parrent: wx.Window, label_text: str, initial_value: str = "", label_style: int = wx.ALIGN_CENTER_HORIZONTAL, textctrl_style: int = wx.TE_DONTWRAP):
        """
        It creates a panel with a label and a textctrl
        
        @param parrent
        @param label_text The text to display in the label.
        @param initial_value The initial value of the textctrl.
        @param label_style wx.ALIGN_CENTER_HORIZONTAL
        @param textctrl_style wx.TE_DONTWRAP
        """
        super().__init__(parrent)
        self.sizer: wx.BoxSizer = wx.BoxSizer()
        self.label: wx.StaticText = wx.StaticText(self, label = label_text, style = label_style)
        self.sizer.Add(self.label, 1, wx.ALIGN_LEFT|wx.EXPAND)
        self.textctrl: wx.TextCtrl = wx.TextCtrl(self, value  = initial_value, style = textctrl_style)
        self.sizer.Add(self.textctrl, 1, wx.ALIGN_LEFT|wx.EXPAND)
        self.SetAutoLayout(True)
        self.SetSizerAndFit(self.sizer)