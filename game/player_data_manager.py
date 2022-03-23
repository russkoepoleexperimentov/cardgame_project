import json
import sqlite3
from pathlib import Path
from game import contstants
from game.contstants import DATABASE

ENCODING = 'utf-8'
_player_data = dict()


def commit():
    with open(contstants.PLAYER_STATS_FILE, 'w', encoding=ENCODING) as file:
        json.dump(_player_data, file, ensure_ascii=False, indent=2)


def load_defaults():
    global _player_data

    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    base_cards_data = cur.execute(f"SELECT * FROM base_cards").fetchall()
    cur.close()
    con.close()

    _player_data = {
        contstants.PD_CHESTS: 10
    }
    for nation, cards in base_cards_data:
        cards = list(map(lambda x: x.strip(), cards.split(',')))
        _player_data[nation] = cards
        unl = _player_data.get(contstants.PD_UNLOCKED_CARDS, [])
        unl.extend(cards)
        _player_data[contstants.PD_UNLOCKED_CARDS] = unl

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
