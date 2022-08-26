class Action:
    def __init__(self):
        self.__listeners = list()

    def add_listener(self, listener):
        self.__listeners.append(listener)

    def clear(self):
        self.__listeners.clear()

    def invoke(self, *args, **kwargs):
        for listener in self.__listeners:
            if listener is not None and callable(listener):
                listener(*args, **kwargs)
