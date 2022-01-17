import pygame

from core.scene import Scene
from core.ui.image import Image
from core.ui.scroll_view import ScrollView
from core.ui.button import Button
from core.ui.text import Text
from core.ui.layout_group import VerticalLayoutGroup, GridLayoutGroup
from core.vector import Vector
from core.resources import load_image
from core.application import close as close_app
from core.components.drag_handler import DragHandler
from core.components.drop_handler import DropHandler
from core.localization import translate_string
from core import config, scene_manager

from game import cursor
from game.button_sounds import ButtonSounds
from game.card import Card
from game.contstants import BUTTON_DEFAULT_DESIGN, BUTTONS_SIZE, BUTTONS_TOP_OFFSET
from scenes.decks_scene import DecksScene


class MenuScene(Scene):
    def __init__(self):
        super().__init__()

        cursor.init()

        screen_w, screen_h = tuple(map(int, config.get_value('vid_mode').split('x')))
        screen = Vector(screen_w, screen_h)
        buttons_holder = Image(position=Vector(screen_w // 2 -
                                               BUTTONS_SIZE.x // 2,
                                               BUTTONS_TOP_OFFSET))
        buttons_layout_group = buttons_holder.add_component(VerticalLayoutGroup)
        self.add_game_object(buttons_holder)

        background = Image(size=screen, sprite=load_image('sprites/ui/menu.png'))
        self.add_game_object(background, -100)

        self.game_title = Text(size=BUTTONS_SIZE, title=translate_string('game_name'),
                               align='center', valign='middle')
        self.game_title.set_parent(buttons_holder)

        start_button = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                              title=translate_string('ui.start'))
        start_button.set_parent(buttons_holder)
        start_button.add_component(ButtonSounds)

        decks_button = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                              title=translate_string('ui.decks'))
        decks_button.set_parent(buttons_holder)
        decks_button.add_component(ButtonSounds)
        decks_button.on_click.add_listener(self.load_decks_showroom)

        settings_button = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                                 title=translate_string('ui.settings'))
        settings_button.set_parent(buttons_holder)
        settings_button.add_component(ButtonSounds)
        settings_button.interactable = False

        exit_button = Button(**BUTTON_DEFAULT_DESIGN, size=BUTTONS_SIZE,
                             title=translate_string('ui.quit'))
        exit_button.set_parent(buttons_holder)
        exit_button.add_component(ButtonSounds)
        exit_button.on_click.add_listener(close_app)

        self.scroll_view = ScrollView(size=Vector(400, 400), position=Vector(25, 40),
                                      background_sprite=
                                      load_image('sprites/ui/scroll_view_back.png'),
                                      slider_background_sprite=
                                      load_image('sprites/ui/slider_back.png'),
                                      slider_handle_sprite=
                                      load_image('sprites/ui/slider_handle.png'))
        self.add_game_object(self.scroll_view)

        content = self.scroll_view.content
        layout_group = content.add_component(GridLayoutGroup)
        layout_group.cell_size = Vector(90, 100)
        layout_group.spacing = 10
        self.scroll_view.content_offset = Vector(10, 10)
        self.scroll_view.slider.set_value(0)
        content.set_size(content.get_size() - Vector(10, 10) * 2)

        for i in range(15):
            wtf = Image(size=Vector(100, 100), sprite=load_image('sprites/ui/slider_back.png'))
            wtf.set_parent(self.scroll_view.content)
            wtf2 = Image(size=Vector(25, 25), sprite=load_image('sprites/ui/slider_handle.png'))
            wtf2.set_parent(wtf)

        # drop_handle = exit_button.add_component(DropHandler)
        # drop_handle.on_drop.add_listener(lambda drag: print(drag))

        # test_drag_go = Image(size=Vector(100, 100),
        # position=Vector(50, 50), sprite=load_image('sprites/ui/button.png'))
        # test_drag_go.add_component(DragHandler)
        # self.add_game_object(test_drag_go)

    def event_hook(self, event):
        super().event_hook(event)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                close_app()

    def load_decks_showroom(self):
        scene_manager.load(DecksScene())
