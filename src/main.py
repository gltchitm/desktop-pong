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

def init(window_size, window_position):
    width, height = window_size

    left = PaddleWindow(
        window_size,
        config.PADDLE_PADDING + window_position[0],
        (height - config.PADDLE_SIZE[1]) / 2,
        True
    )
    right = PaddleWindow(
        window_size,
        width - config.PADDLE_SIZE[0] - config.PADDLE_PADDING + window_position[0],
        (height - config.PADDLE_SIZE[1]) / 2,
        False
    )

    ball_window = BallWindow(window_size, window_position)

    left.show_all()
    right.show_all()
    ball_window.show_all()

def window_draw_callback(window, event):
    window_size = window.get_size()

    if window_size == (1, 1):
        return

    window.add_tick_callback(lambda window, frame_clock: window.destroy())
    init(window_size, window.get_position())

window_size = WindowSize()
window_size.connect('draw', window_draw_callback)

Gtk.main()
