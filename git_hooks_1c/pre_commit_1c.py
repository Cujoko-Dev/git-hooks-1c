#! python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from parse_1c_build import Decompiler
from git_hooks_1c import __version__
from pathlib import Path
import re
import shutil
import subprocess
import sys


added_or_modified = re.compile('^\s*(?:A|M)\s+"?(?P<rel_name>[^"]*)"?')


def get_added_or_modified_files():
    result = []

    try:
        output = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8')
    except subprocess.CalledProcessError:
        return result

    for line in output.split('\n'):
        if line != '':
            match = added_or_modified.match(line)
            if match:
                added_or_modified_file = Path.cwd() / match.group('rel_name')
                if added_or_modified_file.name.lower() != 'readme.md':
                    result.append(added_or_modified_file)

    return result


def get_for_processing_files(files: list):
    result = []

    for file in files:
        if file.suffix.lower() in ['.epf', '.erf', '.ert', '.md']:
            result.append(file)

    return result


def decompile(files: list):
    result = []

    decompiler = Decompiler()

    for file in files:
        source_folder = file.parent / (file.stem + '_' + file.suffix[1:] + '_src')

        if not source_folder.exists():
            source_folder.mkdir(parents=True)
        else:
            shutil.rmtree(str(source_folder), ignore_errors=True)

        decompiler.parse(file, source_folder)

        result.append(source_folder)

    return result


def add_to_index(files: list):
    for file in files:
        exit_code = subprocess.check_call(['git', 'add', '--all', str(file)])
        if exit_code != 0:
            exit(exit_code)


def main():
    argparser = ArgumentParser()
    argparser.add_argument('-v', '--version', action='version', version='%(prog)s, ver. {}'.format(__version__))
    argparser.add_argument('--debug', action='store_true', default=False, help='if this option exists then debug mode '
                                                                               'is enabled')
    args = argparser.parse_args()

    if args.debug:
        import sys
        sys.path.append('C:\\Python34\\pycharm-debug-py3k.egg')

        import pydevd
        pydevd.settrace(port=10050)

    added_or_modified_files = get_added_or_modified_files()
    for_processing_files = get_for_processing_files(added_or_modified_files)
    if len(for_processing_files) == 0:
        exit(0)

    for_indexing_source_folders = decompile(for_processing_files)
    add_to_index(for_indexing_source_folders)


if __name__ == '__main__':
    sys.exit(main())