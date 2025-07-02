from argparse import ArgumentParser

from cjk_commons.logging_ import add_logging_arguments

from git_hooks_1c import __version__, install, pre_commit, uninstall


def get_argparser() -> ArgumentParser:
    """Получить парсер командной строки"""

    parser = ArgumentParser(
        add_help=False,
        description="Git hooks utilities for 1C:Enterprise",
        prog="gh1c",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        help="Show version",
        version=f"%(prog)s, ver. {__version__}",
    )

    add_logging_arguments(parser)

    subparsers = parser.add_subparsers(dest="subparser_name")

    install.add_subparser(subparsers)
    pre_commit.add_subparser(subparsers)
    uninstall.add_subparser(subparsers)

    return parser
