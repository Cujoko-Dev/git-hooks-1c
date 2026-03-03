import os
import shutil
from pathlib import Path

import pytest
from cjk_commons.zip import extract_from_zip

from git_hooks_1c.pre_commit import (
    get_for_processing_file_paths,
    get_indexed_file_paths,
    parse,
    remove_from_index,
)


@pytest.fixture()
def test(request):
    def clean():
        pass

    request.addfinalizer(clean)


def test_pre_commit_1(test):
    dir_path = Path(Path(__file__).parent, "data")
    file_archived_path = Path(dir_path, "1.zip")
    test_path = Path(dir_path, "1")
    if test_path.exists():
        shutil.rmtree(str(test_path))
    extract_from_zip(file_archived_path, test_path)

    os.chdir(test_path)

    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 0

    assert len(get_for_processing_file_paths(file_paths)) == 0


def test_pre_commit_2(test):
    dir_path = Path(Path(__file__).parent, "data")
    file_archived_path = Path(dir_path, "2.zip")
    test_path = Path(dir_path, "2")
    if test_path.exists():
        shutil.rmtree(str(test_path))
    extract_from_zip(file_archived_path, test_path)

    os.chdir(test_path)

    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 1

    assert len(get_for_processing_file_paths(file_paths)) == 0


def test_pre_commit_3(test):
    dir_path = Path(Path(__file__).parent, "data")
    file_archived_path = Path(dir_path, "3.zip")
    test_path = Path(dir_path, "3")
    if test_path.exists():
        shutil.rmtree(str(test_path))
    extract_from_zip(file_archived_path, test_path)

    os.chdir(test_path)

    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 2

    assert len(get_for_processing_file_paths(file_paths)) == 1


def test_pre_commit_4(test):
    dir_path = Path(Path(__file__).parent, "data")
    file_archived_path = Path(dir_path, "4.zip")
    test_path = Path(dir_path, "4")
    if test_path.exists():
        shutil.rmtree(str(test_path))
    extract_from_zip(file_archived_path, test_path)

    os.chdir(test_path)

    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 2

    for_processing_file_paths = get_for_processing_file_paths(file_paths)
    for_indexing_source_dir_paths = parse(for_processing_file_paths)

    assert len(for_indexing_source_dir_paths) == 1

    remove_from_index(for_processing_file_paths)

    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 1
