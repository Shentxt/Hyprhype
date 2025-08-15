import math
import cairo
from gi.repository import Gdk, GdkPixbuf
from fabric.widgets.image import Image

class CustomImage(Image):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._pixbuf = kwargs.get("pixbuf", getattr(self, "pixbuf", None))

    def do_render_rounded_rect(self, cr: cairo.Context, width: int, height: int, radius: int):
        cr.new_path()
        cr.move_to(radius, 0)
        cr.line_to(width - radius, 0)
        cr.arc(width - radius, radius, radius, -math.pi/2, 0)
        cr.line_to(width, height - radius)
        cr.arc(width - radius, height - radius, radius, 0, math.pi/2)
        cr.line_to(radius, height)
        cr.arc(radius, height - radius, radius, math.pi/2, math.pi)
        cr.line_to(0, radius)
        cr.arc(radius, radius, radius, math.pi, 3*math.pi/2)
        cr.close_path()

    def do_draw(self, cr: cairo.Context):
        pixbuf = self._pixbuf
        if not pixbuf:
            return

        width = pixbuf.get_width()
        height = pixbuf.get_height()
        radius = int(min(width, height) * 0.1)  

        cr.save()
        self.do_render_rounded_rect(cr, width, height, radius)
        cr.clip()

        Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
        cr.paint()
        cr.restore()
