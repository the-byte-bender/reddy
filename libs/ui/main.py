import wx
import praw
import praw.util.token_manager
from . import authorize
from .utils import LabeledTextbox
from .. import refresh_token


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
        self.refresh_tokens_db = praw.util.token_manager.SQLiteTokenManager(
            database=self.db_path, key=self.client_id
        )
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri="http://localhost:13456",
            token_manager=self.refresh_tokens_db,
            user_agent=self.user_agent,
        )
        self.panel: wx.Panel = wx.Panel(self)
        if not self.refresh_tokens_db.is_registered():
            success = authorize.AuthorizeDialog(
                self.panel, self.reddit, self.refresh_tokens_db
            ).ShowModal()
            if not success:
                self.Close()
        self.main_sizer: wx.BoxSizer = wx.BoxSizer()
        self.main_notebook: wx.Notebook = wx.Notebook(self.panel, style=wx.NB_BOTTOM)
        self.main_sizer.Add(self.main_notebook)
        self.temp = LabeledTextbox(
            self.main_notebook,
            "Come back later",
            "Nothing to do here. Come back when a feature or 2 is implemented",
            textctrl_style=wx.TE_READONLY | wx.TE_DONTWRAP | wx.TE_MULTILINE,
        )
        self.main_notebook.AddPage(self.temp, "Home")
        self.panel.SetSizer(self.main_sizer)
        self.main_notebook.SetFocus()
