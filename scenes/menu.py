from core.scene import Scene
from core.game_object import GameObject
from core.vector import Vector


class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        obj = GameObject()
        obj.position = Vector(100, 150)
        obj.size = Vector(10, 100)
        self.add_game_object(obj)
