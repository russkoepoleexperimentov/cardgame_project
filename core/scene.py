class Scene:
    def __init__(self):
        self.game_objects = []

    def update_objects(self):
        pass

    def add_game_object(self, obj):
        self.game_objects.append(obj)