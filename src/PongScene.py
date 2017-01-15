from pygame import Color, Rect, mouse, Surface, gfxdraw
from random import random, choice
from engine import Scene, GameObject, Point, Physics
from DebugInfo import DebugInfo


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
            self.vel = Physics.reflect(self.vel, Point(0, 1 if self.dest.top < 0 else -1))

        if self.dest.left not in range(10, self.system.camera.right - self.dest.width - 10):
            self.scene.state = Scene.STATE_FINISHED
            self.system.swap_scene(GameOverScene(self.dest.left < 10))

    def render(self):
        self.system.draw_geom('filled_circle', r=10, x=self.dest.centerx, y=self.dest.centery, color=self.color)

    def on_collision(self, other_go):
        if other_go.has_tag('paddle'):
            #self.vel += other_go.vel
            #self.vel.y *= 10/self.vel.length()
            #self.vel.x *= -1
            self.vel = Physics.reflect(self.vel, other_go.normal)
            self.dest.left = min(self.screen_size.x - 10 - other_go.dest.width, self.dest.left)
            self.dest.left = max(10 + other_go.dest.width, self.dest.left)


class PongPaddle(GameObject):
    def __init__(self, center, game_data):
        GameObject.__init__(self, None, game_data)

        self.color = Color(0, 0, 0)
        self.dest = Rect(center - Point(10, 50), (20, 100))
        self._layer = 2
        self.vel = Point(0, 0)
        self.tags.append('paddle')
        self.normal = Point(0, 0)

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
        self.normal = Point(1, 0)

        PongPaddle.update(self)


class PongPaddlePlayer(PongPaddle):
    def update(self):
        move = self.system.get_mouse_pos()
        self.vel = Point(move) - Point(self.dest.center)
        self.vel = self.vel.normalize() * 10
        self.vel.x = 0
        self.normal = Point(-1, 0)

        PongPaddle.update(self)


class PongScene(Scene):

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


class GameOverScene(Scene):
    def __init__(self, win=False):
        Scene.__init__(self, "GameOver")
        self.text = "You Win!" if win else "Game Over"
        self.back = None

    def start(self, game_data):
        Scene.start(self, game_data)
        self.system.register_last_frame()

    def update(self):
        Scene.update(self)

        if mouse.get_pressed()[0]:
            self.state = Scene.STATE_FINISHED
            self.system.swap_scene(PongScene())

    def render(self):
        self.system.blit('last_frame', self.system.camera)
        self.system.draw_geom('box', rect=self.system.camera, color=(0,0,0,127))
        self.system.draw_font(self.text, "8bit16.ttf", 100, self.screen_size//2,
                              centered=True, fixed=True)