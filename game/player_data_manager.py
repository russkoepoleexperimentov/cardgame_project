import json
from pathlib import Path
from game import contstants

ENCODING = 'utf-8'
_player_data = dict()


def commit():
    with open(contstants.PLAYER_STATS_FILE, 'w', encoding=ENCODING) as file:
        json.dump(_player_data, file, ensure_ascii=False, indent=2)


def load_defaults():
    global _player_data
    _player_data = contstants.PLAYER_DATA_DEFAULTS
    commit()


def init():
    file = Path(contstants.PLAYER_STATS_FILE)
    if not file.exists():
        load_defaults()

    global _player_data
    with open(contstants.PLAYER_STATS_FILE, 'r', encoding=ENCODING) as file:
        _player_data = json.load(file)


def get_player_data():
    return _player_data
