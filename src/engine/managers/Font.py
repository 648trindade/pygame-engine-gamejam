from os.path import isdir
from os import listdir
from pygame import freetype

FONTS_PATH = "etc/font/"

class Font:

    def __init__(self, game_dir):
        self.path = game_dir + FONTS_PATH
        self.fonts = dict()

    def render(self, text, font_name, size, color):
        if self.fonts.get(font_name) is None:
            self.fonts[font_name] = freetype.Font(self.path + font_name)

        return self.fonts[font_name].render(text, fgcolor=color, size=size)