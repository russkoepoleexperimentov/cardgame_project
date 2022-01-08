import os
from core import log

key_value_pairs = {}

CONFIG_FILE_NAME = 'config.cfg'
KEY_VALUE_DELIMITER = ':'


def load_settings():
    log.trace('loading settings')
    load_defaults()

    if not os.path.isfile(CONFIG_FILE_NAME):
        save_settings()
        return

    file_stream = open(CONFIG_FILE_NAME, 'r')
    for line in file_stream.read().strip().split('\n'):
        key, value = line.split(KEY_VALUE_DELIMITER)
        key_value_pairs[key] = value
    file_stream.close()


def load_defaults():
    key_value_pairs['vid_mode'] = '1280x720'
    key_value_pairs['target_fps'] = '60'
    key_value_pairs['volume'] = '100'


def save_settings():
    file_stream = open(CONFIG_FILE_NAME, 'w')
    for key in key_value_pairs.keys():
        value = key_value_pairs.get(key)
        file_stream.write(f'{key}{KEY_VALUE_DELIMITER}{value}')
        file_stream.write('\n')
    file_stream.close()


def get_value(key, default=''):
    return str(key_value_pairs.get(key, default))
