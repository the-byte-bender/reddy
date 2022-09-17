import wx
from ..utils import labeled_widget


class Main(wx.Frame):
    def __init__(
        self,
        title: str = "Reddy",
        client_id: str = "",
        client_secret: str = "",
        user_agent: str = "reddy",
        db_path: str = "",
    ):
        super().__init__(None, title=title)
        self.title: str = title
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.user_agent: str = user_agent
        self.db_path: str = db_path
        self.panel: wx.Panel = wx.Panel(self)
        self.main_sizer: wx.BoxSizer = wx.BoxSizer()
        self.temp_label, self.temp, self.temp_sizer = labeled_widget(
            self.panel,
            "Come back later",
            wx.TextCtrl(
                self.panel,
                value="Nothing to do now, come back later when a feature or 2 is implemented!",
                style = wx.TE_READONLY|wx.TE_MULTILINE|wx.TE_DONTWRAP
            ),
        )
        self.main_sizer.Add(self.temp_sizer, flag=wx.EXPAND)
        self.temp_button = wx.Button(self.panel, label = "Close")
        self.temp_button.Bind(wx.EVT_BUTTON, lambda event: self.Close())
        self.main_sizer.Add(self.temp_button, flag = wx.ALIGN_BOTTOM)
        self.panel.SetSizer(self.main_sizer)
