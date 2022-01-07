

class Component:
    def __init__(self, owner):
        self.__game_object = owner
        self.start()

    def get_game_object(self):
        return self.__game_object

    def start(self):
        pass

    def update(self, delta_time):
        pass

    def event_hook(self, event):
        pass
