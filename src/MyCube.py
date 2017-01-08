from pygame import Rect, Color
from random import randrange
from engine.GameObject import GameObject
from engine.Point import Point

class MyCube(GameObject):

    def __init__(self, game_data):
        GameObject.__init__(self, None)

        self.dest = Rect(0,0,100,100)
        self.vel  = Point(1,1)
        self._layer = 1

        self.system = game_data['system']
        self.screen_size = game_data['screen_size']
        self.color = Color(127, 127, 127)

    def update(self):
        self.dest += self.vel
        if not self.system.camera.contains(self.dest):
            if self.dest.left < self.system.camera.left:
                self.vel.x = 1
            elif self.dest.right > self.system.camera.right:
                self.vel.x = -1

            if self.dest.top < self.system.camera.top:
                self.vel.y = 1
            elif self.dest.bottom > self.system.camera.bottom:
                self.vel.y = -1

        self.color.r = (self.color.r + randrange(-10, 11)) % 256
        self.color.g = (self.color.g + randrange(-10, 11)) % 256
        self.color.b = (self.color.b + randrange(-10, 11)) % 256

    def render(self):
        self.system.draw_geom("box", rect=self.dest, color=self.color)