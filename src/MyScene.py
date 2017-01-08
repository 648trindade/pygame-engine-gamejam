from engine.Scene import Scene
from DebugInfo import DebugInfo
from MyCube import MyCube

class MyScene(Scene):
    def __init__(self):
        Scene.__init__(self, "MyScene")

    def start(self, game_data):
        self.game_objects.append(DebugInfo(game_data))
        self.game_objects.append(MyCube(game_data))

        Scene.start(self, game_data)
