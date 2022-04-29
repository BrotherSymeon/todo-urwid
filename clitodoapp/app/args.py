import argparse


def get_arguments_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="based on urwid",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '--config_path',
        dest='config_path',
        type=str,
        help="path to config file",
    )

    parser.add_argument(
        '--config_section_name',
        dest='config_section_name',
        default=None,
        type=str,
        help="name of config section to use",
    )

    return parser
