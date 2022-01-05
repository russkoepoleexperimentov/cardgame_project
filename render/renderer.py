from core import scene_manager
from core.game_object import GameObject


def render_scene(window):
    for game_object in scene_manager.loaded_scene.game_objects:
        if isinstance(game_object, GameObject):
            game_object.render(window)
