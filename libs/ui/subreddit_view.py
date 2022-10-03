import praw.models
from gi.repository import Gtk
from .submissions_list import SubmissionsList
from .new_post_dialog import NewPostDialog
from .utils import SimpleButton
from .. import threadpool


class SubredditView(Gtk.Frame):
    def __init__(self, subreddit: praw.models.Subreddit):
        super().__init__(label=subreddit.display_name)  # type: ignore
        self.subreddit = subreddit
        self.main_box = Gtk.Box(Gtk.Orientation.VERTICAL)
        self.top_box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.buttons = [SimpleButton("_New post...", self.new_post)]
        for button in self.buttons:
            self.top_box.add(button)
        self.sort_store = Gtk.ListStore(str, object)
        self.sort_list = Gtk.TreeView()
        self.sort_list.set_model(self.sort_store)
        self.sort_list.append_column(
            Gtk.TreeViewColumn("Item", Gtk.CellRendererText(), text=0)
        )
        self.sort_list.get_accessible().set_name("Sort by")
        self.sort_list.connect("row-activated", self.on_sort_change)
        for label, item in [
            ("New", lambda: subreddit.new(limit=None)),  # type: ignore
            ("Hot", lambda: subreddit.hot(limit=None)),  # type: ignore
            ("Rising", lambda: subreddit.rising(limit=None)),  # type: ignore
            ("Top(all)", lambda: subreddit.top(limit=None)),
            ("Top(hour)", lambda: subreddit.top(time_filter="hour", limit=None)),
            ("Top(day)", lambda: subreddit.top(time_filter="day", limit=None)),
            ("Top(week)", lambda: subreddit.top(time_filter="week", limit=None)),
            ("Top(month)", lambda: subreddit.top(time_filter="month", limit=None)),
            ("Top(year)", lambda: subreddit.top(time_filter="year", limit=None)),
            ("Controversial(all)", lambda: subreddit.controversial(limit=None)),
            (
                "Controversial(hour)",
                lambda: subreddit.controversial(time_filter="hour", limit=None),
            ),
            (
                "Controversial(day)",
                lambda: subreddit.controversial(time_filter="day", limit=None),
            ),
            (
                "Controversial(week)",
                lambda: subreddit.controversial(time_filter="week", limit=None),
            ),
            (
                "Controversial(month)",
                lambda: subreddit.controversial(time_filter="month", limit=None),
            ),
            (
                "Controversial(year)",
                lambda: subreddit.controversial(time_filter="year", limit=None),
            ),
        ]:
            self.sort_store.append([label, item])
        self.top_box.add(self.sort_list)
        self.main_box.add(self.top_box)
        self.submissions_list = SubmissionsList("Submissions", subreddit.new(limit=None))  # type: ignore
        self.main_box.add(self.submissions_list)
        self.add(self.main_box)

    def new_post(self):
        if submission := NewPostDialog(self.subreddit).run():
            self.submissions_list.prepend_submission(submission)

    def on_sort_change(self, widget, row, column):
        iter_ = self.sort_store.get_iter(row)
        sort_item = self.sort_store.get_value(iter_, 1)
        threadpool.submit(sort_item, self.submissions_list.set_submissions)
