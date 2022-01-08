from core.component import Component
from core.resources import load_sound
from core.ui.button import Button
from core.ui import ui_manager


class ButtonSounds(Component):
    def __init__(self, owner: Button):
        super(ButtonSounds, self).__init__(owner)
        self.hover_sound = load_sound('sfx/ui/button_hover.wav')
        self.click_sound = load_sound('sfx/ui/button_click.wav')
        self.last_selected_ui = None
        self.get_game_object().on_click.add_listener(self.click_sound.play)

    def update(self, delta_time):
        super(ButtonSounds, self).update(delta_time)

        if ui_manager.get_selected() == self.get_game_object() and self.last_selected_ui != self.get_game_object():
            self.hover_sound.play()

        self.last_selected_ui = ui_manager.get_selected()

