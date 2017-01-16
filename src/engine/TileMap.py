import json
from pygame.rect import Rect
from engine import GameObject, Point
from engine.System import GAME_DIR

TEXTURESPEC_PATH = GAME_DIR + "etc/json/"


class TileMap:
    def __init__(self, name, game_data):
        self.game_data = game_data

        self.name = name
        self.layers = list()
        self.load_json(TEXTURESPEC_PATH + self.game_data['scene'].name + "/" + name + ".json")
        for layer in self.layers:
            self.game_data['scene'].layers.add(*layer, layer=self.layers.index(layer))

    def load_json(self, jsonfile):
        with open(jsonfile) as file:
            dic = json.load(file)

        self.width = dic['width']
        self.height = dic['height']
        self.tile_width = dic['tilewidth']
        self.tile_height = dic['tileheight']
        properties = dic['tilesets'][0]['tileproperties']

        #tileset = self.game_data['system'].texturespecs.specs[self.name]['tileset']
        tileset = self.load_tiles(dic['tilesets'][0])

        for layer in dic['layers']:
            self.load_layer(layer, tileset, properties)

    def load_tiles(self, tileset_dic):
        w = tileset_dic['tilewidth']
        h = tileset_dic['tileheight']
        num_tiles = tileset_dic['tilecount']
        tileset = list()
        for y in range(0, tileset_dic['imageheight'], h):
            for x in range(0, tileset_dic['imagewidth'], w):
                tileset.append(Rect(x, y, w, h))
                num_tiles -= 1
                if num_tiles is 0:
                    break
        return tileset

    def load_layer(self, layer, tileset, properties):
        tile_nums = layer['data']
        height = layer['height']
        width = layer['width']
        offset = Point(layer['x'], layer['y'])
        self.layers.append(list())
        for j in range(height):
            for i in range(width):
                tile_num = tile_nums[j * height + i]
                if tile_num:
                    go_tile = GameObject(self.name, self.game_data)
                    go_tile.src = tileset[tile_num - 1]
                    go_tile.dest = Rect(
                        Point(i * self.tile_width, j * self.tile_height) + offset,
                        go_tile.src.size
                    )
                    if properties.get(str(tile_num)):
                        go_tile.tags.append(properties[str(tile_num)]['tag'])
                        if properties[str(tile_num)].get('rigid'):
                            go_tile.rigid = properties[str(tile_num)]['rigid']
                    self.layers[-1].append(go_tile)

    def get_size(self):
        return Point(self.width * self.tile_width, self.height * self.tile_height)