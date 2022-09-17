import threading
import wx
import praw
import praw.util.token_manager
from .. import refresh_token
from ..utils import LabeledTextbox


class AuthorizeDialog(wx.Dialog):
    def __init__(
        self,
        parrent: wx.Window,
        reddit: praw.Reddit,
        db: praw.util.token_manager.SQLiteTokenManager,
    ):
        super().__init__(parrent, title="Authorize your Reddit account")
        self.reddit = reddit
        self.db = db
        self.success: bool = False
        self.main_panel: wx.Panel = wx.Panel(self)
        self.main_sizer: wx.BoxSizer = wx.BoxSizer()
        self.information: LabeledTextbox = LabeledTextbox(
            self.main_panel,
            "Information",
            "Please  authorize this app to access your account",
            textctrl_style=wx.TE_DONTWRAP | wx.TE_READONLY,
        )
        self.main_sizer.Add(self.information, proportion=1)

    def do_authorize(self):
        token = refresh_token.get_refresh_token(self.reddit)
        if isinstance(token, str):
            wx.CallAfter(self.db.register, token)
            wx.CallAfter(self.Close)
            self.success = True
        else:
            wx.CallAfter(
                self.information.textctrl.SetValue,
                "Unexpected error. Please restart the app",
            )

    def ShowModal(self):
        threading.Thread(target=self.do_authorize, daemon=True).start()
        super().ShowModal()
        return self.success