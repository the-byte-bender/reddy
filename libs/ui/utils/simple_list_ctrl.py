from typing import Callable
import wx
from . import LabeledListCtrl


class SimpleListCtrl(LabeledListCtrl):
    def __init__(self, parrent: wx.Window, label_text: str):
        super().__init__(parrent, label_text)
        self.listctrl.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_press)
        self.items: list = []

    def insert_column(self, position: int, name: str):
        """
        Insert a column into the list control at the specified position

        @param position The position of the column.
        @param name The name of the column.
        """
        self.listctrl.InsertColumn(position, name)

    def append_column(self, name):
        """
        Appends a column to the list control

        @param name The name of the column.
        """
        self.listctrl.AppendColumn(name)

    def append_item(self, item: tuple, on_press: Callable[[], None]):
        """
        It adds an item to the list control and stores a function to be called when the item is selected

        @param item
        @param on_press
        """
        self.listctrl.Append(item)
        self.items.append(on_press)

    def on_press(self, event: wx.ListEvent):
        index: int = event.GetIndex()
        self.items[index]()
