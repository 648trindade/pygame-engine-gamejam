from os.path import isdir
from os import listdir

import pygame
from pygame import image, mask
from engine.Point import Point

TEXTURE_PATH = "etc/img/"
SHARED_FOLDER = "shared/"
FORMATS_SUPPORTED = ("png", "bmp", "jpg")


class Texture:

    def __init__(self, game_dir):
        self.path = game_dir + TEXTURE_PATH
        self.surfaces = dict()
        self.masks = dict()
        self.load(SHARED_FOLDER)

    def load(self, folder):
        """
        Carrega todas as texturas de uma pasta
        :param folder: nome da pasta, localizada dentro de TEXTURE_PATH
        :return: None
        """
        if folder[-1] != '/':
            folder += "/"
        # se pasta existe e é realmente uma pasta
        if isdir(self.path + folder):
            files = listdir(self.path + folder)
            # pra cada arquivo na pasta
            for file in files:
                name = file[:-4]
                extension = file[-3:]
                # testa se a extensão é uma dessas 3
                if extension in FORMATS_SUPPORTED:
                    # carrega a imagem e põe no dicionario
                    self.surfaces[name] = image.load(self.path + folder + file).convert_alpha()
                    self.masks[name] = mask.from_surface(self.surfaces[name])

    def unload(self, folder):
        """
        Descarrega todas as texturas de uma pasta
        :param folder: nome da pasta, localizada dentro de TEXTURE_PATH
        :return: None
        """
        if folder[-1] != '/':
            folder += "/"
        # se pasta existe e é realmente uma pasta
        if isdir(self.path + folder):
            files = listdir(self.path + folder)
            # pra cada arquivo na pasta
            for file in files:
                name = file[:-4]
                extension = file[-3:]
                # testa se a extensão é uma dessas 3
                if extension in FORMATS_SUPPORTED:
                    # carrega a imagem e põe no dicionario
                    self.surfaces.pop(name)
                    self.masks.pop(name)

    def get(self, id):
        """
        Retorna a textura com o id correspondente. Se não houver, lança uma
        exceção
        :param id: ID (nome) da textura
        :return: pygame.Surface -> textura
        """
        if self.surfaces.get(id) is not None:
            return self.surfaces[id]
        else:
            raise Exception("Textura inexistente ou não carregada!")

    def get_size(self, id):
        return Point(self.surfaces.get(id).get_size())
