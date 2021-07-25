from gi.repository import Gtk, Gdk
import cairo

from random import getrandbits

from ball_drawing_area import BallDrawingArea
from store import store
from near import near

import config

def rand_velocity():
    return config.BALL_VELOCITY if getrandbits(1) else -config.BALL_VELOCITY
class BallWindow(Gtk.Window):
    def __init__(self, window_size, x=None, y=None, x_velocity=None, y_velocity=None):
        Gtk.Window.__init__(self)

        self.window_size = window_size

        self.x = x
        self.y = y

        self.x_velocity = x_velocity if x_velocity != None else rand_velocity()
        self.y_velocity = y_velocity if y_velocity != None else rand_velocity()

        self.rebuilding = False

        self.set_app_paintable(True)
        self.set_decorated(False)
        self.set_accept_focus(False)
        self.set_keep_above(True)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_deletable(False)

        self.set_size_request(config.BALL_DIAMETER, config.BALL_DIAMETER)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_visual(self.get_screen().get_rgba_visual())

        self.add_tick_callback(self.tick)

        if self.x and self.y:
            self.move(self.x, self.y)
        
        self.connect("realize", self.realize)
        self.connect("draw", self.draw)
        self.connect("window-state-event", self.check_minimized)
    def rebuild(self, use_current_position):
        if not self.rebuilding:
            if config.USE_ANTI_TAMPER or not use_current_position:
                self.rebuilding = True
                self.destroy()
                if use_current_position:
                    self = BallWindow(self.window_size, self.x, self.y, self.x_velocity, self.y_velocity)
                else:
                    self = BallWindow(self.window_size)
                self.show_all()
    def tick(self, widget, frame_clock):
        if config.USE_ANTI_TAMPER:
            self.set_keep_above(True)
            self.get_window().move_to_desktop(0)

        current_x, current_y = self.get_position()
        ai_x, ai_y = store.get_value("ai_paddle")
        player_x, player_y = store.get_value("player_paddle")
        width, height = self.window_size

        if ai_x == None or player_x == None:
            return True

        if (
            current_x < config.SCREEN_PADDING or
            current_x + config.BALL_DIAMETER > width - config.SCREEN_PADDING
        ):
            self.x -= self.x_velocity
            self.rebuild(False)

        if (
            current_y < config.SCREEN_PADDING or
            current_y + config.BALL_DIAMETER > height - config.SCREEN_PADDING
        ):
            self.y -= self.y_velocity
            self.y_velocity *= -1

        if (
            self.x < ai_x + (config.BALL_DIAMETER / 2 + config.BALL_PADDING) and
            self.y + (config.BALL_DIAMETER + config.BALL_PADDING) > ai_y and
            self.y < ai_y + config.PADDLE_SIZE[1] + config.BALL_PADDING
        ):
            self.x_velocity *= -1
            if config.USE_BALL_STUCK_IN_PADDLE_FIX:
                self.x = ai_x + (config.BALL_DIAMETER / 2 + config.BALL_PADDING)
        if (
            self.x > player_x - (config.BALL_DIAMETER + config.BALL_PADDING) and
            self.y + (config.BALL_DIAMETER + config.BALL_PADDING) > player_y and
            self.y < player_y + config.PADDLE_SIZE[1] + config.BALL_PADDING
        ):
            self.x_velocity *= -1
            if config.USE_BALL_STUCK_IN_PADDLE_FIX:
                self.x = player_x - (config.BALL_DIAMETER + config.BALL_PADDING)

        if not near(self.x, current_x, config.BALL_LEEWAY) or not near(self.y, current_y, config.BALL_LEEWAY):
            self.rebuild(True)

        self.x += self.x_velocity
        self.y += self.y_velocity

        self.move(self.x, self.y)

        store.set_value("ball_position", (self.x, self.y, self.x_velocity, self.y_velocity))

        return True
    def check_minimized(self, widget, event):
        if event.new_window_state & Gdk.WindowState.ICONIFIED:
            self.rebuild(True)
    def realize(self, widget):
        current_x, current_y = self.get_position()
        self.x = current_x
        self.y = current_y

        ball = BallDrawingArea(self.get_window())
        self.add(ball)
        ball.show_all()

        cursor = Gdk.Cursor.new_from_name(Gdk.Display.get_default(), "not-allowed")
        self.get_window().set_cursor(cursor)
    def draw(self, widget, cr):
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()

        return False
