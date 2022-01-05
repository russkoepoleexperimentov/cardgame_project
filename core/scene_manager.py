from core.scene import Scene
from core import log

loaded_scene = Scene


def load(scene):
    if not isinstance(scene, Scene):
        raise TypeError()

    global loaded_scene
    log.trace('loading scene...')
    loaded_scene = scene
