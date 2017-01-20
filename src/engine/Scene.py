from pygame.sprite import spritecollide, collide_mask
from engine.LayerRender import LayerRender
from engine import GameObject
from engine import Physics

class Scene:
    STATE_NEW = 1
    STATE_RUNNING = 2
    STATE_PAUSED = 3
    STATE_FINISHED = 4

    def __init__(self, name=None):
        """
        Construtor da cena. Classes derivadas devem chamar esse construtor
        :param name: Nome da cena
        """

        self.name = name if name else type(self).__name__
        self.state = Scene.STATE_NEW
        self.system = None
        self.screen_size = None
        self.shared = dict()
        self.game_objects = list()
        self.layers = LayerRender()
        self.event_queue = list()

    def start(self, game_data):
        """
        Inicia uma cena. Função chamada pela System. Dados do sistema são
         passados por aqui. Classes derivadas DEVEM chamar esse método
        :param game_data: dados do sistema
        :return: None
        """
        assert self == game_data['scene']
        self.__dict__.update(game_data)
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
        to_remove = []
        for go in self.game_objects:
            if go.updatable:
                go.update()
            if not go.alive:
                go.kill()
                to_remove.append(go)

        for event in self.event_queue:
            event['time'] -= self.system.delta_time
            if event['time'] <= 0:
                if callable(event['event']):
                    event['event']()
                to_remove.append(event)

        for obj in to_remove:
            if type(obj) is dict:
                self.event_queue.remove(obj)
            else:
                self.game_objects.remove(go)

        for go in self.game_objects:
            if go.updatable:
                collisions = spritecollide(go, self.layers, False)#, collide_mask)
                if collisions.count(go) > 0:
                    collisions.remove(go)
                for go_collided in collisions:
                    if go_collided.renderable:
                        go.on_collision(go_collided)

    def render(self):
        self.layers.draw(self.system)

    def get_gos_with_tag(self, tag):
        """
        Retorna todos os Game Objects que possuem a tag dad
        :param tag: tag
        :return: Lista de GameObjects
        """
        gos = list()
        for go in self.game_objects:
            if go.has_tag(tag):
                gos.append(go)
        return gos

    def get_nearest_go(self, origin, tag=None):
        """
        Retorna o game object mais proximo de uma posição
        :param origin: posição ou game object
        :param tag: tag do game object procurado (opcional)
        :return: game object ou None
        """
        distance = float('inf')
        nearest = None

        # testa se origin é um game object
        if GameObject in type(origin).mro():
            position = origin.rect.center
        else:
            position = origin

        # testa se tem uma tag e filtra os gos
        if tag:
            game_objects = self.get_gos_with_tag(tag)
        else:
            game_objects = self.game_objects
        game_objects.remove(origin)

        for go in game_objects:
            this_distance = Physics.distance_pt_rect(position, go.rect)
            if this_distance < distance:
                distance = this_distance
                nearest = go
        return nearest

    def get_gos_in_range(self, origin, range_, tag=None):
        """
        Retorna todos os game_objects dada uma distancia
        :param origin:
        :param range_:
        :param tag:
        :return:
        """
        # testa se origin é um game object
        if GameObject in type(origin).mro():
            position = origin.rect.center
        else:
            position = origin

        # testa se tem uma tag e filtra os gos
        if tag:
            game_objects = self.get_gos_with_tag(tag)
        else:
            game_objects = self.game_objects
        game_objects.remove(origin)

        gos = list()
        for go in game_objects:
            distance = Physics.distance_pt_rect(position, go.rect)
            if distance <= range_:
                gos.append(go)
        return gos


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

    def enqueue_event(self, event, time=0):
        self.event_queue.append({'event': event, 'time': time})