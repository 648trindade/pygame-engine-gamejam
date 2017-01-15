from engine import System
from MyScene import MyScene
from MyPong import MyPong

system = System()
#scene = MyScene()
scene = MyPong()
system.push_scene(scene)
system.run() # entra no laço principal do jogo
