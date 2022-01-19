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
PLAYER_STATS_BASE = 'data/player_stats.sqlite3'
