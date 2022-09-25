import typing
from gi.repository import Gtk


class SimpleButton(Gtk.Button):
    def __init__(
        self, label: str, callback: typing.Optional[typing.Callable[[], None]]
    ):
        super().__init__(label)
        self.set_use_underline(True)
        self.callback = callback
        if callback:
            self.connect("clicked", self.on_clicked)

    def on_clicked(self, *args):
        self.stop_emission_by_name("clicked")
        self.callback()
