import argparse
import textwrap


def get_arguments_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=textwrap.dedent(
            """\
            A todo app based on urwid
            ------------------------
                You can add a todo to the app from the 
                command line like this
            $ clitodoapp --new 'Go to the store' --done --priority high --blocked 'George stole my external hard drive. Please Help.'
                """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--config_path",
        dest="config_path",
        type=str,
        help="Path to config file.",
    )

    parser.add_argument(
        "--config_section_name",
        dest="config_section_name",
        default=None,
        type=str,
        help="Name of config section to use.",
    )

    parser.add_argument("--new", default=None, help="Add this for making a new todo.")
    parser.add_argument(
        "--blocked",
        default=None,
        help="The reason that it is blocked if it is blocked.",
    )
    parser.add_argument(
        "--done",
        action="store_true",
        help="Mark your todo as done if it is. Defaults to False.",
    )
    parser.add_argument(
        "--priority",
        choices=["high", "medium", "low"],
        default="medium",
        help="Mark your todo with a priority. Defaults to medium",
        type=str,
    )

    return parser
