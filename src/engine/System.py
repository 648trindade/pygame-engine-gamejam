import pygame
import pygame.gfxdraw
import os
import sys
from engine.Point import Point
from engine.Scene import Scene
from engine.managers.Texture import Texture
from engine.managers.Font import Font
from engine.managers.TextureSpec import TextureSpec

# tamanho fake da tela. Todos os objetos pensam que a tela tem esse tamanho
SCREEN_SIZE = Point(1920, 1080)
WINDOW_SIZE = Point(960, 540)
GAME_NAME = "Jogo"
GAME_DIR = os.path.dirname(os.path.abspath(sys.argv[0])) + "/../"
WHITE_COLOR = (255, 255, 255)


class System:

    def __init__(self):
        pygame.init()

        # centraliza a janela no monitor
        os.environ['SDL_VIDEO_CENTERED'] = 'true'

        # cria a surface que o jogo enxerga, com o tamanho fake
        self.screen = pygame.Surface(SCREEN_SIZE)

        self.fullscreen = False

        # cria a janela
        self.window_size = None
        self.window = None
        self.scale = None
        self.screen_real_size = None
        self.offset = None
        self.set_window(WINDOW_SIZE)
        self.mouse_rel = None

        pygame.display.set_caption(GAME_NAME)
        # pygame.display.set_icon()

        # pilha de cenas
        self.scene_stack = list()

        # lista de eventos
        self.events = None

        # retângulo da câmera
        self.camera = pygame.Rect((0, 0), SCREEN_SIZE)
        self.camera_limits = pygame.Rect((0, 0), SCREEN_SIZE)
        self.camera_target = None

        # Gerenciador de Texturas
        self.textures = Texture(GAME_DIR)
        self.fonts = Font(GAME_DIR)
        self.texturespecs = TextureSpec(GAME_DIR)

        # Clock
        self.clock = pygame.time.Clock()
        self.delta_time = 0

    def __del__(self):
        """
        Encerra o sistema. Chamado quando python apaga o objeto System da memória
        :return: None
        """
        pygame.quit()

    def set_window(self, new_size):
        """
        Define um tamanho para a janela e calcula proporção da viewport
        :param new_size: novo tamanho da janela
        :return: None
        """
        if self.fullscreen:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            flags = pygame.NOFRAME
        self.window = pygame.display.set_mode(new_size, flags)
        self.window_size = Point(self.window.get_size())

        # Proporção em largura e altura da janela com relação ao tamanho fake
        proportion = Point(
            new_size.x / SCREEN_SIZE.x,
            new_size.y / SCREEN_SIZE.y
        )
        # Escolhe a menor taxa de proporção pra encaixar direitinho na tela
        self.scale = min(proportion.x, proportion.y)

        # tamanho real da tela que será renderizada, mantida a proporção da fake
        self.screen_real_size = (SCREEN_SIZE * self.scale).int()

        # offset de deslocamento da tela com relação ao início da janela (cria
        #  tarjas pretas)
        self.offset = (self.window_size - self.screen_real_size)//2

    def set_fullscreen(self, value):
        if self.fullscreen ^ value:
            self.fullscreen = value
            if self.fullscreen:
                self.set_window(Point(pygame.display.list_modes()[0]))
            else:
                self.set_window(self.window_size)

    def run(self):
        """
        Loop das cenas. Roda uma cena até que termine, então procura por novas
         cenas na pilha. Se não houver mais cenas, termina.
        :return: None
        """
        game_data = {
            'system': self,
            'screen_size': SCREEN_SIZE,
            'scene': None,
            'shared': dict()
        }

        while len(self.scene_stack) > 0:
            scene = self.scene_stack[-1] # topo da pilha
            game_data['scene'] = scene


            if scene.is_new():
                self.load_assets(scene.name)
                scene.start(game_data)
            elif scene.is_paused():
                scene.resume()

            if not scene.is_finished():
                scene.run()

            if scene.is_paused():
                scene.pause()
            elif scene.is_finished():
                scene.finish()
                self.unload_assets(scene.name)
                if scene == self.scene_stack[-1]: # se a cena estiver no topo
                    self.pop_scene()

    def update(self):
        """
        Atualiza o sistema. A cena ativa deve chamar esse método antes de
         qualquer outro update
        :return: None
        """
        # pega os eventos
        self.delta_time = self.clock.tick(60)
        self.mouse_rel = Point(pygame.mouse.get_rel()) / self.scale
        self.events = pygame.event.get()
        for event in self.events:
            if event.type is pygame.QUIT:
                for scene in self.scene_stack:
                    scene.state = Scene.STATE_FINISHED
            elif event.type is pygame.VIDEORESIZE:
                self.set_window(Point(event.size))

        if self.camera_target:
            self.move_camera(Point(self.camera_target.dest.center) - Point(self.camera.center))

        # limpa a tela
        self.window.fill(pygame.Color(0, 0, 0))
        self.screen.fill(pygame.Color(255, 255, 255))

    def render(self):
        """
        Renderiza a tela na janela. A cena ativa deve chamar esse método depois
         de todos os outros métodos render do jogo.
        :return: None
        """
        viewport = pygame.transform.scale(self.screen, self.screen_real_size)
        self.window.blit(viewport, self.offset)
        pygame.display.update()

    def blit(self, ID, dest, src=None, fixed=False, angle=0, scale=None):
        """
        Desenha uma surface na tela. Possui suporte para renderização
         independente da posição da câmera, como é o caso de menus. Se o tamanho
         de dest é diferente de src, há um redimensionamento.
        :param ID: ID da surface
        :param dest: Rect de destino na tela
        :param src: Rect de origem da surface
        :param fixed: Determina se a renderização é relativa a camera ou não
        :return: None
        """
        # Pega a textura do manager de texturas
        texture = self.textures.get(ID)

        # Se um retangulo de origem nao foi definido, pega o da textura
        if not src:
            src = texture.get_rect()
        # Se o retangulo de origem for difente do da textura, pega a porção
        elif src != texture.get_rect():
            texture = texture.subsurface(src)

        # Calcula tamanho de destino a partir de escala
        if scale is not None:
            if type(dest) is pygame.Rect:
                dest.size = Point(src.size) * scale
            else:
                dest = pygame.Rect(dest, Point(src.size) * scale)

        if not self.camera.colliderect(dest):
            # retangulo da imagem esta fora da camera
            return

        # Se a posição é relativa a câmera
        if not fixed:
            # Pega a posição relativa a câmera
            dest -= Point(self.camera.topleft)

        # se os retangulos de origem e destino tem tamanhos diferentes,
        #  redimensiona a imagem para o tamanho de destino
        if Point(src.size) != Point(dest.size):
            texture = pygame.transform.scale(texture, dest.size)

        # se necessitar rotacionar
        if angle % 360 != 0:
            texture = pygame.transform.rotate(texture, angle)
            src = texture.get_rect()
            src.center = dest.center
            dest = src

        # screen = pygame.Rect((0, 0), SCREEN_SIZE)
        # if not screen.contains(dest):
        #      clip_area = screen.clip(dest)
        #      src_area = clip_area - Point(dest.topleft)
        #      dest = clip_area
        #      texture = texture.subsurface(src_area)
        #      self.screen.blit(texture, dest.topleft, src_area)
        # else:
        #     self.screen.blit(texture, dest.topleft)

        self.screen.blit(texture, dest.topleft)

        # retorna o retangulo da tela que foi renderizado
        return dest

    def push_scene(self, scene):
        """
        Adiciona uma cena no topo da pilha
        :param scene: Cena nova
        :return: None
        """
        self.scene_stack.append(scene)

    def pop_scene(self):
        """
        Remove e retorna a cena no topo da pilha
        :return: Scene
        """
        n_scenes = len(self.scene_stack)
        if n_scenes > 0:
            return self.scene_stack.pop(n_scenes - 1)

    def swap_scene(self, scene):
        """
        Substitui a cena atualmente no topo da pilha pela cena fornecida.
        Retorna a cena removida.
        :param scene: Cena nova
        :return: Scene
        """
        old_scene = self.pop_scene()
        self.push_scene(scene)
        return old_scene

    def draw_font(self, text, font_name, size, destination, color=WHITE_COLOR,
                  centered=True, fixed=False):
        """
        Renderiza um texto e desenha na tela. Possui suporte para renderização
         independente da posição da câmera, como é o caso de menus.
        :param text: Texto a ser renderizado
        :param font_name: nome da fonte (com extensão) a ser renderizada
        :param size: tamanho da fonte
        :param destination: ponto de destino (centro)
        :param color: cor da fonte
        :param fixed: Determina se a renderização é relativa a camera ou não
        :return: None
        """
        texture = self.fonts.render(text, font_name, size, color)[0]
        src = texture.get_rect()
        dest = pygame.Rect(destination, src.size)
        if centered:
            dest.topleft = Point(dest.topleft) - Point(src.center)

        if not fixed:
            # Se alguma porção da surface está aparecendo na tela
            if self.camera.colliderect(dest):
                # Pega a posição relativa a câmera
                dest -= Point(self.camera.topleft)
            else:
                # retangulo da imagem esta fora da camera
                return
        self.screen.blit(texture, dest)

    def calculate_size_text(self, text, font_name, size):
        return self.fonts.render(text, font_name, size, (0, 0, 0))[0].get_rect()
        # src = self.fonts.render(text, font_name, size, (0, 0, 0))[1]
        # src.topleft = (0, 0)
        # return src

    def draw_geom(self, name, **kargs):

        if not kargs.get("fixed"):
            if kargs.get("rect"):
                kargs["rect"] -= Point(self.camera.topleft)
            elif kargs.get("x") and kargs.get("y"):
                kargs['x'] -= self.camera.x
                kargs['y'] -= self.camera.y

        if name == "rectangle":
            pygame.gfxdraw.rectangle(self.screen, kargs['rect'], kargs['color'])
        elif name == "box":
            pygame.gfxdraw.box(self.screen, kargs['rect'], kargs['color'])
        elif name == "circle":
            pygame.gfxdraw.circle(self.screen, kargs['x'], kargs['y'],
                                  kargs['r'], kargs['color'])
        elif name == "aacicle":
            pygame.gfxdraw.aacircle(self.screen, kargs['x'], kargs['y'],
                                    kargs['r'], kargs['color'])
        elif name == "filled_circle":
            pygame.gfxdraw.filled_circle(self.screen, kargs['x'], kargs['y'],
                                         kargs['r'], kargs['color'])

    def get_events(self):
        """
        Retorna uma cópia da lista de eventos ocorridos no frame
        :return:
        """
        return self.events.copy()

    def get_mouse_move(self):
        return self.mouse_rel

    def get_mouse_pos(self):
        return (Point(pygame.mouse.get_pos()) - self.offset) / self.scale

    def get_animation(self, image, name):
        return self.texturespecs.get(image, name)

    def get_image_size(self, image):
        return self.textures.get_size(image)

    def load_assets(self, name):
        self.textures.load(name)
        self.texturespecs.load(name)

    def unload_assets(self, name):
        self.textures.unload(name)
        self.texturespecs.unload(name)

    def register_last_frame(self):
        self.textures.surfaces['last_frame'] = pygame.Surface(SCREEN_SIZE)
        self.textures.surfaces['last_frame'].blit(self.screen, (0, 0))

    def move_camera(self, offset):
        self.camera.topleft += offset
        if not self.camera_limits.contains(self.camera):
            if self.camera.top not in range(self.camera_limits.top,
                                            self.camera_limits.bottom - self.camera.h):
                self.camera.top = min(self.camera_limits.bottom - self.camera.h,
                                      self.camera.top)
                self.camera.top = max(self.camera_limits.top, self.camera.top)
            if self.camera.left not in range(self.camera_limits.left,
                                             self.camera_limits.right - self.camera.w):
                self.camera.left = min(self.camera_limits.right- self.camera.w,
                                       self.camera.left)
                self.camera.left = max(self.camera_limits.left, self.camera.left)

    def reset_camera(self):
        self.camera.topleft = Point(0, 0)

