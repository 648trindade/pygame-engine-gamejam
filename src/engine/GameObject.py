from pygame.mask import Mask
from pygame.sprite import Sprite
from pygame import Rect, Surface

from engine.Animation import Animation


class GameObject(Sprite):

    def __init__(self, name, game_data, *groups):
        Sprite.__init__(self, groups)

        self.system = None
        self.screen_size = None
        self.scene = None
        self.shared = None

        self.alive = True
        self.updatable = True
        self.renderable = True
        self.id = name
        self.dest = Rect(0, 0, 0, 0)
        self.scale = None
        self.angle = 0
        self.fixed = False
        self.tags = list()
        self.animation = None
        self.rigid = False
        self.src = None
        self.animation_dict = dict()
        self.state = None
        self.current_animation_name = None

        if self.__dict__.get('animation_names'):
            for name in self.animation_names:
                self.animation_dict[name] = Animation(self.id, name, game_data)
            self.current_animation_name = self.animation_names[0]
            self.animation = self.animation_dict[self.current_animation_name]
            self.__dict__.pop('animation_names')

        self.__dict__.update(game_data)

    def __str__(self):
        return "<" + str(type(self).__name__) + " at " + \
               "({r.x}, {r.y}, {r.w}, {r.h})".format(r=self.dest) + ">"

    def update(self):
        if self.animation_dict.get(self.current_animation_name):
            self.animation = self.animation_dict[self.current_animation_name]

    def render(self):
        if self.animation:
            name = self.animation.render(self.dest, self.fixed, self.angle, self.scale)
            if name != self.current_animation_name:
                self.animation_dict[name].reset()
                self.current_animation_name = name
        else:
            self.system.blit(self.id, self.dest, self.src, self.fixed, self.angle, self.scale)


    def kill(self):
        self.alive = False
        self.updatable = False
        self.renderable = False
        Sprite.kill(self)

    def has_tag(self, tag):
        return tag in self.tags

    def on_collision(self, other_go):
        pass

    def set_state(self, new_state):
        self.state = new_state

    @property
    def rect(self):
        return self.dest

    @property
    def image(self):
        if self.id:
            if self.animation:
                return self.system.textures.get(self.id).subsurface(self.animation.get_src_size())
            else:
                return self.system.textures.get(self.id)
        else:
            return Surface(self.dest.size)

    @property
    def mask(self):
        if self.id:
            if self.animation:
                return self.animation.get_mask()
            else:
                return self.system.textures.masks[self.id]
        else:
            mask = Mask(self.dest.size)
            mask.fill()
            return mask
