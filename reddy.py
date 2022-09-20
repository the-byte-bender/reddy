import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from libs.ui import main

window: Gtk.Window = main.Main(
    title="Reddy",
    client_id=os.getenv("REDDY_CLIENT_ID") or "TQbF2Bjmk_ilyTry-c_G8A",
    client_secret=os.getenv("REDDY_CLIENT_SECRET"),
    user_agent=os.getenv("REDDY_USER_AGENT") or "reddy",
    db_path=os.getenv("REDDY_DB_PATH") or "./reddy.db",
)
window.show_all()
Gtk.main()
