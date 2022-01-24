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

CARDS_AT_START = 2

PHASE1_AMMO_INCREASE = 1
PHASE1_FUEL_INCREASE = 0
PHASE1_DURATION_IN_TURNS = 3

PHASE2_AMMO_INCREASE = 2
PHASE2_FUEL_INCREASE = 1

PD_SOVIET_DECK = 'soviet_deck'
PD_GERMANY_DECK = 'germany_deck'
PD_UNLOCKED_CARDS = 'unlocked_cards'
PD_CHESTS = 'chests_count'

PLAYER_DATA_DEFAULTS = {
    PD_SOVIET_DECK: ['Т-26',
                    'Рота НКВД',
                    'Т-34',
                    'Т-34-85',
                    'КВ-1',
                    'ИС-2',
                    'СУ-76',
                    'СУ-85',
                    'СУ-122',
                    'СУ-152',
                    'КВ-2',
                    'ИСУ-122',
                    'ИСУ-152',
                    'Ил-2',
                    'Ил-10'],
    PD_GERMANY_DECK: ['SS-Unternehmen',
                     'Pz.Kpfw. II',
                     'Panther',
                     'Tiger II',
                     'Panzerjäger I',
                     'Marder II',
                     'Wespe',
                     'Grille',
                     'Jagdpanzer IV',
                     'Hummel',
                     'sFH 18',
                     'Pak 36',
                     'Pak 40',
                     'Ju.87',
                     'Ju.188'],
    PD_UNLOCKED_CARDS: ['Т-26',
                        'Рота НКВД',
                        'Т-34',
                        'Т-34-85',
                        'КВ-1',
                        'ИС-2',
                        'СУ-76',
                        'СУ-85',
                        'СУ-122',
                        'СУ-152',
                        'КВ-2',
                        'ИСУ-122',
                        'ИСУ-152',
                        'Ил-2',
                        'Ил-10',
                        'SS-Unternehmen',
                        'Pz.Kpfw. II',
                        'Panther',
                        'Tiger II',
                        'Panzerjäger I',
                        'Marder II',
                        'Wespe',
                        'Grille',
                        'Jagdpanzer IV',
                        'Hummel',
                        'sFH 18',
                        'Pak 36',
                        'Pak 40',
                        'Ju.87',
                        'Ju.188'],
    PD_CHESTS: 10,
}
