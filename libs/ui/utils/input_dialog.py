from gi.repository import Gtk
from . import LabeledTextbox


class InputDialog(Gtk.Dialog):
    def __init__(self, title: str, question: str):
        super().__init__(title)
        self.box = self.get_content_area()
        self.input = LabeledTextbox(question, "")
        self.input.textbox.set_activates_default(True)
        self.box.add(self.input)
        button = self.add_button("Done", Gtk.ResponseType.OK)
        button.set_can_default(True)
        button.grab_default()

    def run(self):
        self.show_all()
        response = super().run()
        text = self.input.get_text()
        self.destroy()
        return text if response == Gtk.ResponseType.OK else None
