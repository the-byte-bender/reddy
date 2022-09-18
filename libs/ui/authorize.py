import typing
import wx
import praw
import praw.util.token_manager
from .. import refresh_token, threadpool
from .utils import LabeledTextbox


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

    def do_authorize(self, token: typing.Optional[str]):
        if isinstance(token, str):
            self.db.register(token)
            self.Close()
            self.success = True
        else:
            self.information.textctrl.SetValue(
                "Unexpected error. Please restart the app"
            )

    def ShowModal(self):
        threadpool.submit(
            refresh_token.get_refresh_token, self.do_authorize, self.reddit
        )
        super().ShowModal()
        return self.success
