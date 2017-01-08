from pygame.sprite import Sprite
from pygame import Rect


class GameObject(Sprite):

    def __init__(self, name, *groups):
        Sprite.__init__(self, groups)

        self.image = name
        self.rect = Rect(0,0,0,0)
        self.src = Rect(0,0,0,0)
        self.fixed = False

    def update(self):
        pass

    def render(self):
        pass