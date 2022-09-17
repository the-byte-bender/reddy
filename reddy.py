import os
import wx
from libs.ui import main

app = wx.App()
window: wx.Frame = main.Main(
    title="Reddy",
    client_id=os.getenv("REDDY_CLIENT_ID") or "",
    client_secret=os.getenv("REDDY_CLIENT_SECRET") or "",
    user_agent=os.getenv("REDDY_USER_AGENT") or "reddy",
    db_path=os.getenv("REDDY_DB_PATH") or "",
)
window.Show()
app.MainLoop()
