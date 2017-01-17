from engine.GameObject import GameObject
from engine.Point import Point
from pygame import Rect, Color, time


class DebugInfo(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)
        self.log = ""
        self.dest = Rect((0, self.screen_size.y - 60), (self.screen_size.x, 60))
        self._layer = 10

    def render(self):
        fps = str(self.system.clock.get_fps())[:4].ljust(8)
        mouse = '{m.x} x {m.y}'.format(m=self.system.get_mouse_pos().int()).ljust(11)
        time_passed = time.get_ticks()
        playtime = '{h}:{m}:{s}.{t}'.format(
            h=str(int(time_passed / 1000 / 60 / 60)).rjust(2, '0'),
            m=str(int(time_passed / 1000 / 60 % 60)).rjust(2, '0'),
            s=str(int(time_passed / 1000 % 60)).rjust(2, '0'),
            t=str(int(time_passed % 1000)).rjust(3, '0')
        )
        text = "FPS: {f} Mouse: {m} Playtime: {p}".format(f=fps, m=mouse, p=playtime)

        box_color = Color(100, 100, 100, 127)

        font_dest = Point(10, self.dest.top + 15)

        self.system.draw_geom("box", rect=self.dest, color=box_color, fixed=True)
        self.system.draw_font(text, "8bit16.ttf", 50, font_dest, centered=False,
                              fixed=True)
