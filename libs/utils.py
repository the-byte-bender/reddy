import wx
def labeled_widget(parrent: wx.Window, label: str, widget: wx.Window, orient: int = wx.VERTICAL):
    """
    It takes a parent widget, a label string, a widget, and an optional orientation, and returns a tuple of the label widget, the widget, and a sizer that contains both of them
    
    @param parrent
    @param label The text to display next to the widget.
    @param widget The widget to be labeled.
    @param orient The orientation of the sizer, optional.
    
    @return A tuple of the label widget, the widget, and the sizer.
    """
    sizer: wx.BoxSizer = wx.BoxSizer(orient)
    label_widget: wx.StaticText = wx.StaticText(parrent, label = label)
    sizer.Add(label_widget, 0)
    sizer.Add(widget, 1, wx.EXPAND)
    return label_widget, widget, sizer