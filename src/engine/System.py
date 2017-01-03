import pygame
import os
import sys
from engine.Point import Point
from engine.Scene import Scene
from engine.managers.Texture import Texture

# tamanho fake da tela. Todos os objetos pensam que a tela tem esse tamanho
SCREEN_SIZE = Point(1920, 1080)
GAME_NAME = "Jogo"
GAME_DIR = os.path.dirname(os.path.abspath(sys.argv[0]))


class System:

    def __init__(self):
        pygame.init()

        # centraliza a janela no monitor
        os.environ['SDL_VIDEO_CENTERED'] = 'true'

        # cria a surface que o jogo enxerga, com o tamanho fake
        self.screen = pygame.Surface(SCREEN_SIZE)

        # cria a janela
        self.window_size = None
        self.window = None
        self.scale = None
        self.screen_real_size = None
        self.offset = None
        self.set_window(Point(800, 600))

        pygame.display.set_caption(GAME_NAME)
        # pygame.display.set_icon()

        # pilha de cenas
        self.scene_stack = list()

        # lista de eventos
        self.events = None

        # retângulo da câmera
        self.camera = pygame.Rect((0,0), SCREEN_SIZE)

        # Gerenciador de Texturas
        self.textures = Texture()

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
        self.window = pygame.display.set_mode(new_size, pygame.HWACCEL | pygame.RESIZABLE)
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

    def run(self):
        """
        Loop das cenas. Roda uma cena até que termine, então procura por novas
         cenas na pilha. Se não houver mais cenas, termina.
        :return: None
        """
        game_data = {'system': self}

        while len(self.scene_stack) > 0:
            scene = self.scene_stack[-1] # topo da pilha

            if scene.is_new():
                scene.start(game_data)
            elif scene.is_paused():
                scene.resume()

            if not scene.is_finished():
                scene.run()

            if scene.is_paused():
                scene.pause()
            elif scene.is_finished():
                scene.finish()
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
        self.events = pygame.event.get()
        for event in self.events:
            if event.type is pygame.QUIT:
                for scene in self.scene_stack:
                    scene.state = Scene.STATE_FINISHED
            elif event.type is pygame.VIDEORESIZE:
                self.set_window(Point(event.size))

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
        :param scene: Cena nova
        :return: None
        """
        self.pop_scene()
        self.push_scene(scene)

    def get_events(self):
        """
        Retorna uma cópia da lista de eventos ocorridos no frame
        :return:
        """
        return self.events.copy()

    def blit(self, ID, dest, src=None, fixed=False):
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
        # Se a posição é relativa a câmera
        if not fixed:
            # Se alguma porção da surface está aparecendo na tela
            if self.camera.colliderect(dest):
                # Pega a posição relativa a câmera
                _dest = dest - Point(self.camera.topleft)
                # se os retangulos de origem e destino tem tamanhos diferentes,
                #  redimensiona a imagem para o tamanho de destino
                if src and src.size != _dest.size:
                    texture = pygame.transform.scale(texture, _dest.size)
                self.screen.blit(texture, _dest, area=src)
        else:
            # se os retangulos de origem e destino tem tamanhos diferentes,
            #  redimensiona a imagem para o tamanho de destino
            if src and src.size != dest.size:
                texture = pygame.transform.scale(texture, dest.size)
            self.screen.blit(texture, dest, area=src)
