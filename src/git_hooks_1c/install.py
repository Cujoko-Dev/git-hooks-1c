import sys
from pathlib import Path

from loguru import logger
from plumbum import local

logger.disable(__name__)


def run(args) -> None:
    """Запустить"""

    logger.enable("cjk_commons")
    logger.enable("parse_1c_build")
    logger.enable(__name__)

    hooks_dir_path = Path(".git", "hooks")
    if not hooks_dir_path.is_dir():
        logger.error("not a git repo")
        return

    pre_commit_file_path = Path(hooks_dir_path, "pre-commit")
    if pre_commit_file_path.exists() and not args.force:
        logger.info("git-hooks-1c already exist")
        return

    try:
        with pre_commit_file_path.open("w") as pre_commit_file:
            pre_commit_file.write("#!/bin/sh\n")
            pre_commit_file.write(
                f'gh1c pre-commit{" -a" if args.keep_files else ""}\n'
            )

        git = local["git"]
        git("config", "--local", "core.quotepath", "false")
        git("config", "--local", "core.longpaths", "true")

        logger.info("git-hooks-1c installed")
    except Exception as exc:
        logger.exception(exc)
        sys.exit(1)


def add_subparser(subparsers) -> None:
    """Добавить подпарсер"""

    decs = "Install hooks"

    subparser = subparsers.add_parser(
        Path(__file__).stem.replace("_", "-"),
        add_help=False,
        description=decs,
        help=decs,
    )

    subparser.set_defaults(func=run)

    subparser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Install hooks anyway",
    )
    subparser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit",
    )
    subparser.add_argument(
        "-k",
        "--keep-files",
        action="store_true",
        help="Keep 1C-files in the index",
    )
