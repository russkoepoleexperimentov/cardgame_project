class Action:
    def __init__(self):
        self.__listeners = []

    def add_listener(self, listener: callable):
        self.__listeners.append(listener)

    def invoke(self, *args, **kwargs):
        for listener in self.__listeners:
            if listener is not None and callable(listener):
                listener(*args, **kwargs)
