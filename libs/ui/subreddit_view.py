import praw.models
from gi.repository import Gtk
from .submissions_list import SubmissionsList
from .new_post_dialog import NewPostDialog
from .utils import SimpleButton


class SubredditView(Gtk.Frame):
    def __init__(self, subreddit: praw.models.Subreddit):
        super().__init__(label=subreddit.display_name)  # type: ignore
        self.subreddit = subreddit
        self.main_box = Gtk.Box(Gtk.Orientation.VERTICAL)
        self.top_box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.buttons = [SimpleButton("_New post...", self.new_post)]
        for button in self.buttons:
            self.top_box.add(button)
        self.main_box.add(self.top_box)
        self.submissions_list = SubmissionsList("Submissions", subreddit.new(limit=None))  # type: ignore
        self.main_box.add(self.submissions_list)
        self.add(self.main_box)

    def new_post(self):
        submission = NewPostDialog(self.subreddit).run()
        if submission:
            self.submissions_list.prepend_submission(submission)
