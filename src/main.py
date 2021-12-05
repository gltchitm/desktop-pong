import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from window_size import WindowSize
from ball_window import BallWindow
from paddle_window import PaddleWindow
from store import store

import config

store['ai_paddle'] = (None, None)
store['player_paddle'] = (None, None)
store['ball_position'] = (None, None)

def init(window_size):
    width, height = window_size

    left = PaddleWindow(
        window_size,
        config.PADDLE_PADDING,
        (height - config.PADDLE_SIZE[1]) / 2,
        True
    )
    right = PaddleWindow(
        window_size,
        width - config.PADDLE_SIZE[0] - config.PADDLE_PADDING,
        (height - config.PADDLE_SIZE[1]) / 2,
        False
    )

    ball_window = BallWindow(window_size)

    left.show_all()
    right.show_all()
    ball_window.show_all()

def window_size_map_callback(window, _event):
    window.add_tick_callback(lambda window, _frame_clock: window.destroy())
    init(window.get_size())

window_size = WindowSize()
window_size.connect('map-event', window_size_map_callback)

Gtk.main()
