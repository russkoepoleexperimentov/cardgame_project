from core.scene import Scene
from core import log

__loaded_scene = Scene()


def load(scene: Scene):
    global __loaded_scene
    log.trace('loading scene...')
    __loaded_scene = scene


def update(delta_time: float):
    global __loaded_scene
    if __loaded_scene is not None:
        __loaded_scene.update(delta_time)


def event_hook(event):
    global __loaded_scene
    if __loaded_scene is not None:
        __loaded_scene.event_hook(event)


def get_loaded_scene():
    global __loaded_scene
    return __loaded_scene
