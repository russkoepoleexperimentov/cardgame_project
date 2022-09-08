import random
import pygame
from core import config
from game.cards import card_manager
from game.cards.card import face_back_index, CardInfo
from game.contstants import *
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from core.application import close as close_app
from game.button_sounds import ButtonSounds
from core import scene_manager
from game.game_scene import game_manager
from game.game_scene.card_line import CardLine, TYPE_ENEMY, TYPE_PLAYER, TYPE_PLAYER_HAND, \
    TYPE_ENEMY_HAND
from scenes.menu import MenuScene
from random import shuffle
from core.ui.layout_group import HorizontalLayoutGroup, VerticalLayoutGroup
from game.game_scene.game_card import GameCard
from game.game_scene.game_hero import GameHero
from scenes.game_end_scene import GameEndScene

ENEMY_TURN_MIN = 2
ENEMY_TURN_MAX = 5
enemy_turn_timer = 0

HERO_ICON_POS, HERO_ICON_SIZE = Vector(70, 100), Vector(100, 100)
HERO_ICON_BG = load_image('sprites/ui/slider_back.png')


class GameScene(Scene):
    def __init__(self):
        super(GameScene, self).__init__()
        game_manager.game_result = ''
        self.screen_w, self.screen_h = 1366, 768
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

        def make_flag(nation, position=Vector(), addgo=self.add_game_object, start=self.start_game):
            flag = Button(size=Vector(350, 175), position=position,
                          sprite=load_image(f'sprites/ui/{nation}_flag.png'))
            flag.add_component(ButtonSounds)
            flag.on_click.add_listener(lambda: start(nation))
            addgo(flag)
            lbl = Text(size=flag.get_size(), position=Vector(0, flag.get_size().y + 5),
                       title=translate_string(nation))
            lbl.block_raycasts = False
            lbl.set_parent(flag)
            return flag

        self.add_game_object(self.choice_label)

        self.soviet_flag = make_flag('soviet', position=Vector(222, 250 + 175))
        self.germany_flag = make_flag('germany', position=Vector(774, 250 + 175))
        self.english_flag = make_flag('english', position=Vector(222, 250 - 175))
        self.usa_flag = make_flag('usa', position=Vector(774, 250 - 175))

        self.game_menu_opened = False
        self.game_loaded = False

    def start_game(self, player_nation):
        bot_available_nations = list(card_manager.nations)
        bot_available_nations.remove(player_nation)
        enemy_nation = random.choice(bot_available_nations)
        game_manager.init_decks(player_nation, enemy_nation)
        self.load_game()

    def load_game(self):
        self.game_loaded = True
        self.remove_game_object(self.back_btn)
        self.remove_game_object(self.choice_label)
        self.remove_game_object(self.soviet_flag)
        self.remove_game_object(self.germany_flag)
        self.remove_game_object(self.english_flag)
        self.remove_game_object(self.usa_flag)

        background_image = load_image('sprites/ui/scroll_view_back.png')
        backline_icon = load_image('sprites/ui/backline.png')
        frontline_icon = load_image('sprites/ui/frontline.png')
        icon_size = Vector(50, 50)
        line_icon_pos = 1070
        line_box_w_padding = 200
        line_box_size = Vector(self.screen_w - line_box_w_padding * 2, 141.6)
        self.card_size = Vector(99.12, 141.6)
        self.backside_image = load_image('sprites/card_face_back.png')
        deck_box_size = Vector(456.88, 141.6)

        enemy_backside_1 = Image(position=Vector(1200, 70), size=self.card_size,
                                 sprite=self.backside_image)
        self.add_game_object(enemy_backside_1)

        enemy_backside_2 = Image(position=enemy_backside_1.position + Vector(3, 3),
                                 size=self.card_size,
                                 sprite=self.backside_image)
        self.add_game_object(enemy_backside_2)

        enemy_backside_3 = Image(position=enemy_backside_2.position + Vector(3, 3),
                                 size=self.card_size,
                                 sprite=self.backside_image)
        self.add_game_object(enemy_backside_3)

        self.enemy_deck_box = Image(position=Vector(self.screen_w // 2 - deck_box_size.x // 2,
                                                    -80.8),
                                    size=deck_box_size)
        self.enemy_deck_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.enemy_deck_box)

        self.enemy_backline_box = Image(position=Vector(line_box_w_padding, 70.8),
                                        size=line_box_size,
                                        sprite=background_image)
        self.enemy_backline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.enemy_backline_box)

        enemy_backline_icon = Image(position=Vector(line_icon_pos, 116.6), size=icon_size,
                                    sprite=backline_icon)
        enemy_backline_icon.block_raycasts = False
        self.add_game_object(enemy_backline_icon)

        self.enemy_frontline_box = Image(position=Vector(line_box_w_padding, 222.4),
                                         size=line_box_size,
                                         sprite=background_image)
        self.enemy_frontline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.enemy_frontline_box)

        enemy_frontline_icon = Image(position=Vector(line_icon_pos, 268.2), size=icon_size,
                                     sprite=frontline_icon)
        enemy_frontline_icon.block_raycasts = False
        self.add_game_object(enemy_frontline_icon)

        black_line = Image(position=Vector(0, 369), size=Vector(1366, 10),
                           sprite=load_image('sprites/ui/black_line.jpg'))
        self.add_game_object(black_line)

        self.my_frontline_box = Image(position=Vector(line_box_w_padding, 384), size=line_box_size,
                                      sprite=background_image)
        self.my_frontline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.my_frontline_box)

        my_frontline_icon = Image(position=Vector(line_icon_pos, 429.8), size=icon_size,
                                  sprite=frontline_icon)
        my_frontline_icon.block_raycasts = False
        self.add_game_object(my_frontline_icon)

        self.my_backline_box = Image(position=Vector(line_box_w_padding, 535.6), size=line_box_size,
                                     sprite=background_image)
        self.my_backline_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.my_backline_box)

        my_backline_icon = Image(position=Vector(line_icon_pos, 581.4), size=icon_size,
                                 sprite=backline_icon)
        my_backline_icon.block_raycasts = False
        self.add_game_object(my_backline_icon)

        my_backside = Image(position=Vector(1200, self.screen_h - 70 - self.card_size.y),
                            size=self.card_size,
                            sprite=self.backside_image)
        self.add_game_object(my_backside)

        self.my_deck_box = Image(position=Vector(self.screen_w // 2 - deck_box_size.x // 2, 687.2),
                                 size=deck_box_size)
        self.my_deck_box.add_component(HorizontalLayoutGroup)
        self.add_game_object(self.my_deck_box)

        self.end_turn_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(1200, 394),
                                   size=Vector(120, 50), title=translate_string('end_turn'))
        self.end_turn_btn.label.set_font_size(20)
        self.end_turn_btn.add_component(ButtonSounds)
        self.add_game_object(self.end_turn_btn)

        ammo_icon = Image(position=Vector(1200, 444), size=icon_size,
                          sprite=load_image('sprites/ui/ammo.png'))
        self.add_game_object(ammo_icon)

        game_manager.ui_player_ammo = Text(position=Vector(1270, 444), size=icon_size,
                                           valign='middle', title=str(0))
        self.add_game_object(game_manager.ui_player_ammo)

        fuel_icon = Image(position=Vector(1200, 504), size=icon_size,
                          sprite=load_image('sprites/ui/fuel.png'))
        self.add_game_object(fuel_icon)

        game_manager.ui_player_fuel = Text(position=Vector(1270, 504), size=icon_size,
                                           valign='middle', title=str(0))
        self.add_game_object(game_manager.ui_player_fuel)

        self.card_count_info = Text(size=self.card_size,
                                    title=str(len(game_manager.get_player_deck())), align='center',
                                    valign='middle', font_size=72)
        self.card_count_info.set_parent(my_backside)

        # enemy lines
        game_manager.enemy_second_line = self.enemy_backline_box.add_component(CardLine)
        game_manager.enemy_second_line.type = TYPE_ENEMY
        game_manager.enemy_first_line = self.enemy_frontline_box.add_component(CardLine)
        game_manager.enemy_first_line.type = TYPE_ENEMY

        # player lines
        game_manager.player_first_line = self.my_frontline_box.add_component(CardLine)
        game_manager.player_first_line.type = TYPE_PLAYER
        game_manager.player_second_line = self.my_backline_box.add_component(CardLine)
        game_manager.player_second_line.type = TYPE_PLAYER

        # hands
        game_manager.player_hand = self.my_deck_box.add_component(CardLine)
        game_manager.player_hand.type = TYPE_PLAYER_HAND
        game_manager.enemy_hand = self.enemy_deck_box.add_component(CardLine)
        game_manager.enemy_hand.type = TYPE_ENEMY_HAND

        # end turn
        self.end_turn_btn.on_click.add_listener(self.end_turn)

        # heroes
        enemy_hero = Image(position=HERO_ICON_POS,
                           size=HERO_ICON_SIZE,
                           sprite=HERO_ICON_BG)
        self.enemy_hero = game_manager.enemy_hero = enemy_hero.add_component(GameHero)
        self.enemy_hero.init(card_manager.hero_by_nation.get(game_manager.enemy_nation))
        self.add_game_object(enemy_hero)

        player_hero = Image(position=Vector(HERO_ICON_POS.x, self.screen_h - HERO_ICON_POS.y -
                                            HERO_ICON_SIZE.y),
                            size=HERO_ICON_SIZE,
                            sprite=HERO_ICON_BG)
        self.player_hero = game_manager.player_hero = player_hero.add_component(GameHero)
        self.player_hero.init(card_manager.hero_by_nation.get(game_manager.player_nation), True)
        self.add_game_object(player_hero)

        # start game
        self.prepare_game()
        self.player_turn()

    def prepare_game(self):
        game_manager.player_fuel = 0
        game_manager.player_ammo = 0

        game_manager.enemy_fuel = 0
        game_manager.enemy_ammo = 0

        shuffle(game_manager.get_player_deck())
        shuffle(game_manager.get_enemy_deck())

        for i in range(CARDS_AT_START):
            self.pick_player_card()

        for i in range(CARDS_AT_START):
            self.pick_enemy_card()

    def player_turn(self):

        global enemy_turn_timer
        enemy_turn_timer = random.randint(ENEMY_TURN_MIN, ENEMY_TURN_MAX)

        if game_manager.get_turn_count() <= PHASE1_DURATION_IN_TURNS:
            game_manager.player_ammo += PHASE1_AMMO_INCREASE
            game_manager.player_fuel += PHASE1_FUEL_INCREASE
        else:
            game_manager.player_ammo += PHASE2_AMMO_INCREASE
            game_manager.player_fuel += PHASE2_FUEL_INCREASE

        game_manager.ui_player_ammo.set_title(str(game_manager.player_ammo))
        game_manager.ui_player_fuel.set_title(str(game_manager.player_fuel))
        self.pick_player_card()

        for card in game_manager.player_first_line.get_game_object().get_children():
            card.get_component(GameCard).turn_tick()

        for card in game_manager.player_second_line.get_game_object().get_children():
            card.get_component(GameCard).turn_tick()

    def pick_player_card(self):
        if not game_manager.get_player_deck():
            return

        card_info = game_manager.get_player_deck().pop()
        card = card_info.build_card_object(card_width=self.card_size.x)
        game_card = card.add_component(GameCard)
        game_card.init(card_info, is_player=True)
        game_manager.player_hand.add_card(game_card)
        self.card_count_info.set_title(str(len(game_manager.get_player_deck())))

    def pick_enemy_card(self):
        if not game_manager.get_enemy_deck():
            return

        card_info = game_manager.get_enemy_deck().pop()
        card = card_info.build_card_object(card_width=self.card_size.x)
        card.get_child(face_back_index()).enabled = True
        game_card = card.add_component(GameCard)
        game_card.init(card_info, is_player=False)
        game_manager.enemy_hand.add_card(game_card)

    def enemy_turn(self):
        if game_manager.get_turn_count() <= PHASE1_DURATION_IN_TURNS:
            game_manager.enemy_ammo += PHASE1_AMMO_INCREASE
            game_manager.enemy_fuel += PHASE1_FUEL_INCREASE
        else:
            game_manager.enemy_ammo += PHASE2_AMMO_INCREASE
            game_manager.enemy_fuel += PHASE2_FUEL_INCREASE

        self.pick_enemy_card()

        for card in game_manager.enemy_first_line.get_game_object().get_children():
            card.get_component(GameCard).turn_tick()

        for card in game_manager.enemy_second_line.get_game_object().get_children():
            card.get_component(GameCard).turn_tick()

        cards_hand = game_manager.enemy_hand.get_game_object()
        cards = cards_hand.get_children()

        # pseudo AI

        # step 1 throw cards into table (if we can)
        def is_available(c: GameCard):
            info: CardInfo = c.get_card_info()
            return info.fuel_cost <= game_manager.enemy_fuel and \
                   info.ammo_cost <= game_manager.enemy_ammo

        while True:
            available_cards = [card for card in map(lambda go: go.get_component(GameCard), cards)
                               if is_available(card)]

            if not available_cards:
                break

            card = available_cards[0]
            line = random.randint(0, 1)  # first or second
            if line:
                game_manager.enemy_first_line.add_card(card)
            else:
                game_manager.enemy_second_line.add_card(card)
            card.get_game_object().get_child(face_back_index()).enabled = False

        # step 2 attack player
        def is_can_attack(c: GameCard):
            return c.can_attack and not c.attack_used

        cards = game_manager.enemy_second_line.get_game_object().get_children() +\
                game_manager.enemy_first_line.get_game_object().get_children()

        attack_cards = [card for card in map(lambda go: go.get_component(GameCard), cards)
                        if is_can_attack(card)]

        player_cards = game_manager.player_first_line.get_game_object().get_children()
        if not player_cards:
            player_cards = game_manager.player_second_line.get_game_object().get_children()

        player_cards = list(map(lambda go: go.get_component(GameCard), player_cards))

        player_first_line = game_manager.player_first_line.get_game_object()

        if not attack_cards:
            return

        for card in attack_cards:
            solution = random.random()
            if solution > 0.7 or not player_cards:
                # attack hero
                if player_first_line.child_count() == 0:
                    game_manager.player_hero.process_card(card)
            else:
                chosen_card: GameCard = random.choice(player_cards)
                chosen_card.process_card(card)

    def end_turn(self):
        game_manager.end_turn()
        if game_manager.is_player_turn():
            self.end_turn_btn.interactable = True
            self.player_turn()
        else:
            self.end_turn_btn.interactable = False

    def update(self, delta_time):
        super(GameScene, self).update(delta_time)

        if not game_manager.is_player_turn():
            global enemy_turn_timer
            if enemy_turn_timer > 0:
                enemy_turn_timer -= delta_time / 1000
            else:
                self.enemy_turn()
                self.end_turn()

        if game_manager.game_result:
            scene_manager.load(GameEndScene(game_manager.game_result == game_manager.GR_PLAYER_WIN))

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
