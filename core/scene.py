class Scene:
    def __init__(self):
        self.game_objects = []

    def event_hook(self, event):
        for game_object in self.game_objects:
            game_object.event_hook(event)

    def update_objects(self):
        for game_object in self.game_objects:
            game_object.update()

    def add_game_object(self, obj):
        self.game_objects.append(obj)