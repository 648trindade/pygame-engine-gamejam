import pygame
import os
import sys
from engine.Point import Point

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
        self.window_size = new_size
        self.window = pygame.display.set_mode(self.window_size, pygame.HWACCEL)

        # Proporção em largura e altura da janela com relação ao tamanho fake
        proportion = Point(
            new_size.x / SCREEN_SIZE.x,
            new_size.y / SCREEN_SIZE.y
        )
        # Escolhe a menor taxa de proporção pra não redimensionar errado
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
        self.events = pygame.event.get()

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