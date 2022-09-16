import wx
from libs.ui import main

app = wx.App()
window: wx.Frame = main.Main(title="Reddy")
window.Show()
app.MainLoop()
