from pygame.sprite import spritecollide
from engine.LayeredUpdates import LayeredUpdates

class Scene:
    STATE_NEW = 1
    STATE_RUNNING = 2
    STATE_PAUSED = 3
    STATE_FINISHED = 4

    def __init__(self, name):
        """
        Construtor da cena. Classes derivadas devem chamar esse construtor
        :param name: Nome da cena
        """
        self.name = name
        self.state = Scene.STATE_NEW
        self.system = None
        self.game_objects = list()
        self.layers = LayeredUpdates()

    def start(self, game_data):
        """
        Inicia uma cena. Função chamada pela System. Dados do sistema são
         passados por aqui. Classes derivadas DEVEM chamar esse método
        :param game_data: dados do sistema
        :return: None
        """
        self.system = game_data['system']
        self.layers.add(*self.game_objects)

    def resume(self):
        """
        Resume uma cena. Classes derivadas podem sobreescrever esse método.
        :return: None
        """
        pass

    def pause(self):
        """
        Pausa uma cena. Classes derivadas podem sobreescrever esse método.
        :return: None
        """
        pass

    def finish(self):
        """
        Encerra uma cena. Classes derivadas podem sobreescrever esse método.
        :return: None
        """
        pass

    def run(self):
        """
        Loop principal da cena. Atualiza e renderiza tudo. Classes derivadas NÃO
        podem sobreescrever esse método
        :return: None
        """
        self.state = Scene.STATE_RUNNING

        while self.is_running():
            self.system.update()
            self.update()
            self.render()
            self.system.render()

    def update(self):
        for go in self.game_objects:
            collisions = spritecollide(go, self.layers, False)
            collisions.remove(go)
            for go_collided in collisions:
                go.on_collision(go_collided)

        for go in self.game_objects:
            go.update()

    def render(self):
        self.layers.draw(self.system)

    def is_new(self):
        """
        Diz se a cena recém foi criada
        :return: bool
        """
        return self.state is Scene.STATE_NEW

    def is_paused(self):
        """
        Diz se a cena está pausada
        :return: bool
        """
        return self.state is Scene.STATE_PAUSED

    def is_finished(self):
        """
        Diz se a cena está encerrada
        :return: bool
        """
        return self.state is Scene.STATE_FINISHED

    def is_running(self):
        """
        Diz se a cena está em execução
        :return: bool
        """
        return self.state is Scene.STATE_RUNNING