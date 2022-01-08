from core import scene_manager
from core.game_object import GameObject
from core.action import Action

on_render = Action()


def render_scene(window):
    all_game_objects = scene_manager.get_loaded_scene().get_game_objects() + \
                       scene_manager.get_common_game_objects().get_game_objects()
    for game_object in all_game_objects:
        if isinstance(game_object, GameObject):
            # render only root game objects (without parent)
            if game_object.get_parent() is None and game_object.enabled:
                game_object.render(window)

    global on_render
    on_render.invoke(window)
