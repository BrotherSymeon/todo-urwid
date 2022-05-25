import logging

from clitodoapp.app.version import __version__
import tabulate
import urwid

from clitodoapp.ui import TodoUI, palette
from clitodoapp.models.todo import Todos, TodoData

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
                ["Description", args.new],
                ["Done", args.done],
                ["Priority", args.priority],
                ["Blocked", args.blocked],
            ]

            todos = Todos()
            todo = TodoData(desc=args.new, done=args.done, priority=args.priority)
            todos.save(todo)

            print("You todo was saved!")
            print(tabulate.tabulate(data))

        except Exception as e:
            LOG.error(e)
            print(e)

    else:
        # else
        # run the TUI
        todos = Todos()
        TodoUI(todos).start()
