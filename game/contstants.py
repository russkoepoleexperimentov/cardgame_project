from core.resources import load_image
from core.vector import Vector

BUTTONS_SIZE = Vector(260, 54)
BUTTONS_TOP_OFFSET = 200

BUTTON_DEFAULT_DESIGN = {
    'sprite': load_image('sprites/ui/button.png'),
    'pressed_sprite': load_image('sprites/ui/button_p.png'),
    'selected_sprite': load_image('sprites/ui/button_s.png'),
    'disabled_sprite': load_image('sprites/ui/button_d.png'),
}

DATABASE = 'data/cards.sqlite3'
PLAYER_STATS_FILE = 'data/player_stats.json'

HERO_HIT_POINTS = 10

CARDS_AT_START = 2

PHASE1_AMMO_INCREASE = 6
PHASE1_FUEL_INCREASE = 5
PHASE1_DURATION_IN_TURNS = 3

PHASE2_AMMO_INCREASE = 10
PHASE2_FUEL_INCREASE = 7

PD_UNLOCKED_CARDS = 'unlocked_cards'
PD_CHESTS = 'chests_count'
