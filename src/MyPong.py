from pygame import Color, Rect, mouse, Surface, gfxdraw
from random import random, choice
from engine.Scene import Scene
from DebugInfo import DebugInfo
from engine.GameObject import GameObject
from engine.Point import Point


class PongField(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)

        self.color = Color(127, 127, 127)
        self._layer = 1
        width = 5
        self.dest = Rect((self.screen_size.x - width) // 2, 0, width,
                         self.screen_size.y)

    def render(self):
        self.system.draw_geom('box', rect=self.dest, color=self.color)


class PongBall(GameObject):
    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)

        self.color = Color(255, 0, 0)
        self.dest = Rect(self.screen_size//2, (20, 20))
        self._layer = 2
        self.vel = Point(choice([-1, 1]),
                         random() * choice([-1, 1]))
        self.vel = self.vel.normalize()
        self.vel *= 10
        self.tags.append('ball')

    def update(self):
        self.dest.topleft += self.vel
        if self.dest.top not in range(0, self.system.camera.bottom - self.dest.height):
            self.vel.y *= -1

        if self.dest.left not in range(10, self.system.camera.right - self.dest.width - 10):
            self.scene.state = Scene.STATE_FINISHED
            self.system.swap_scene(GameOver(self.dest.left < 10))

    def render(self):
        self.system.draw_geom('filled_circle', r=10, x=self.dest.centerx, y=self.dest.centery, color=self.color)

    def on_collision(self, other_go):
        if PongPaddle in type(other_go).mro():
            self.vel += other_go.vel
            self.vel.y *= 10/self.vel.length()
            self.vel.x *= -1
            print('colided!')


class PongPaddle(GameObject):
    def __init__(self, center, game_data):
        GameObject.__init__(self, None, game_data)

        self.color = Color(0, 0, 0)
        self.dest = Rect(center - Point(10, 50), (20, 100))
        self._layer = 2
        self.vel = Point(0, 0)

    def update(self):
        self.dest.topleft = Point(
            max(0, min(self.dest.x + self.vel.x, self.screen_size.x - self.dest.width)),
            max(0, min(self.dest.y + self.vel.y, self.screen_size.y - self.dest.height))
        ).int()

    def render(self):
        self.system.draw_geom("box", rect=self.dest, color=self.color)


class PongPaddleIA(PongPaddle):
    def update(self):
        ball = self.scene.get_gos_with_tag('ball')[0]
        self.vel = Point(ball.dest.center) - Point(self.dest.center)
        self.vel = self.vel.normalize() * 10
        self.vel.x = 0

        PongPaddle.update(self)


class PongPaddlePlayer(PongPaddle):
    def update(self):
        move = self.system.get_mouse_pos()
        self.vel = Point(move) - Point(self.dest.center)
        self.vel = self.vel.normalize() * 10
        self.vel.x = 0

        PongPaddle.update(self)


class MyPong(Scene):

    def __init__(self):
        Scene.__init__(self, "MyPong")

    def start(self, game_data):
        self.game_objects.append(DebugInfo(game_data))
        self.game_objects.append(PongField(game_data))
        self.game_objects.append(PongBall(game_data))
        y_2 = game_data['screen_size'].y//2
        self.game_objects.append(PongPaddleIA(Point(20, y_2), game_data))
        self.game_objects.append(PongPaddlePlayer(Point(1900, y_2), game_data))

        Scene.start(self, game_data)


class GameOver(Scene):
    def __init__(self, win=False):
        Scene.__init__(self, "GameOver")
        self.text = "You Win!" if win else "Game Over"
        self.back = None

    def start(self, game_data):
        Scene.start(self, game_data)
        self.back = Surface(game_data['screen_size'])
        self.back.blit(self.system.screen, (0,0))
        gfxdraw.box(self.back, self.system.camera, (0,0,0,127))

    def update(self):
        Scene.update(self)

        if mouse.get_pressed()[0]:
            self.state = Scene.STATE_FINISHED
            self.system.swap_scene(MyPong())

    def render(self):
        # FIXME: não pode fazer essa linha ahsuehaseuh
        self.system.screen.blit(self.back, (0, 0))
        self.system.draw_font(self.text, "8bit16.ttf", 100, self.screen_size//2,
                              centered=True, fixed=True)