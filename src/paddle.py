from gi.repository import Gtk, Gdk

from store import store
from near import near

import config

class Paddle(Gtk.Window):
    def __init__(self, window_size, x, y, is_ai):
        Gtk.Window.__init__(self)

        self.window_size = window_size

        self.is_ai = is_ai
        
        color = Gdk.RGBA(*config.PADDLE_AI_COLOR) if is_ai else Gdk.RGBA(*config.PADDLE_PLAYER_COLOR)
        self.override_background_color(Gtk.StateType.NORMAL, color)

        self.x = x
        self.y = y
        
        self.move(x, y)
        self.resize(*config.PADDLE_SIZE)

        self.set_app_paintable(False)
        self.set_decorated(False)
        self.set_accept_focus(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_deletable(False)

        self.dragging_from = None
        self.target_y = None
        self.add_tick_callback(self.tick)

        if not is_ai:
            self.connect("button-press-event", self.btn_press)
            self.connect("button-release-event", self.btn_release)
            self.connect("motion-notify-event", self.motion)
        else:
            store.add_hook_for_key("ball_position", self.ball_position_change)

        self.connect("realize", self.realize)
        self.connect("window-state-event", self.check_minimized)
    def rebuild(self):
        if config.USE_ANTI_TAMPER:
            self.destroy()
            self = Paddle(self.window_size, self.x, self.y, self.is_ai)
            self.show_all()
    def ball_position_change(self, new_position):
        self.target_y = new_position[1] - config.PADDLE_SIZE[1] / 2
    def tick(self, widget, frame_clock):
        current_x, current_y = self.get_position()

        if self.x != current_x or not near(self.y, current_y, config.PADDLE_LEEWAY):
            self.rebuild()
            return False

        if self.target_y != None:
            proposed_y = None
            if self.target_y - config.PADDLE_VELOCITY > self.y:
                proposed_y = self.y + config.PADDLE_VELOCITY
            elif self.target_y + config.PADDLE_VELOCITY < self.y:
                proposed_y = self.y - config.PADDLE_VELOCITY
            if (
                proposed_y != None and
                not proposed_y < config.SCREEN_PADDING and
                not proposed_y + config.PADDLE_SIZE[1] > self.window_size[1] - config.SCREEN_PADDING
            ):
                self.move(self.x, proposed_y)
                self.y = proposed_y

        if config.USE_ANTI_TAMPER:
            self.set_keep_above(True)
            self.get_window().move_to_desktop(0)

        if self.is_ai:
            store.set_value("ai_paddle", (self.x, current_y))
        else:
            store.set_value("player_paddle", (self.x, current_y))

        return True
    def check_minimized(self, widget, event):
        if event.new_window_state & Gdk.WindowState.ICONIFIED:
            self.rebuild()
    def realize(self, data):
        cursor_name = "not-allowed" if self.is_ai else "grab"
        cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), cursor_name)
        self.get_window().set_cursor(cursor)
    def btn_press(self, widget, event):
        if self.target_y == None:
            cursor = Gdk.Cursor.new_from_name(Gdk.Display().get_default(), "grabbing")
            self.get_window().set_cursor(cursor)
            _, current_y = self.get_position()
            self.dragging_from = current_y - (current_y - event.y)
            return True
    def btn_release(self, widget, event):
        cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "grab")
        self.get_window().set_cursor(cursor)
        self.target_y = None
        return True
    def motion(self, widget, event):
        if self.dragging_from != None:
            self.target_y = event.y_root - self.dragging_from
            return True
