from core.scene import Scene
from core import log

__loaded_scene = Scene()
__common_game_objects = Scene()


def load(scene: Scene):
    global __loaded_scene
    log.trace(f'Loading scene "{scene.__class__.__name__}"...')
    __loaded_scene = scene

    from .application import Application
    Application.get().redraw_screen()


def pre_update(delta_time: float):
    global __loaded_scene
    if __loaded_scene is not None:
        __loaded_scene.pre_update(delta_time)
    __common_game_objects.pre_update(delta_time)


def update(delta_time: float):
    global __loaded_scene
    if __loaded_scene is not None:
        __loaded_scene.update(delta_time)
    __common_game_objects.update(delta_time)


def event_hook(event):
    global __loaded_scene, __common_game_objects
    if __loaded_scene is not None:
        __loaded_scene.event_hook(event)
    __common_game_objects.event_hook(event)


def get_loaded_scene():
    global __loaded_scene
    return __loaded_scene


def get_common_game_objects():
    global __common_game_objects
    return __common_game_objects
