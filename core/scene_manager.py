from core.scene import Scene
from core import log

loaded_scene = Scene()


def load(scene: Scene):
    global loaded_scene
    log.trace('loading scene...')
    loaded_scene = scene
