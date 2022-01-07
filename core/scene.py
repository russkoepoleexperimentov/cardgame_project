from core.game_object import GameObject

class Scene:
    def __init__(self):
        self.__game_objects = dict()

    def event_hook(self, event):
        for game_object in self.__game_objects.keys():
            game_object.event_hook(event)

    def update(self, delta_time):
        for game_object in self.__game_objects.keys():
            game_object.update(delta_time)

    def sort_game_objects_by_priority(self):
        self.__game_objects = dict(sorted(self.__game_objects.items(), key=lambda item: item[1]))

    def has_game_object(self, obj: GameObject):
        return obj in self.__game_objects.keys()

    def add_game_object(self, obj: GameObject, priority=0):
        if not self.has_game_object(obj):
            self.__game_objects[obj] = priority
        else:
            raise ValueError(obj)
        self.sort_game_objects_by_priority()

    def update_game_object(self, obj: GameObject, priority=0):
        if self.has_game_object(obj):
            self.__game_objects[obj] = priority
        else:
            raise ValueError(obj)
        self.sort_game_objects_by_priority()

    def remove_game_object(self, obj: GameObject):
        if self.has_game_object(obj):
            del self.__game_objects[obj]
        else:
            raise ValueError(obj)
        self.sort_game_objects_by_priority()
