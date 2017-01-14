from pygame import Rect, Color
from random import randrange
from engine.GameObject import GameObject
from engine.Point import Point

#GRAVITY = 100
#INITIAL_VEL = -200

class MyCube(GameObject):

    def __init__(self, game_data):
        GameObject.__init__(self, None)

        self.system = game_data['system']
        self.screen_size = game_data['screen_size']
        self.color = Color(127, 127, 127)

        self.dest = Rect(self.system.camera.centerx, self.system.camera.centery-100, 100, 100)
        self.vel  = Point(randrange(-10,11), randrange(-10,11))
        self.position = Point(self.dest.topleft)
        self._layer = 1

    def bounce(self, value):
        pass

    def update(self):
        self.dest += self.vel
        if self.dest.left not in range(0, self.system.camera.right - self.dest.width):
            self.vel.x *= -1

        if self.dest.top not in range(0, self.system.camera.bottom - self.dest.height):
            self.vel.y *= -1

        # s = s0 + v0t + at²/2
        # t = self.system.delta_time / 1000
        # a = Point(0, GRAVITY)
        # v0t = self.vel * t
        # at2 = a * ((t ** 2) / 2)
        # self.position += v0t + at2
        # self.dest.topleft = self.position.int()
        #
        # self.vel += a * t
        #
        #
        # if (self.dest.bottom > self.system.camera.centery):
        #     self.dest.bottom = self.system.camera.centery
        #     old = self.vel
        #     self.vel *= 0.9
        #     self.vel.y *= -1
        #     print(old, '->', self.vel)

        self.color.r = (self.color.r + randrange(-10, 11)) % 256
        self.color.g = (self.color.g + randrange(-10, 11)) % 256
        self.color.b = (self.color.b + randrange(-10, 11)) % 256

    def render(self):
        self.system.draw_geom("filled_circle", x=self.dest.centerx,
                              y=self.dest.centery, r=self.dest.w // 2,
                              color=self.color)

    def on_collision(self, other_go):
        print("Colisao com", other_go)