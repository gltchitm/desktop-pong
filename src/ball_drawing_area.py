from gi.repository import Gtk

from config import BALL_DIAMETER, BALL_COLOR
from math import tau

class BallDrawingArea(Gtk.DrawingArea):
    def __init__(self, _window):
        Gtk.DrawingArea.__init__(self)

        self.connect('draw', self.draw)
    def draw(self, _event, cr):
        radius = BALL_DIAMETER / 2
        cr.arc(radius, radius, radius, 0, tau)
        cr.set_source_rgb(*BALL_COLOR)
        cr.fill_preserve()
        return False
