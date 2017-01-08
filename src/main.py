from engine import System
from MyScene import MyScene

system = System()
scene = MyScene()
system.push_scene(scene)
system.run() # entra no laço principal do jogo
