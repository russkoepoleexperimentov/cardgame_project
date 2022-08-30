from core.localization import translate_string as _
from core.ui.dropdown import Dropdown


class Toggle(Dropdown):
    def __init__(self, **kwargs):
        super(Toggle, self).__init__(choices=(_('ui.off'), _('ui.on')), **kwargs)