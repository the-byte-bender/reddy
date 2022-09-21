import typing
import praw.models
from gi.repository import Gtk
from .. import threadpool


class SubmitionsList(Gtk.Box):
    def __init__(
        self,
        label: str,
        submitions: typing.Iterable[praw.models.Submission],
        show_subreddit_name: bool = False,
    ):
        super().__init__()
        self.show_subreddit_name: bool = show_subreddit_name
        self._active = True
        self.connect("destroy", lambda _: setattr(self, "_active", False))
        self.label = Gtk.Label(label)
        self.add(self.label)
        self.liststore = Gtk.ListStore(str, str, str, int, int, bool, bool, object)
        self.view = Gtk.TreeView()
        self.view.set_model(self.liststore)
        self.view.get_accessible().set_name(label)
        self.add(self.view)
        self.text_renderer = Gtk.CellRendererText()
        self.upvote_toggle = Gtk.CellRendererToggle()
        self.upvote_toggle.connect("toggled", self.do_upvote)
        self.upvote_toggle.set_radio(True)
        self.downvote_toggle = Gtk.CellRendererToggle()
        self.downvote_toggle.connect("toggled", self.do_downvote)
        self.downvote_toggle.set_radio(True)
        self.subreddit_name_column = Gtk.TreeViewColumn(
            "Subreddit", self.text_renderer, text=0
        )
        self.view.append_column(self.subreddit_name_column)
        self.title_column = Gtk.TreeViewColumn("Title", self.text_renderer, text=1)
        self.view.append_column(self.title_column)
        self.author_column = Gtk.TreeViewColumn("Author", self.text_renderer, text=2)
        self.view.append_column(self.author_column)
        self.upvotes_column = Gtk.TreeViewColumn("Upvotes", self.text_renderer, text=3)
        self.view.append_column(self.upvotes_column)
        self.comments_column = Gtk.TreeViewColumn(
            "Comments", self.text_renderer, text=4
        )
        self.view.append_column(self.comments_column)
        self.upvote_column = Gtk.TreeViewColumn("Upvote", self.upvote_toggle, active=5)
        self.view.append_column(self.upvote_column)
        self.downvote_column = Gtk.TreeViewColumn(
            "Downvote", self.downvote_toggle, active=6
        )
        self.view.append_column(self.downvote_column)
        for submission in submitions:
            self.append_submission(submission)

    def _add_submission(self, submission: praw.models.Submission):
        item = []
        if self.show_subreddit_name:
            item.append(submission.subreddit.display_name)
        else:
            item.append("")
        item.extend(
            [
                submission.title,
                submission.author.name,
                submission.score,
                submission.num_comments,
                submission.likes is True,
                submission.likes is False,
                submission,
            ]
        )
        self.liststore.append(item)

    def load_submission(self, submission: praw.models.Submission):
        if not self._active:
            return
        if not submission._fetched:
            submission.comments
        return submission

    def append_submission(self, submission: praw.models.Submission):
        threadpool.submit(self.load_submission, self._add_submission, submission)

    def do_upvote(self, renderer, treepath):
        row = self.liststore[treepath]
        upvote_value = row[5]
        submission = row[7]
        if not upvote_value:
            threadpool.submit(submission.upvote, None, threadpool=1)
            row[3] += 1
        else:
            threadpool.submit(submission.clear_vote, None, threadpool=1)
            row[3] -= 1
        row[5] = not upvote_value
        row[6] = False

    def do_downvote(self, renderer, treepath):
        row = self.liststore[treepath]
        downvote_value = row[6]
        submission = row[7]
        if not downvote_value:
            threadpool.submit(submission.downvote, None, threadpool=1)
            row[3] -= 1
        else:
            threadpool.submit(submission.clear_vote, None, threadpool=1)
            row[3] += 1
        row[6] = not downvote_value
        row[5] = False
