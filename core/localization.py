import os
from csv import reader as csv_reader
from core.resources import DATA_PATH

__key_value_pairs = dict()


def load_localization(name: str):
    global __key_value_pairs
    __key_value_pairs = dict()
    fullname = os.path.join(DATA_PATH, name)
    with open(fullname, encoding='utf-8') as file_stream:
        reader = csv_reader(file_stream, delimiter=':', quotechar='"')
        for key, value in reader:
            __key_value_pairs[key.lower()] = value


def translate_string(key: str):
    if key is None:
        return ''
    return __key_value_pairs.get(key.lower(), key)
