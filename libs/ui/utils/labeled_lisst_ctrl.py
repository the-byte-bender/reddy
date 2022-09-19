import typing
from gi.repository import Gtk

callback_type = typing.Callable[[], None]


class LabeledListCtrl(Gtk.Box):
    def __init__(self, label_text: str, model: typing.Optional[typing.Iterable] = None):
        """
        @param label_text str - The text to display next to the list
        @param model This is a list of tuples. Each tuple has two items. The first item is the label for the
        column. The second item is the type of data that will be stored in the column.
        """
        if model is None:
            model = []
        super().__init__(Gtk.Orientation.HORIZONTAL)
        self.label: Gtk.Label = Gtk.Label(label_text)
        self.items: list[callback_type] = []
        self.pack_start(self.label, False, False, 0)
        self.liststore: Gtk.ListStore = Gtk.ListStore(*[i[1] for i in model])
        self.view: Gtk.TreeView = Gtk.TreeView()
        self.view.connect("row-activated", self.on_activate)
        self.view.get_selection().set_mode(Gtk.SelectionMode.BROWSE)
        self.view.get_accessible().set_name(label_text)
        self.view.set_model(self.liststore)
        self.pack_start(self.view, True, True, 0)
        self.renderer = Gtk.CellRendererText()
        for index, item in enumerate(model):
            label: str = item[0]
            self.view.append_column(
                Gtk.TreeViewColumn(label, self.renderer, text=index)
            )

    def append_item(self, item: list, callback: callback_type):
        self.liststore.append(item)
        self.items.append(callback)

    def on_activate(self, *args):
        index: int = self.view.get_selection().get_selected_rows()[1][0][0]
        self.items[index]()
