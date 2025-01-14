# -*- coding: utf-8 -*-
import sys
from pathlib import Path

from loguru import logger

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
    if not pre_commit_file_path.exists():
        logger.info("git-hooks-1c not installed")
        return

    try:
        pre_commit_file_path.unlink()

        logger.info("git-hooks-1c uninstalled")
    except Exception as exc:
        logger.exception(exc)
        sys.exit(1)


def add_subparser(subparsers) -> None:
    """Добавить подпарсер"""

    decs = "Uninstall hooks"

    subparser = subparsers.add_parser(
        Path(__file__).stem.replace("_", "-"),
        add_help=False,
        description=decs,
        help=decs,
    )

    subparser.set_defaults(func=run)

    subparser.add_argument(
        "-h",
        "--help",
        action="help",
        help="Show this help message and exit",
    )
