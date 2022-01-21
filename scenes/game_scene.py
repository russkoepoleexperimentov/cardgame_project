import sqlite3
import pygame
from core import config
from core.components.drag_handler import DragHandler
from core.components.drop_handler import DropHandler
from game.contstants import PLAYER_STATS_BASE, BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from core.application import close as close_app
from game.button_sounds import ButtonSounds
from game.cards import card_manager
from core import scene_manager
from game.game_scene import game_manager
from game.game_scene.card_line import CardLine
from scenes.menu import MenuScene
from random import sample
from core.ui.layout_group import HorizontalLayoutGroup, VerticalLayoutGroup
from game.game_scene.game_card import GameCard


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

        self.game_menu_opened = False
        self.game_loaded = False

    def soviet_choice(self):
        self.my_deck = list(card_manager.deck_by_nation.get('soviet'))
        self.enemy_deck = sample(list(card_manager.cards_by_nation.get('germany')), k=15)
        self.load_game()

    def germany_choice(self):
        self.my_deck = list(card_manager.deck_by_nation.get('germany'))
        self.enemy_deck = sample(list(card_manager.cards_by_nation.get('soviet')), k=15)
        self.load_game()

    def load_game(self):
        self.game_loaded = True
        self.remove_game_object(self.back_btn)
        self.remove_game_object(self.choice_label)
        self.remove_game_object(self.soviet_btn)
        self.remove_game_object(self.soviet_label)
        self.remove_game_object(self.germany_btn)
        self.remove_game_object(self.germany_label)

        self.my_cards_count = 15
        self.my_ammo = 0
        self.turn_num = 0

        self.my_fuel = 0
        background_image = load_image('sprites/ui/my_deck_background.jpg')
        backline_icon = load_image('sprites/ui/backline.png')
        frontline_icon = load_image('sprites/ui/frontline.png')
        icon_size = Vector(50, 50)
        line_box_size = Vector(566, 141.6)
        self.card_size = Vector(99.12, 141.6)
        self.backside_image = load_image('sprites/card_face_back.png')
        deck_box_size = Vector(456.88, 141.6)

        enemy_backside_1 = Image(position=Vector(400, -80.8), size=self.card_size,
                                 sprite=self.backside_image)
        self.add_game_object(enemy_backside_1)

        enemy_backside_2 = Image(position=Vector(403, -77.8), size=self.card_size,
                                 sprite=self.backside_image)
        self.add_game_object(enemy_backside_2)

        enemy_backside_3 = Image(position=Vector(406, -74.8), size=self.card_size,
                                 sprite=self.backside_image)
        self.add_game_object(enemy_backside_3)

        self.enemy_deck_box = Image(position=Vector(509.12, -80.8), size=deck_box_size)
        self.enemy_deck_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.enemy_deck_box)

        self.enemy_backline_box = Image(position=Vector(400, 70.8), size=line_box_size,
                                        sprite=background_image)
        self.enemy_backline_box.add_component(HorizontalLayoutGroup)
        game_manager.enemy_second_line = self.enemy_backline_box.add_component(CardLine)
        game_manager.enemy_second_line.allow_add_cards = False
        self.add_game_object(self.enemy_backline_box)

        enemy_backline_icon = Image(position=Vector(976, 116.6), size=icon_size,
                                    sprite=backline_icon)
        self.add_game_object(enemy_backline_icon)

        self.enemy_frontline_box = Image(position=Vector(400, 222.4), size=line_box_size,
                                         sprite=background_image)
        self.enemy_frontline_box.add_component(HorizontalLayoutGroup)
        game_manager.enemy_first_line = self.enemy_frontline_box.add_component(CardLine)
        game_manager.enemy_first_line.allow_add_cards = False
        self.add_game_object(self.enemy_frontline_box)

        enemy_frontline_icon = Image(position=Vector(976, 268.2), size=icon_size,
                                     sprite=frontline_icon)
        self.add_game_object(enemy_frontline_icon)

        black_line = Image(position=Vector(0, 369), size=Vector(1366, 10),
                           sprite=load_image('sprites/ui/black_line.jpg'))
        self.add_game_object(black_line)

        self.my_frontline_box = Image(position=Vector(400, 384), size=line_box_size,
                                      sprite=background_image)
        self.my_frontline_box.add_component(HorizontalLayoutGroup)
        game_manager.player_first_line = self.my_frontline_box.add_component(CardLine)
        self.add_game_object(self.my_frontline_box)

        my_frontline_icon = Image(position=Vector(976, 429.8), size=icon_size,
                                  sprite=frontline_icon)
        self.add_game_object(my_frontline_icon)

        self.my_backline_box = Image(position=Vector(400, 535.6), size=line_box_size,
                                     sprite=background_image)
        self.my_backline_box.add_component(HorizontalLayoutGroup)
        game_manager.player_second_line = self.my_backline_box.add_component(CardLine)
        self.add_game_object(self.my_backline_box)

        my_backline_icon = Image(position=Vector(976, 581.4), size=icon_size, sprite=backline_icon)
        self.add_game_object(my_backline_icon)

        my_backside = Image(position=Vector(400, 687.2), size=self.card_size,
                            sprite=self.backside_image)
        self.add_game_object(my_backside)

        self.my_deck_box = Image(position=Vector(509.12, 687.2), size=deck_box_size)
        self.my_deck_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.my_deck_box)

        self.end_turn_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(1200, 394),
                                   size=Vector(120, 50), title=translate_string('end_turn'))
        self.end_turn_btn.label.set_font_size(20)
        self.end_turn_btn.on_click.add_listener(self.end_turn)
        self.end_turn_btn.add_component(ButtonSounds)
        self.add_game_object(self.end_turn_btn)

        ammo_icon = Image(position=Vector(1200, 444), size=icon_size,
                               sprite=load_image('sprites/ui/ammo.png'))
        self.add_game_object(ammo_icon)

        self.ammo_info = Text(position=Vector(1270, 444), size=icon_size, valign='middle',
                              title=str(self.my_ammo))
        self.add_game_object(self.ammo_info)

        fuel_icon = Image(position=Vector(1200, 504), size=icon_size,
                               sprite=load_image('sprites/ui/fuel.png'))
        self.add_game_object(fuel_icon)

        self.fuel_info = Text(position=Vector(1270, 504), size=icon_size, valign='middle',
                              title=str(self.my_fuel))
        self.add_game_object(self.fuel_info)

        self.card_count_info = Text(position=Vector(400, 687.2), size=Vector(99.12, 80.8),
                                    title=str(self.my_cards_count), align='center', valign='middle')
        self.add_game_object(self.card_count_info)

        self.my_turn()

    def my_turn(self):
        self.my_cards_count -= 3
        self.card_count_info.set_title(str(self.my_cards_count))
        self.turn_num += 1
        if self.turn_num <= 3:
            self.my_ammo += 1
            self.ammo_info.set_title(str(self.my_ammo))
        else:
            self.my_ammo += 2
            self.ammo_info.set_title(str(self.my_ammo))
            self.my_fuel += 1
            self.fuel_info.set_title(str(self.my_fuel))
        new_cards = sample(self.my_deck, k=3)
        for card_info in new_cards:
            card = card_info.build_card_object(card_width=self.card_size.x)
            game_card = card.add_component(GameCard)
            game_card.init(card_info)
            card.set_parent(self.my_deck_box)

        ########################################################################################

        new_cards = sample(self.enemy_deck, k=3)
        for card_info in new_cards:
            card = card_info.build_card_object(card_width=self.card_size.x)
            game_card = card.add_component(GameCard)
            game_card.init(card_info)
            game_manager.enemy_second_line.add_card(game_card)  # -=-=-===-=-=-=-

    def end_turn(self):
        pass

    def back(self):
        scene_manager.load(MenuScene())

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if not self.game_menu_opened and self.game_loaded:
                    self.game_menu_opened = True

                    self.menu_background = Image(size=Vector(300, 316), position=Vector(533, 226),
                                                 sprite=self.backside_image)
                    self.add_game_object(self.menu_background, 200)

                    game_menu = Image(size=Vector(260, 376), position=Vector(20, 20))
                    btn_box = game_menu.add_component(VerticalLayoutGroup)
                    btn_box.spacing = 20
                    game_menu.set_parent(self.menu_background)

                    menu_label = Text(size=BUTTONS_SIZE, title=translate_string('ui.menu'),
                                      align='center', valign='middle')
                    menu_label.set_parent(game_menu)

                    resume_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                        title=translate_string('resume'))
                    resume_btn.on_click.add_listener(self.resume)
                    resume_btn.add_component(ButtonSounds)
                    resume_btn.set_parent(game_menu)

                    exit_match_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                        title=translate_string('exit_match'))
                    exit_match_btn.on_click.add_listener(self.exit_match)
                    exit_match_btn.add_component(ButtonSounds)
                    exit_match_btn.set_parent(game_menu)

                    exit_game_btn = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                            title=translate_string('exit_game'))
                    exit_game_btn.on_click.add_listener(self.exit_game)
                    exit_game_btn.add_component(ButtonSounds)
                    exit_game_btn.set_parent(game_menu)

                elif self.game_menu_opened:
                    self.resume()

    def resume(self):
        self.remove_game_object(self.menu_background)
        self.game_menu_opened = False

    def exit_match(self):
        scene_manager.load(MenuScene())

    def exit_game(self):
        close_app()
