import re
import shutil
import sys
from pathlib import Path

import fleep
from loguru import logger
from parse_1c_build import Parser
from plumbum import local

indexed_pattern = re.compile(r'^\s*[AM]\s+"?(?P<rel_name>[^"]*)"?')
bin_file_suffixes = [".epf", ".erf", ".ert", ".md"]
bin_file_to_check_suffixes = [".md"]

logger.disable(__name__)


def get_indexed_file_paths() -> list[Path]:
    result = []
    git = local["git"]
    try:
        output = git(
            "diff-index", "--ignore-submodules", "--name-status", "--cached", "HEAD"
        )
    except:
        output = git("status", "--ignore-submodules", "--porcelain")
    for line in output.split("\n"):
        if line != "":
            match = indexed_pattern.match(line)
            if match:
                indexed_file_path = Path(match.group("rel_name"))
                result.append(indexed_file_path)
    return result


def get_for_processing_file_paths(file_paths: list[Path]) -> list[Path]:
    result = []
    for file_path in file_paths:
        if file_path.suffix.lower() in bin_file_suffixes:
            if file_path.suffix.lower() in bin_file_to_check_suffixes:
                with file_path.open("rb") as file:
                    info = fleep.get(file.read(128))
                if info.type == ["document"]:
                    result.append(file_path)
            else:
                result.append(file_path)
    return result


def parse(file_paths: list[Path]) -> list[Path]:
    result = []
    parser = Parser()
    for file_path in file_paths:
        source_dir_path = Path(
            file_path.parent,
            file_path.stem + "_" + file_path.suffix[1:] + "_src",
        )
        if not source_dir_path.exists():
            source_dir_path.mkdir(parents=True)
        else:
            shutil.rmtree(source_dir_path)
        parser.run(file_path, source_dir_path)
        result.append(source_dir_path)
    return result


def add_to_index(dir_paths: list[Path]) -> None:
    git = local["git"]
    for dir_path in dir_paths:
        git("add", "--all", str(dir_path))


def remove_from_index(file_paths: list[Path]) -> None:
    git = local["git"]

    git("rm", "--cached", *[str(file_path) for file_path in file_paths])


def run(args) -> None:
    """Запустить"""

    logger.enable("cjk_commons")
    logger.enable("parse_1c_build")
    logger.enable(__name__)

    try:
        indexed_file_paths = get_indexed_file_paths()
        if len(indexed_file_paths) == 0:
            logger.info("no added or modified files")
            return

        for_processing_file_paths = get_for_processing_file_paths(indexed_file_paths)
        if len(for_processing_file_paths) == 0:
            logger.info("no for processing files")
            return

        for_indexing_source_dir_paths = parse(for_processing_file_paths)
        if len(for_indexing_source_dir_paths) == 0:
            logger.info("no for indexing source dirs")
            return

        add_to_index(for_indexing_source_dir_paths)

        if not args.keep_files:
            remove_from_index(for_processing_file_paths)
    except Exception as exc:
        logger.exception(exc)
        sys.exit(1)


def add_subparser(subparsers) -> None:
    """Добавить подпарсер"""

    decs = "Pre-commit for 1C:Enterprise files"

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
    subparser.add_argument(
        "-k",
        "--keep-files",
        action="store_true",
        help="Keep 1C-files in the index",
    )
