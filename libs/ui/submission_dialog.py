from gi.repository import Gtk
import praw.models
from .utils import LabeledTextbox
from .. import threadpool


class SubmissionDialog(Gtk.Dialog):
    def __init__(self, parrent: Gtk.Window, submission: praw.models.Submission):
        super().__init__(submission.title)
        self.submission = submission
        self.set_transient_for(parrent)
        self.content = self.get_content_area()
        self.box = Gtk.Box(Gtk.Orientation.HORIZONTAL)
        self.content.add(self.box)
        self.body = LabeledTextbox(
            submission.title, submission.selftext or "", False, True
        )
        self.box.add(self.body)
        self.add_button("Close", Gtk.ResponseType.CLOSE)
