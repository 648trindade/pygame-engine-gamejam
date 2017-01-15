from engine import System
from TestScene import TestScene
from PongScene import PongScene
from TextureTestScene import TextureTestScene

system = System()
#scene = TestScene()
scene = PongScene()
#scene = TextureTestScene()
system.push_scene(scene)
system.run() # entra no laço principal do jogo
