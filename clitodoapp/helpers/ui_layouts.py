import urwid

class SimpleLayout:
    _palette = [
        ("banner", "black", "light gray"),
        ("selectable", "white", "black"),
        ("focus", "black", "light gray"),
    ]

    def __init__(self):
        self._body = self.body()
        self._loop = urwid.MainLoop(
            self._body, self._palette, unhandled_input=self.handle_keys
        )

    def reset_layout(self, widget):
        self._loop.widget = widget

    def body(self):
        raise Exception("you have to overload this")

    def handle_keys(self, key):
        raise Exception("you have to overload this")

    def start(self):
        self._loop.run()


