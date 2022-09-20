import typing
from gi.repository import Gtk

callback_type = typing.Callable[[], None]


class LabeledListCtrl(Gtk.Box):
    def __init__(
        self,
        label_text: str,
        model: typing.Optional[typing.Iterable] = None,
        callback_column: int = -1,
    ):
        """
        @param label_text str - The text to display next to the list
        @param model This is a list of tuples. Each tuple has two items. The first item is the label for the
        column (can be None for a hidden column). The second item is the type of data that will be stored in the column.
        """
        if model is None:
            model = []
        super().__init__(Gtk.Orientation.HORIZONTAL)
        self.label: Gtk.Label = Gtk.Label(label_text)
        self.pack_start(self.label, False, False, 0)
        self.callback_column = callback_column
        self.liststore: Gtk.ListStore = Gtk.ListStore(*[i[1] for i in model])
        self.view: Gtk.TreeView = Gtk.TreeView()
        self.view.connect("row-activated", self.on_activate)
        self.view.get_selection().set_mode(Gtk.SelectionMode.BROWSE)
        self.view.get_accessible().set_name(label_text)
        self.view.set_model(self.liststore)
        self.pack_start(self.view, True, True, 0)
        self.renderer = Gtk.CellRendererText()
        for index, item in enumerate(model):
            label: typing.Optional[str] = item[0]
            if not label:
                continue
            self.view.append_column(
                Gtk.TreeViewColumn(label, self.renderer, text=index)
            )

    def append_item(
        self,
        item: list,
    ):
        self.liststore.append(item)

    def on_activate(self, widget, row, column):
        if self.callback_column == -1:
            return
        iter_ = self.liststore.get_iter(row)
        print(row, column)
        callback = self.liststore.get_value(iter_, self.callback_column)
        callback()
