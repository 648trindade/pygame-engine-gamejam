from os.path import isdir
from os import listdir
import json
from pygame import Rect

TEXTURESPEC_PATH = "etc/json/"
SHARED_FOLDER = TEXTURESPEC_PATH + "shared/"


class TextureSpec:
    def __init__(self, game_dir):
        self.path = game_dir + TEXTURESPEC_PATH
        self.specs = dict()
        self.load(SHARED_FOLDER)

    def load(self, folder):
        if folder[-1] != '/':
            folder += "/"
        # se pasta existe e é realmente uma pasta
        if isdir(self.path + folder):
            files = listdir(self.path + folder)
            # pra cada arquivo na pasta
            for file in files:
                name = file[:-5]
                extension = file[-4:]
                # testa se a extensão é uma dessas 3
                if extension == 'json':
                    # carrega o json e põe no dicionario
                    with open(self.path + folder + file) as jfile:
                        specs = json.load(jfile)
                        self.specs[name] = dict()

                    if not specs.get('version'):
                        # common
                        w = specs['tilewidth']
                        h = specs['tileheight']
                        num_tiles = specs['tilecount']
                        tiles = list()
                        for y in range(0, specs['height'], h):
                            for x in range(0, specs['width'], w):
                                tiles.append(Rect(x, y, w, h))
                                num_tiles -= 1
                                if num_tiles is 0:
                                    break

                        self.specs[name]['animations'] = dict()
                        for ani_name, value in specs['animations'].items():
                            self.specs[name]['animations'][ani_name] = {
                                'time': value['time'],
                                'tiles': [tiles[i] for i in value['tiles']],
                                'next': value.get('next')
                            }
                        self.specs[name]['tiles'] = tiles


    def unload(self, folder):
        """
        Descarrega todas as specs de uma pasta
        :param folder: nome da pasta, localizada dentro de TEXTURESPEC_PATH
        :return: None
        """
        if folder[-1] != '/':
            folder += "/"
        # se pasta existe e é realmente uma pasta
        if isdir(self.path + folder):
            files = listdir(self.path + folder)
            # pra cada arquivo na pasta
            for file in files:
                name = file[:-5]
                extension = file[-4:]
                # testa se a extensão é uma dessas 3
                if extension == 'json':
                    try:
                        self.specs.pop(name)
                    except:
                        pass # tentou descarregar tilemap

    def get(self, image, name):
        try:
            return self.specs[image]['animations'][name]
        except:
            raise Exception('Animação '+ name + ' de ' + image + 'não carregada!')