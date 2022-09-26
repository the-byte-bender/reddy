from itertools import islice
import typing
import praw.models
from gi.repository import Gtk
from . import submission_dialog
from .. import threadpool


class SubmitionsList(Gtk.Box):
    def __init__(
        self,
        label: str,
        submissions: typing.Iterable[praw.models.Submission],
        show_subreddit_name: bool = False,
    ):
        super().__init__()
        self.show_subreddit_name: bool = show_subreddit_name
        self.submissions = submissions
        self._active = True
        self.connect("destroy", lambda _: setattr(self, "_active", False))
        self.label = Gtk.Label(label)
        self.add(self.label)
        self.liststore = Gtk.ListStore(str, str, str, str, int, int, bool, bool, object)
        self.view = Gtk.TreeView()
        self.view.connect("row-activated", self.on_activate)
        self.view.set_model(self.liststore)
        self.view.get_accessible().set_name(label)
        self.selection = self.view.get_selection()
        self.selection.connect("changed", self.on_selection_change)
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
        self.link_flair_column = Gtk.TreeViewColumn(
            "Link flair", self.text_renderer, text=1
        )
        self.view.append_column(self.link_flair_column)
        self.title_column = Gtk.TreeViewColumn("Title", self.text_renderer, text=2)
        self.view.append_column(self.title_column)
        self.author_column = Gtk.TreeViewColumn("Author", self.text_renderer, text=3)
        self.view.append_column(self.author_column)
        self.upvotes_column = Gtk.TreeViewColumn("Upvotes", self.text_renderer, text=4)
        self.view.append_column(self.upvotes_column)
        self.comments_column = Gtk.TreeViewColumn(
            "Comments", self.text_renderer, text=5
        )
        self.view.append_column(self.comments_column)
        self.upvote_column = Gtk.TreeViewColumn("Upvote", self.upvote_toggle, active=6)
        self.view.append_column(self.upvote_column)
        self.downvote_column = Gtk.TreeViewColumn(
            "Downvote", self.downvote_toggle, active=7
        )
        self.view.append_column(self.downvote_column)
        self.append_more_submissions()

    def append_more_submissions(self):
        for submission in islice(self.submissions, 50):
            self.append_submission(submission)

    def on_selection_change(self, selection):
        selection = self.view.get_selection()
        model, iter = selection.get_selected()
        if iter is not None and not model.iter_next(iter):
            self.append_more_submissions()

    def _add_submission(self, value: tuple[praw.models.Submission, bool]):
        submission, prepend = value
        submission._extra_replies = []
        item = []
        if self.show_subreddit_name:
            item.append(submission.subreddit.display_name)
        else:
            item.append("")
        item.extend(
            [
                submission.link_flair_text or "",
                submission.title,
                submission.author.name,
                submission.score,
                submission.num_comments,
                submission.likes is True,
                submission.likes is False,
                submission,
            ]
        )
        self.liststore.prepend(item) if prepend else self.liststore.append(item)

    def load_submission(self, submission: praw.models.Submission, prepend=False):
        if not self._active:
            return
        if not submission._fetched:
            submission.comments
        return submission, prepend

    def append_submission(self, submission: praw.models.Submission):
        threadpool.submit(self.load_submission, self._add_submission, submission)

    def prepend_submission(self, submission: praw.models.Submission):
        threadpool.submit(self.load_submission, self._add_submission, submission, True)

    def do_upvote(self, renderer, treepath):
        row = self.liststore[treepath]
        upvote_value = row[6]
        submission = row[8]
        if not upvote_value:
            threadpool.submit(submission.upvote, None, threadpool=1)
            row[4] += 1
        else:
            threadpool.submit(submission.clear_vote, None, threadpool=1)
            row[4] -= 1
        row[6] = not upvote_value
        row[7] = False

    def do_downvote(self, renderer, treepath):
        row = self.liststore[treepath]
        downvote_value = row[7]
        submission = row[8]
        if not downvote_value:
            threadpool.submit(submission.downvote, None, threadpool=1)
            row[4] -= 1
        else:
            threadpool.submit(submission.clear_vote, None, threadpool=1)
            row[4] += 1
        row[7] = not downvote_value
        row[6] = False

    def on_activate(self, widget, row, column):
        iter_ = self.liststore.get_iter(row)
        submission = self.liststore.get_value(iter_, 8)
        dialog = submission_dialog.SubmissionDialog(self.get_toplevel(), submission)  # type: ignore
        dialog.show_all()
        dialog.run()
        dialog.destroy()
