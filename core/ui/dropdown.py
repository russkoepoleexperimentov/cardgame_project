from core.action import Action
from core.ui.button import Button
from core.ui.image import Image
from core.vector import Vector


class Dropdown(Image):
    def __init__(self,
                 choices=('',),
                 **kwargs):
        super(Dropdown, self).__init__(**kwargs)

        self._button = Button(title=choices[0], **kwargs)
        self._button.position = Vector()
        self._button.parent = self
        self._button.on_click.add_listener(self.select_next)

        self._choices = choices

        self._current_choice = 0
        self._on_change_value = Action()

    @property
    def choices(self):
        return self._choices

    @choices.setter
    def choices(self, value):
        if len(value) <= 0:
            raise ValueError('Dropdown choices can\'t be with length == 0')
        self._choices = value
        self._current_choice = 0
        self._update_graphics()

    @property
    def value(self):
        return self._current_choice

    @property
    def on_change_value(self) -> Action:
        return self._on_change_value

    def select(self, index):
        if index < 0 or index >= len(self.choices):
            raise IndexError('Dropdown choice index out of range')

        self._current_choice = index
        self._on_change_value.invoke(self.value)
        self._update_graphics()

    def select_value(self, value):
        if value not in self.choices:
            raise KeyError(f'Dropdown choice \'{value}\' does not exist')

        self.select(self.choices.index(value))

    def _update_graphics(self):
        self._button.set_title(self.choices[self._current_choice])

    def select_next(self):
        next_choice = self._current_choice + 1
        if next_choice >= len(self.choices):
            next_choice = 0
        self.select(next_choice)
