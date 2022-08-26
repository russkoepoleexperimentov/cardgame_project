import os
from core import log

from json import load

from core.vector import Vector

key_value_pairs = {}

CONFIG_FILE_NAME = 'config.cfg'
KEY_VALUE_DELIMITER = ':'


def _parse_vector(data, delimiter='x'):
    return Vector(*map(float, data.split(delimiter)))


class Config:
    main = None

    def __init__(self, path):
        with open(path, 'r') as file:
            self._raw_data = load(file)
        self._values = dict()

        self._parse_values()

    def _parse_values(self):
        parsers = {
            'float': float,
            'int': int,
            'vector': _parse_vector
        }

        self._values = dict()
        for data in self._raw_data:
            dtype = data['type']
            name = data['name']
            value = parsers[dtype](data['value'])
            self._values.update({name: value})

    def get(self, name, default=None):
        return self._values.get(name, default)

    @staticmethod
    def load_main():
        Config.main = Config(CONFIG_FILE_NAME)
        log.trace('Main config loaded')

    @staticmethod
    def get_value(name, default=None):
        return Config.main.get(name, default)
