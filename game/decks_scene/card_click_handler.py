from core.component import Component
from core.ui.button import Button
from core.ui.image import Image
from core.vector import Vector
from game.cards.card import CARD_SIZE, BOTTOM_TEXT_POS, BOTTOM_TEXT_SIZE, CardInfo
from game.contstants import BUTTON_DEFAULT_DESIGN

swap_candidate: CardInfo = None
swap_candidate_obj: Image = None

SWAP_BUTTON_SIZE = Vector(CARD_SIZE.x, BOTTOM_TEXT_SIZE.y)
SWAP_BUTTON_POS = Vector(0, BOTTOM_TEXT_POS.y)


class CardClickHandler(Component):
    def __init__(self, owner: Image):
        super(CardClickHandler, self).__init__(owner)

    def init(self, card_info, in_deck=False):
        self.card_info = card_info
        if in_deck:
            pass
        else:
            self.button = Button(size=self.get_game_object().get_size())
            self.button.set_parent(self.get_game_object())

            self.swap_btn = Button(**BUTTON_DEFAULT_DESIGN,
                                   position=SWAP_BUTTON_POS,
                                   size=SWAP_BUTTON_SIZE,
                                   title='swap')
            self.swap_btn.set_parent(self.button)
            self.swap_btn.enabled = False

            def process_click(swap_btn=self.swap_btn, obj=self.get_game_object()):
                global swap_candidate, swap_candidate_obj
                if swap_candidate:
                    swap_candidate_obj.get_component(CardClickHandler).swap_btn.enabled = False
                swap_btn.enabled = True
                swap_candidate_obj = obj

            self.button.on_click.add_listener(process_click)
