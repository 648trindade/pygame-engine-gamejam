from engine import Point


class Animation:
    """
    Classe representando uma animação
    """

    def __init__(self, image, name, game_data):
        self.__dict__.update(game_data)
        self.image = image
        self.index = 0
        self.num_loops = 1
        self.loops = 0
        self.time_passed = 0
        self.state = "running"

        # Pega as informações lidas do json
        ani_dict = self.system.get_animation(image, name)
        self.tiles = ani_dict['tiles']
        self.time_tile = ani_dict['time']

    def render(self, dest, angle=0, scale=None, fixed=False):
        if self.state == "running":
            self.time_passed += self.system.delta_time

            # atualiza indice da animação. Para se o número de loops atingir o maximo
            while self.time_passed >= self.time_tile:
                self.time_passed -= self.time_tile
                self.index += 1

                if self.index == len(self.tiles):
                    self.loops += 1
                    self.index = 0

                if self.loops == self.num_loops:
                    self.state = "finished"

        # desenha a animação
        src = self.tiles[self.index]
        self.system.blit(self.image, dest, src, fixed=fixed, angle=angle, scale=scale)

    def reset(self):
        self.index = 0
        self.loops = 0
        self.time_passed = 0
        self.state = "running"

    def pause(self):
        self.state = "paused"

    def resume(self):
        self.state = "running"

    def is_finished(self):
        return  self.state == "finished"

    def get_src_size(self):
        return Point(self.tiles[self.index].size)