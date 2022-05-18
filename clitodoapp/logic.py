import logging

from clitodoapp.app.version import __version__
from clitodoapp.ui import TodoUI, Todos, palette

import urwid

LOG = logging.getLogger(__name__)


def run(parser) -> None:
    LOG.info(
        "hello from clitodoapp v%s",
        __version__,
    )
    todos = Todos("todos.db")
    TodoUI(todos).start()
