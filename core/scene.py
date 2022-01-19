from core.game_object import GameObject


class Scene:
    def __init__(self):
        self.__game_objects = dict()
        self.__game_objects_to_add = dict()
        self.__game_objects_to_remove = set()

    def event_hook(self, event):
        for game_object in self.__game_objects.keys():
            game_object.event_hook(event)

    def pre_update(self, delta_time):
        if len(self.__game_objects_to_remove) > 0:
            for obj in self.__game_objects_to_remove:
                del self.__game_objects[obj]
            self.__game_objects_to_remove.clear()
            self.sort_game_objects_by_priority()

        if len(self.__game_objects_to_add) > 0:
            for key in self.__game_objects_to_add:
                priority = self.__game_objects_to_add[key]
                self.__game_objects[key] = priority
            self.__game_objects_to_add.clear()
            self.sort_game_objects_by_priority()

        for game_object in self.__game_objects.keys():
            game_object.pre_update(delta_time)

    def update(self, delta_time):
        for game_object in self.__game_objects.keys():
            game_object.update(delta_time)

    def sort_game_objects_by_priority(self):
        self.__game_objects = dict(sorted(self.__game_objects.items(), key=lambda item: item[1]))

    def has_game_object(self, obj: GameObject):
        return obj in self.__game_objects.keys()

    def add_game_object(self, obj: GameObject, priority=0):
        if not self.has_game_object(obj):
            # self.__game_objects[obj] = priority
            self.__game_objects_to_add[obj] = priority
        else:
            raise ValueError(obj)

    def update_game_object(self, obj: GameObject, priority=0):
        if self.has_game_object(obj):
            self.__game_objects[obj] = priority
        else:
            raise ValueError(obj)
        self.sort_game_objects_by_priority()

    def remove_game_object(self, obj: GameObject):
        if self.has_game_object(obj):
            #del self.__game_objects[obj]
            self.__game_objects_to_remove.add(obj)
        else:
            raise ValueError(obj)

    def get_game_objects(self):
        return tuple(self.__game_objects)
