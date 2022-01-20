from core.component import Component
from core.ui.button import Button
from core.ui.image import Image
from core.vector import Vector
from game.cards.card import CardInfo
from game.contstants import BUTTON_DEFAULT_DESIGN
from core.localization import translate_string
swap_candidate: CardInfo = None
swap_candidate_obj: Image = None

SWAP_BUTTON_SIZE = Vector(200, 100 * 200 / 720)
SWAP_BUTTON_POS = Vector(0, 937 * 200 / 720)


class CardClickHandler(Component):
    def __init__(self, owner: Image):
        super(CardClickHandler, self).__init__(owner)

    def init(self, card_info, card_list, in_deck=False):
        self.button = Button(size=self.get_game_object().get_size())
        self.button.set_parent(self.get_game_object())

        if in_deck:
            def process_click():
                if not card_list.card_swapping:
                    return

                global swap_candidate
                card_list.swap_cards(card_info, swap_candidate)
                swap_candidate = None

            self.button.on_click.add_listener(process_click)
        else:

            self.swap_btn = Button(**BUTTON_DEFAULT_DESIGN,
                                   position=SWAP_BUTTON_POS,
                                   size=SWAP_BUTTON_SIZE,
                                   title=translate_string('swap'))

            def start_swap_operation(swap_btn=self.swap_btn):
                if card_list.card_swapping:
                    return

                swap_btn.enabled = False
                card_list.start_card_swap_operation()

            self.swap_btn.set_parent(self.button)
            self.swap_btn.on_click.add_listener(start_swap_operation)
            self.swap_btn.enabled = False

            def process_click(swap_btn=self.swap_btn, obj=self.get_game_object(), cinfo=card_info):
                if card_list.card_swapping:
                    return

                global swap_candidate, swap_candidate_obj
                if swap_candidate_obj:
                    swap_candidate_obj.get_component(CardClickHandler).swap_btn.enabled = False
                swap_btn.enabled = True
                swap_candidate = cinfo
                swap_candidate_obj = obj

            self.button.on_click.add_listener(process_click)
