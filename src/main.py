from engine import System, Scene

system = System()
scene = Scene("teste")
system.push_scene(scene)
system.run() # entra no laço principal do jogo
