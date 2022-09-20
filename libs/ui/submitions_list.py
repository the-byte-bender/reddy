import typing
import praw.models
from gi.repository import Gtk
from .utils import LabeledListCtrl
from .. import threadpool


class SubmitionsList(LabeledListCtrl):
    def __init__(
        self,
        label: str,
        submitions: typing.Iterable[praw.models.Submission],
        show_subreddit_name: bool = False,
    ):
        super().__init__(
            label,
            [
                ("Subreddit", str),
                ("Title", str),
                ("Author", str),
                ("Upvotes", int),
                ("Comments", int),
                (None, object),
            ],
            5,
        )
        self.submissions: list[praw.models.Submission] = []
        self.show_subreddit_name: bool = show_subreddit_name
        for submission in submitions:
            self.append_submission(submission)

    def append_submission(self, submission: praw.models.Submission):
        self.submissions.append(submission)
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
                lambda: lambda: None,  # todo
            ]
        )
        self.append_item(
            item,
        )
