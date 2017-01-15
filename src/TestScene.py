from engine import Scene
from DebugInfo import DebugInfo


class TestScene(Scene):
    def __init__(self):
        Scene.__init__(self, "MyScene")

    def start(self, game_data):
        self.game_objects.append(DebugInfo(game_data))
        for i in range(10):
            self.game_objects.append(MyCube(game_data))

        Scene.start(self, game_data)


from pygame import Rect, Color
from random import random, choice, randrange
from engine.GameObject import GameObject
from engine.Point import Point

class MyCube(GameObject):

    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)

        self.color = Color(127, 127, 127)

        self.radius = randrange(1,3)*25
        self.dest = Rect(randrange(0, self.screen_size.x),
                         randrange(0, self.screen_size.y),
                         self.radius*2, self.radius*2)
        self.vel  = Point(random() * choice([-1, 1]),
                          random() * choice([-1, 1]))
        self.vel.normalize()
        self.vel *= 100/self.radius
        self.position = Point(self.dest.topleft)
        self._layer = 1
        self.state = "running"

    def bounce(self, value):
        pass

    def update(self):
        if self.state == "killed":
            self.kill()
            return

        self.dest += self.vel
        if self.dest.left not in range(0, self.system.camera.right - self.dest.width):
            self.vel.x *= -1

        if self.dest.top not in range(0, self.system.camera.bottom - self.dest.height):
            self.vel.y *= -1

        self.color.r = (self.color.r + randrange(-10, 11)) % 256
        self.color.g = (self.color.g + randrange(-10, 11)) % 256
        self.color.b = (self.color.b + randrange(-10, 11)) % 256

    def render(self):
        self.system.draw_geom("filled_circle", x=self.dest.centerx,
                              y=self.dest.centery, r=self.radius,
                              color=self.color)

    def on_collision(self, other_go):
        if type(other_go) is MyCube:
            if other_go.radius < self.radius:
                self.radius += other_go.radius
                pos = self.dest.center
                self.dest.height = self.dest.width = self.radius*2
                self.dest.center = pos

                self.vel += other_go.vel
                self.vel.normalize()
                self.vel *= 100/self.radius
            elif self.radius < other_go.radius:
                self.state = "killed"