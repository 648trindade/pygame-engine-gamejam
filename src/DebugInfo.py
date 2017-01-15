from pygame import Rect, Color
from engine import GameObject, Point


class DebugInfo(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)
        self.log = ""
        self.dest = Rect((0, self.screen_size.y - 60), (self.screen_size.x, 60))
        self._layer = 10

    def render(self):
        delta_time = self.system.delta_time
        time  = str(delta_time)[:4].ljust(8)
        fps   = str(1000/delta_time)[:4].ljust(8)
        mouse = self.system.get_mouse_pos().int()
        text = "Time: {t} FPS: {f} Mouse: {m.x} x {m.y}".format(t=time, f=fps, m=mouse)

        box_color = Color(100, 100, 100, 127)

        font_dest = Point(10, self.screen_size.y - 50)

        self.system.draw_geom("box", rect=self.dest, color=box_color, fixed=True)
        self.system.draw_font(text, "8bit16.ttf", 50, font_dest, centered=False,
                              fixed=True)