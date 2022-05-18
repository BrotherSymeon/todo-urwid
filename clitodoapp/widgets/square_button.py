

import urwid

class SquareButton(urwid.Button):
    def __init__(self, *args, **kargs):
        self.left_button= "["
        self.right_button= "]"
        super(SquareButton, self).__init__(*args, **kargs)

