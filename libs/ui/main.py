from gi.repository import Gtk
import praw
import praw.util.token_manager
from . import authorize, submitions_list
from .utils import LabeledTextbox
from .. import refresh_token, threadpool


class Main(Gtk.Window):
    def __init__(
        self,
        title: str = "Reddy",
        client_id: str = "",
        client_secret: str = "",
        user_agent: str = "reddy",
        db_path: str = "",
    ):
        super().__init__(title=title)
        self.connect("destroy", Gtk.main_quit)
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
        if not self.refresh_tokens_db.is_registered():
            success = authorize.AuthorizeDialog(
                self, self.reddit, self.refresh_tokens_db
            ).run()
            if not success:
                self.close()
                return
        self.main_notebook: Gtk.Notebook = Gtk.Notebook()
        self.main_notebook.get_accessible().set_name("Main tab bar")
        self.front_page: submitions_list.SubmitionsList = (
            submitions_list.SubmitionsList(
                "Front page", self.reddit.front.new(limit=None), True
            )
        )
        self.add_tab("Front page", self.front_page)
        self.add(self.main_notebook)

    def add_tab(self, label: str, widget: Gtk.Widget):
        self.main_notebook.append_page(widget, Gtk.Label(label))
