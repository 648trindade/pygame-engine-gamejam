from pygame.sprite import Sprite
from pygame import Rect


class GameObject(Sprite):

    def __init__(self, name, *groups):
        Sprite.__init__(self, groups)

        self.image = name
        self.dest = Rect(0,0,0,0)
        self.src = Rect(0,0,0,0)
        self.fixed = False
        self.tags = list()

    def update(self):
        pass

    def render(self):
        pass

    def has_tag(self, tag):
        return tag in self.tags

    def on_collision(self, other_go):
        pass

    @property
    def rect(self):
        return self.dest