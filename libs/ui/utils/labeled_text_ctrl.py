import typing
from gi.repository import Gtk


class LabeledTextbox(Gtk.Box):
    def __init__(
        self,
        label_text: str,
        initial_value: str = "",
        editable: bool = True,
        multiline: bool = False,
    ):
        super().__init__(Gtk.Orientation.VERTICAL)
        self.textbox: typing.Union[Gtk.Entry, Gtk.TextView]
        self.multiline: bool = multiline
        self.text_buffer: Gtk.TextBuffer
        self.label = Gtk.Label(label_text)
        self.add(self.label)
        self.textbox = Gtk.TextView() if multiline else Gtk.Entry()
        self.textbox.get_accessible().set_name(label_text)
        self.textbox.set_editable(editable)
        if multiline:
            self.text_buffer = Gtk.TextBuffer()
            self.textbox.set_buffer(self.text_buffer)
            self.textbox.set_wrap_mode(Gtk.WrapMode.NONE)
        self.add(self.textbox)
        self.set_text(initial_value)

    def get_text(self):
        if self.multiline:
            return self.text_buffer.get_text(
                self.text_buffer.get_start_iter(), self.text_buffer.get_end_iter(), True
            )
        return self.textbox.get_text()

    def set_text(self, text: str):
        if self.multiline:
            return self.text_buffer.set_text(text, -1)
        return self.textbox.set_text(text)

    text = property(get_text, set_text)
