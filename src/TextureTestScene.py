from engine import Point, Scene, GameObject, Animation


class TextureTestScene(Scene):

    def __init__(self):
        Scene.__init__(self, "TextureTestScene")

    def start(self, game_data):
        # cria e adiciona um gato
        self.game_objects.append(Cat(game_data))

        Scene.start(self, game_data)


class Cat(GameObject):

    def __init__(self, game_data):
        GameObject.__init__(self, 'cat', game_data)

        # diz para pegar a animação standby da imagem cat
        self.animation = Animation(self.image, 'standby', game_data)
        # -1 torna o numero de loops infinito
        self.animation.num_loops = -1
        # tamanho de destino é igual ao de origem
        self.dest.size = self.animation.get_src_size()
        # desenha no meio da tela
        self.dest.topleft = self.screen_size//2 - Point(self.dest.size)//2