from pygame.sprite import Sprite
from pygame import Rect


class GameObject(Sprite):

    def __init__(self, name, game_data, *groups):
        Sprite.__init__(self, groups)

        self.system = None
        self.screen_size = None
        self.scene = None
        self.shared = None

        self.image = name
        self.dest = Rect(0, 0, 0, 0)
        self.scale = None
        self.angle = 0
        self.fixed = False
        self.tags = list()
        self.animation = None
        self.rigid = False
        self.src = None
        self.__dict__.update(game_data)

    def __str__(self):
        return "<" + str(type(self).__name__) + " at " + \
               "({r.x}, {r.y}, {r.w}, {r.h})".format(r=self.dest) + ">"

    def update(self):
        pass

    def render(self):
        if self.animation:
            self.animation.render(self.dest, self.angle, self.scale)
        else:
            self.system.blit(self.image, self.dest, self.src, self.fixed, self.angle, self.scale)

    def has_tag(self, tag):
        return tag in self.tags

    def on_collision(self, other_go):
        pass

    @property
    def rect(self):
        return self.dest
