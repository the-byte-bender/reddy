import wx
class Main(wx.Frame):
    def __init__(self, title: str = "Reddy", client_id: str = "", client_secret: str = "", user_agent: str = "reddy", db_path: str = ""):
        super().__init__(None, title = title)
        self.title: str = title
        self.client_id: str = client_id
        self.client_secret: str = client_secret
        self.user_agent: str = user_agent
        self.db_path: str = db_path
        self.pannel: wx.Panel = wx.Panel(self)
        self.main_sizer: wx.BoxSizer = wx.BoxSizer()
        self.temp: wx.TextCtrl = wx.TextCtrl(self.pannel, style = wx.TE_DONTWRAP|wx.TE_READONLY)
        self.temp.SetValue("This is a test. You cannot do anything at the moment.")
        self.main_sizer.Add(self.temp, wx.EXPAND|wx.ALIGN_CENTER)
        self.pannel.SetSizer(self.main_sizer)