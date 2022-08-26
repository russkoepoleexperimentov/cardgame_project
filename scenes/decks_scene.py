import pygame

from core import config
from core.resources import load_image
from core.scene import Scene
from core.ui.button import Button
from core.ui.image import Image
from core.ui.scroll_view import ScrollView
from core.ui.text import Text
from core.vector import Vector
from core.localization import translate_string
from game.button_sounds import ButtonSounds
from game.cards import card_manager
from game.cards.card import CardInfo
import textwrap

from game.contstants import BUTTON_DEFAULT_DESIGN

from core import scene_manager
from game.decks_scene.cards_list import SV_SLIDER_WIDTH, SV_SIDE_OFFSET, SV_TOP_OFFSET, \
    SV_BOTTOM_OFFSET, CardsList
from game.decks_scene.nation_buttons import BTN_SIZE, BTN_MARGIN, NationButtons


class DecksScene(Scene):
    def __init__(self):
        super(DecksScene, self).__init__()
        self.nations = ('soviet', 'germany')
        self.screen_w, self.screen_h = pygame.display.get_window_size()
        self.screen = Vector(self.screen_w, self.screen_h)

        background = Image(size=self.screen, sprite=load_image('sprites/ui/menu_blur.png'))
        self.add_game_object(background, -100)

        back_btn = Button(**BUTTON_DEFAULT_DESIGN,
                          position=Vector(40, 30),
                          size=BTN_SIZE,
                          title=translate_string('ui.back'))
        back_btn.add_component(ButtonSounds)
        back_btn.on_click.add_listener(self.load_menu)
        back_btn.label.set_font_size(25)
        self.add_game_object(back_btn, 150)

        self.switch_buttons_group = None
        self.scroll_view = None

        self.chosen_nation = ''

        self.exchanging_card = False
        self.exchanging_card_info = None
        self.exchanging_card_obj = None

        size = Vector(800, 600)
        self.info_wnd = Image(size=size, position=Vector((self.screen_w - size.x) // 2,
                                                         (self.screen_h - size.y) // 2),
                              sprite=load_image('sprites/ui/scroll_view_back.png'))
        self.add_game_object(self.info_wnd, 10)
        self.info_wnd.enabled = False

        Text(size=self.info_wnd.get_size(), title='Информация', align='center',
             position=Vector(0, 20)).set_parent(self.info_wnd)


        self.info_texts = []

        self.close_info = Button(**BUTTON_DEFAULT_DESIGN,
                                 position=Vector(self.info_wnd.get_size().x - BTN_SIZE.x - 40,
                                                 self.info_wnd.get_size().y - BTN_SIZE.y - 30),
                                 size=BTN_SIZE,
                                 title=translate_string('ui.close'))
        self.close_info.set_parent(self.info_wnd)
        def c(w=self.info_wnd):
            w.enabled = False
        self.close_info.on_click.add_listener(c)

        self.init_scroll_view()
        self.init_switch_buttons()

    def init_scroll_view(self):
        self.scroll_view = ScrollView(size=Vector(self.screen_w - 2 * SV_SIDE_OFFSET -
                                                  SV_SLIDER_WIDTH,
                                                  self.screen_h - SV_TOP_OFFSET - SV_BOTTOM_OFFSET),
                                      position=Vector(SV_SIDE_OFFSET, SV_TOP_OFFSET),
                                      background_sprite=
                                      load_image('sprites/ui/scroll_view_back.png'),
                                      slider_background_sprite=
                                      load_image('sprites/ui/slider_back.png'),
                                      slider_handle_sprite=
                                      load_image('sprites/ui/slider_handle.png'),
                                      slider_width=SV_SLIDER_WIDTH)
        self.add_game_object(self.scroll_view)
        self.cards_list = self.scroll_view.add_component(CardsList)

    def init_switch_buttons(self):
        self.switch_buttons_group = Image(size=Vector(self.screen_w - 2 * SV_SIDE_OFFSET -
                                                      SV_SLIDER_WIDTH,
                                                      BTN_SIZE.y),
                                          position=Vector(SV_SIDE_OFFSET, SV_TOP_OFFSET -
                                                          BTN_SIZE.y - BTN_MARGIN))
        self.add_game_object(self.switch_buttons_group)
        self.nations_buttons = self.switch_buttons_group.add_component(NationButtons)
        self.nations_buttons.set_cards_list(self.cards_list)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.load_menu()

    def load_menu(self):
        from scenes.menu import MenuScene
        card_manager.init()
        scene_manager.load(MenuScene())

    def show_info(self, card):
        self.info_wnd.enabled = True
        for t in self.info_texts:
            t.set_parent(None)

        for i, line in enumerate(textwrap.wrap(card.description, width=68)):
            t = Text(title=line)
            t.position=Vector(10, 70 + i * 25)
            t.set_parent(self.info_wnd)
            self.info_texts.append(t)

