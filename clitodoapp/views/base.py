
class BaseView(object):
    """
    All application views will derive from BaseView

    """
    def __init__(self):
        self._body = None
        self._loop = None

    def start(self):
        self._loop.run()
