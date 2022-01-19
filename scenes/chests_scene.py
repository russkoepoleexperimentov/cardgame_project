import sqlite3
from core import config
from game.contstants import DATABASE, BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE
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
from random import choice


class ChestsScene(Scene):
    def __init__(self):
        super(ChestsScene, self).__init__()
        self.card_on_screen = False
        self.con = sqlite3.connect(DATABASE)
        self.cur = self.con.cursor()
        self.screen_w, self.screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        self.screen = Vector(self.screen_w, self.screen_h)
        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)
        back_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(40, 30), size=Vector(150, 30),
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.back)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)
        chest = Image(sprite=load_image('sprites/ui/chest.png'), size=Vector(400, 400),
                      position=Vector(30, 120))
        self.add_game_object(chest)
        self.chest_count = self.cur.execute('SELECT chests_count FROM player_stats').fetchall()[0][0]
        self.chest_info = Text(position=Vector(60, 550), size=BUTTONS_SIZE,
                          title=translate_string('ui.chest_info') + ': ' + str(self.chest_count))
        self.add_game_object(self.chest_info)
        self.open_btn = Button(**BUTTON_DEFAULT_DESIGN, position=Vector(60, 580), size=BUTTONS_SIZE,
                          title=translate_string('ui.open'))
        self.open_btn.add_component(ButtonSounds)
        self.open_btn.on_click.add_listener(self.open_chest)
        self.add_game_object(self.open_btn)
        if self.chest_count == 0:
            self.open_btn.interactable = False

    def open_chest(self):
        self.chest_count -= 1
        if self.chest_count == 0:
            self.open_btn.interactable = False
        self.chest_info.set_title(translate_string('ui.chest_info') + ': ' + str(self.chest_count))
        if not self.card_on_screen:
            claim_info = Text(position=Vector(750, 150), size=BUTTONS_SIZE,
                              title=translate_string('ui.congratulations') + ':')
            self.add_game_object(claim_info)
        self.card_on_screen = True
        lock_cards = list(filter(lambda x: x.unlock == 'False', card_manager.game_cards))
        random_card_info = choice(lock_cards)
        card = random_card_info.build_card_object()
        card.position = Vector(800, 180)
        self.add_game_object(card)
        self.cur.execute(f'UPDATE cards SET unlock = "True" WHERE name = "{random_card_info.name}"')
        self.con.commit()


    def back(self):
        scene_manager.load(MenuScene())
