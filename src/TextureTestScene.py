import pygame
from pygame.rect import Rect

from DebugInfo import DebugInfo
from engine import Point, Scene, GameObject
from engine.Animation import Animation
from engine.TileMap import TileMap
from engine import Physics


class TextureTestScene(Scene):

    def __init__(self):
        Scene.__init__(self, "TextureTestScene")

    def start(self, game_data):
        # cria e adiciona um gato
        self.game_objects.append(Cat(game_data))
        self.game_objects.append(Grass(game_data))
        self.game_objects.append(Target(game_data))

        self.game_objects.append(DebugInfo(game_data))
        self.tilemap = TileMap('teste', game_data)
        Scene.start(self, game_data)

        self.system.camera_target = self.game_objects[-2]
        self.system.camera_limits.size = self.tilemap.get_size()

    def update(self):
        if not self.system.camera_target:
            self.system.camera_target = self.game_objects[0]
            self.game_objects[0].updatable = True
            self.game_objects[1].updatable = True
        Scene.update(self)


class Cat(GameObject):

    def __init__(self, game_data):
        self.animation_names = ['standby']
        GameObject.__init__(self, 'cat', game_data)

        # diz para pegar a animação standby da imagem cat
        # self.animation = Animation(self.id, 'standby', game_data)
        # -1 torna o numero de loops infinito
        # self.animation.num_loops = -1
        # tamanho de destino é igual ao de origem
        self.dest.size = self.animation.get_src_size()
        self.ground = 0
        self.vel = Point(0, 0)
        self.acel = Point(0, 2300)
        #self.system.camera_target = self
        self.move_rel = Point(0, 0)
        self.updatable = False

    def on_collision(self, other_go):
        # precisa rechecar a colisão se houve alguma modificação
        if other_go.rigid and other_go.dest.colliderect(self.dest):
            up = False
            horiz = False
            clip = other_go.dest.clip(self.dest)
            self.move_rel = -self.move_rel.int()
            self.dest.topleft += self.move_rel
            if clip.h > clip.w and self.move_rel.x != 0:
                normal = Point(self.move_rel.x / abs(self.move_rel.x), 0)
                horiz = True
            elif clip.w > clip.h and self.move_rel.y != 0:
                normal = Point(0, self.move_rel.y / abs(self.move_rel.y))
                up = normal.y == -1
            elif self.move_rel.x != 0 and self.move_rel.y != 0:
                normal = Point(self.move_rel.x / abs(self.move_rel.x),
                               self.move_rel.y / abs(self.move_rel.y)).normalize()
                up = normal.y == -1
            else:
                normal = Point(0, 0)
            self.vel = Physics.reflect(self.vel, normal) * 0.1

            if up and self.move_rel.length() <= 1 or self.ground and horiz:
                self.ground = 4

    def update(self):
        if not self.ground:
            if self.acel.y < 2300:
                self.acel.y += 2300
        else:
            self.ground -= 1

        if self.move_rel.y == self.move_rel.y:
            for event in self.system.get_events():
                if event.type is pygame.KEYDOWN and event.key == pygame.K_UP:
                    self.vel.y = -1000

        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.vel.x = -1000
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.vel.x = 1000
        else:
            self.vel.x = 0

        new_pos, self.vel = Physics.mruv(self.dest.topleft, self.vel,
                                         self.acel, self.system.delta_time)

        self.move_rel = new_pos - self.dest.topleft
        self.dest.topleft = new_pos

class Target(GameObject):

    def __init__(self, game_data):
        GameObject.__init__(self, None, game_data)
        self.renderable = False
        self.dest = Rect((500, 500), (0,0))
        self.vel = Point(200, 0)
        self.state = "direita"

    def update(self):
        self.dest.topleft += self.vel * self.system.delta_time / 200
        if self.state == "direita":
            if self.dest.x > 2000:
                self.state = "baixo"
                self.vel = Point(0, 200)
        elif self.state == "baixo":
            if self.dest.y > 2000:
                self.state = "esquerda"
                self.vel = Point(-200, 0)
        elif self.state == "esquerda":
            if self.dest.x < 500:
                self.state = "cima"
                self.vel = Point(0, -200)
        else:
            if self.dest.y < 500:
                self.system.camera_target = None
                self.kill()

        
class Grass(GameObject):

    def __init__(self, game_data):

        GameObject.__init__(self, "grass", game_data)
        self._layer = 2
        self.dest = Rect((0,0), (5000,1100))
        #self.scale = 1.5
        self.camera = self.system.camera.copy()
        self.updatable = False

    def update(self):
        self.dest = self.dest - (Point(self.system.camera.topleft) - self.camera.topleft) * 0.5
        self.camera = self.system.camera.copy()