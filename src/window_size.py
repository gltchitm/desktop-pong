from gi.repository import Gtk


class WindowSize(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_decorated(False)
        self.set_size_request(1, 1)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_accept_focus(False)

        self.maximize()
        self.set_opacity(0.0)

        self.show_all()
