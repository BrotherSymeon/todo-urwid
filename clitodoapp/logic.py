import logging

from clitodoapp.app.version import __version__
from clitodoapp.ui import TodoUI, Todos, Todo, palette
import tabulate
import urwid

LOG = logging.getLogger(__name__)


def run(parser) -> None:
    LOG.info(
        "hello from clitodoapp v%s",
        __version__,
    )
    args = parser.parse_args()

    # if the add command is one of the args
    if args.new:
        # add a todo
        try:
            data = [
                ['Description', args.new],
                ['Done', args.done],
                ['Priority', args.priority],
                ['Blocked', args.blocked],
            ]
            print("The following item will be created:")
            print("")
            print(tabulate.tabulate(data))
            todos = Todos('todos.db')
            todo = Todo(args.new)
            todo.done = int(args.done)
            todos.save(todo)

            print("You todo was saved!")
            print(tabulate.tabulate(data))

        except Exception as e:
            LOG.error(e)
            print(e)

    else:
        # else
        # run the TUI
        todos = Todos("todos.db")
        TodoUI(todos).start()
