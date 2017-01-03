from pygame.sprite import Sprite
from pygame import Rect


class GameObject(Sprite):

    def __init__(self, name, *groups):
        Sprite.__init__(self, groups)

        self.image = name
        self.rect = Rect()
        self.src = Rect()
        self.fixed = False