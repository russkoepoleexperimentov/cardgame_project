import sqlite3
from core import config
from game.contstants import PLAYER_STATS_BASE, BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from game.button_sounds import ButtonSounds
from game.cards import card_manager
from core import scene_manager
from scenes.menu import MenuScene
from random import sample
from core.ui.layout_group import HorizontalLayoutGroup


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()
        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)
        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)
        self.back_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(40, 30),
                               size=Vector(150, 30), title=translate_string('ui.back'))
        self.back_btn.add_component(ButtonSounds)
        self.back_btn.on_click.add_listener(self.back)
        self.back_btn.label.set_font_size(25)
        self.add_game_object(self.back_btn)
        self.choice_label = Text(title=translate_string('ui.deck_choice'), align='center',
                            valign='middle', size=Vector(400, 30), position=Vector(483, 30))
        self.add_game_object(self.choice_label)
        self.soviet_btn = Button(size=Vector(350, 175),
                                 sprite=load_image('sprites/ui/soviet_flag.png'),
                                 position=Vector(222, 250))
        self.soviet_btn.add_component(ButtonSounds)
        self.soviet_btn.on_click.add_listener(self.soviet_choice)
        self.add_game_object(self.soviet_btn)
        self.soviet_label = Text(title=translate_string('soviet'), align='center', valign='middle',
                            size=Vector(350, 30), position=Vector(222, 450))
        self.add_game_object(self.soviet_label)
        self.germany_btn = Button(size=Vector(350, 175),
                             sprite=load_image('sprites/ui/germany_flag.png'),
                             position=Vector(774, 250))
        self.germany_btn.add_component(ButtonSounds)
        self.germany_btn.on_click.add_listener(self.germany_choice)
        self.add_game_object(self.germany_btn)
        self.germany_label = Text(title=translate_string('germany'), align='center',
                                  valign='middle', size=Vector(350, 30), position=Vector(774, 450))
        self.add_game_object(self.germany_label)

    def soviet_choice(self):
        self.my_deck = list(card_manager.deck_by_nation.get('soviet'))
        self.enemy_deck = sample(list(card_manager.cards_by_nation.get('germany')), k=15)
        self.load_game()

    def germany_choice(self):
        self.my_deck = list(card_manager.deck_by_nation.get('germany'))
        self.enemy_deck = sample(list(card_manager.cards_by_nation.get('soviet')), k=15)
        self.load_game()

    def load_game(self):
        self.remove_game_object(self.back_btn)
        self.remove_game_object(self.choice_label)
        self.remove_game_object(self.soviet_btn)
        self.remove_game_object(self.soviet_label)
        self.remove_game_object(self.germany_btn)
        self.remove_game_object(self.germany_label)

        self.my_cards_count = 15
        self.current_ammo = 0
        self.current_fuel = 0

        background_image = load_image('sprites/ui/my_deck_background.jpg')
        backline_icon = load_image('sprites/ui/backline.png')
        frontline_icon = load_image('sprites/ui/frontline.png')
        icon_size = Vector(50, 50)
        line_box_size = Vector(566, 108)
        card_size = Vector(75.6, 108)
        backside_image = load_image('sprites/card_face_back.png')
        deck_box_size = Vector(375, 108)

        enemy_backside_1 = Image(position=Vector(409.4, 10), size=card_size, sprite=backside_image)
        self.add_game_object(enemy_backside_1)

        enemy_backside_2 = Image(position=Vector(412.4, 13), size=card_size, sprite=backside_image)
        self.add_game_object(enemy_backside_2)

        enemy_backside_3 = Image(position=Vector(415.4, 16), size=card_size, sprite=backside_image)
        self.add_game_object(enemy_backside_3)

        self.enemy_deck_box = Image(position=Vector(495, 10), size=deck_box_size)
        self.enemy_deck_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.enemy_deck_box)

        self.enemy_backline_box = Image(position=Vector(400, 128), size=line_box_size,
                                        sprite=background_image)
        self.enemy_backline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.enemy_backline_box)

        self.enemy_backline_icon = Image(position=Vector(976, 155), size=icon_size,
                                         sprite=backline_icon)
        self.add_game_object(self.enemy_backline_icon)

        self.enemy_frontline_box = Image(position=Vector(400, 246), size=line_box_size,
                                         sprite=background_image)
        self.enemy_frontline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.enemy_frontline_box)

        self.enemy_fronline_icon = Image(position=Vector(976, 273), size=icon_size,
                                         sprite=frontline_icon)
        self.add_game_object(self.enemy_fronline_icon)

        self.black_line = Image(position=Vector(0, 364), size=Vector(1366, 10),
                                sprite=load_image('sprites/ui/black_line.jpg'))
        self.add_game_object(self.black_line)

        self.my_frontline_box = Image(position=Vector(400, 384), size=line_box_size,
                                      sprite=background_image)
        self.my_frontline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.my_frontline_box)

        self.my_frontline_icon = Image(position=Vector(976, 419), size=icon_size,
                                       sprite=frontline_icon)
        self.add_game_object(self.my_frontline_icon)

        self.my_backline_box = Image(position=Vector(400, 502), size=line_box_size,
                                     sprite=background_image)
        self.my_backline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.my_backline_box)

        self.my_backline_icon = Image(position=Vector(976, 529), size=icon_size,
                                      sprite=backline_icon)
        self.add_game_object(self.my_backline_icon)

        my_backside_1 = Image(position=Vector(409.4, 630), size=card_size, sprite=backside_image)
        self.add_game_object(my_backside_1)

        my_backside_2 = Image(position=Vector(412.4, 633), size=card_size, sprite=backside_image)
        self.add_game_object(my_backside_2)

        my_backside_3 = Image(position=Vector(415.4, 636), size=card_size, sprite=backside_image)
        self.add_game_object(my_backside_3)

        self.my_deck_box = Image(position=Vector(495, 630), size=deck_box_size)
        self.my_deck_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.my_deck_box)


    def back(self):
        scene_manager.load(MenuScene())
