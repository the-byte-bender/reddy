import contextlib
from gi.repository import Gtk
import praw
import praw.util.token_manager
from . import authorize, submissions_list
from .subreddit_view import SubredditView
from .utils import LabeledTextbox, InputDialog, SimpleButton
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
        self.front_page: submissions_list.SubmissionsList = submissions_list.SubmissionsList(
            "Front page", self.reddit.front.new(limit=None), True  # type: ignore
        )
        self.add_tab("Front page", self.front_page, False)
        self.box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.box.add(self.main_notebook)
        self.box.add(SimpleButton("New _tab", self.new_tab_dialog))
        self.box.add(SimpleButton("_Close current tab", self.remove_current_tab))
        self.add(self.box)

    def add_tab(self, label: str, widget: Gtk.Widget, closable: bool = True):
        widget._tab_closable = closable
        self.main_notebook.append_page(widget, Gtk.Label(label))
        self.main_notebook.show_all()
        page = self.main_notebook.get_n_pages() - 1
        self.main_notebook.set_current_page(page)

    def remove_current_tab(self):
        page_index = self.main_notebook.get_current_page()
        page = self.main_notebook.get_nth_page(page_index)
        if page._tab_closable:
            self.main_notebook.remove_page(page_index)
            self.main_notebook.set_current_page(page_index - 1)
            self.main_notebook.show_all()

    def new_tab_dialog(self):
        if subreddit_name := InputDialog("Please type in a subreddit", "r/").run():
            with contextlib.suppress(Exception):
                subreddit = self.reddit.subreddit(subreddit_name)
                subreddit._fetch()
                self.add_subreddit_as_tab(subreddit)

    def add_subreddit_as_tab(self, subreddit):
        subreddit_widget = SubredditView(subreddit)
        self.add_tab(subreddit.display_name, subreddit_widget)
