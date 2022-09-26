import praw.models
from gi.repository import Gtk
from .utils import LabeledTextbox


class NewPostDialog(Gtk.Dialog):
    def __init__(self, subreddit: praw.models.Subreddit):
        super().__init__("New submission")
        self.subreddit = subreddit
        self.box = self.get_content_area()
        self.box.add(
            LabeledTextbox(
                "Posting guidelines",
                subreddit.post_requirements()["guidelines_text"] or "",
                False,
                True,
            )
        )
        self.title_box = LabeledTextbox("Title")
        self.box.add(self.title_box)
        self.flairs_store = Gtk.ListStore(str, str)
        self.flairs_store.append(["None", ""])
        for flair in subreddit.flair.link_templates:
            self.flairs_store.append([flair["text"], flair["id"]])
        self.flair_combobox = Gtk.ComboBox()
        self.flair_combobox.get_accessible().set_name("Link flair:")
        self.flair_combobox.set_model(self.flairs_store)
        self.flair_combobox.set_active(0)
        self.box.add(self.flair_combobox)
        cellrenderertext = Gtk.CellRendererText()
        self.flair_combobox.pack_start(cellrenderertext, True)
        self.flair_combobox.add_attribute(cellrenderertext, "text", 0)
        self.body_box = LabeledTextbox("Post body", "", multiline=True)
        self.box.add(self.body_box)
        self.check_buttons = Gtk.ButtonBox(Gtk.Orientation.HORIZONTAL)
        self.spoiler_button = Gtk.CheckButton("mark submission as a spoiler")
        self.check_buttons.add(self.spoiler_button)
        self.nsfw_button = Gtk.CheckButton("Mark submission as NSFW")
        self.check_buttons.add(self.nsfw_button)
        self.box.add(self.check_buttons)
        self.add_button("_Submit", Gtk.ResponseType.OK)
        self.add_button("_Cancel", Gtk.ResponseType.CANCEL)

    def get_selected_flair(self):
        treeiter = self.flair_combobox.get_active_iter()
        model = self.flair_combobox.get_model()
        return model[treeiter][1] or None  # type: ignore

    def run(self):
        self.show_all()
        response = super().run()
        submission = None
        if response == Gtk.ResponseType.OK and self.title_box.get_text():
            submission = self.subreddit.submit(
                title=self.title_box.get_text(),
                flair_id=self.get_selected_flair(),
                selftext=self.body_box.get_text(),
                spoiler=self.spoiler_button.get_active(),
                nsfw=self.nsfw_button.get_active(),
            )
        self.destroy()
        return submission
