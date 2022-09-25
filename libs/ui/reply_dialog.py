import typing
from gi.repository import Gtk
from .utils import SimpleButton, LabeledTextbox
from .. import threadpool
import praw.models

ID_SEND = 100
ID_CANCEL = 101


class ReplyDialog(Gtk.Dialog):
    def __init__(
        self,
        parent_window: Gtk.Widget,
        title: str,
        parent: typing.Union[praw.models.Comment, praw.models.Submission],
    ):
        super().__init__(title)
        self.set_transient_for(parent_window)
        self.parent = parent
        self.box = self.get_content_area()
        self.parent_text = (
            parent.body
            if isinstance(parent, praw.models.Comment)
            else (parent.selftext or parent.url or "")
        )
        self.parent_body = LabeledTextbox("Replying to", self.parent_text, False, True)
        self.box.add(self.parent_body)
        self.reply_body = LabeledTextbox("Your reply", "", True, True)
        self.box.add(self.reply_body)
        self.add_button("_Send", ID_SEND)
        self.add_button("_Cancel", ID_CANCEL)

    def run(self):
        self.show_all()
        response = super().run()
        if response == ID_SEND:
            try:
                comment = self.parent.reply(body=self.reply_body.get_text())
                if isinstance(self.parent, praw.models.Submission):
                    self.parent._fetch()
                else:
                    self.parent.refresh()
                self.destroy()
                return comment
            except Exception as e:
                print(e)
                self.destroy()
                return None
        self.destroy()
        return None
