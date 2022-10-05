import typing
import praw
import praw.util.token_manager
from gi.repository import Gtk
from .. import refresh_token, threadpool
from .utils import LabeledTextbox


class AuthorizeDialog(Gtk.Dialog):
    def __init__(
        self,
        parrent: Gtk.Window,
        reddit: praw.Reddit,
        db: refresh_token.KeyringTokenManager,
    ):
        super().__init__("Please authorize access to your account")
        self.set_transient_for(parrent)
        self.set_modal(True)
        self.box: Gtk.Box = self.get_content_area()
        self.reddit = reddit
        self.db = db
        self.success: bool = False
        self.information: LabeledTextbox = LabeledTextbox(
            "Information",
            "Please  authorize this app to access your account",
            editable=False,
            multiline=True,
        )
        self.box.add(self.information)

    def do_authorize(self, token: typing.Optional[str]):
        if isinstance(token, str):
            self.db.set_token(token)
            self.destroy()
            self.success = True
        else:
            self.information.set_text("Unexpected error. Please restart the app")

    def run(self):
        threadpool.submit(
            refresh_token.get_refresh_token, self.do_authorize, self.reddit
        )
        self.show_all()
        super().run()
        return self.success
