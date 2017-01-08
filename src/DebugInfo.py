from pygame import Rect, Color
from engine.GameObject import GameObject
from engine.Point import Point


class DebugInfo(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None)
        self.system = game_data['system']
        self.screen_size = game_data['screen_size']
        self.log = ""
        self.dest = Rect((0, self.screen_size.y - 60), (self.screen_size.x, 60))
        self._layer = 10

    def render(self):
        delta_time = self.system.delta_time
        time = str(delta_time)[:4].ljust(8)
        fps  = str(1000/delta_time)[:4]
        text = "Time: {t} FPS: {f}".format(t=time, f=fps)

        box_color = Color(100, 100, 100)

        font_dest = Point(10, self.screen_size.y - 50)

        self.system.draw_geom("box", rect=self.dest, color=box_color, fixed=True)
        self.system.draw_font(text, "8bit16.ttf", 50, font_dest, centered=False,
                              fixed=True)