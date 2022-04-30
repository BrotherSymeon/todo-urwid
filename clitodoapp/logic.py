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
    todo_ui = TodoUI(todos)
    ui = todo_ui.draw_ui()
    loop = urwid.MainLoop(ui, palette, unhandled_input=todo_ui.handle_keys)
    loop.run()
