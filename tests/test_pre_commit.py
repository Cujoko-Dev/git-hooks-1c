import subprocess
from pathlib import Path

import pytest

from git_hooks_1c.pre_commit import (
    get_for_processing_file_paths,
    get_indexed_file_paths,
    remove_from_index,
)


def _git(repo_path: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


@pytest.fixture
def repo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    repo_path = tmp_path / "repo"
    repo_path.mkdir()
    _git(repo_path, "init")
    monkeypatch.chdir(repo_path)
    return repo_path


def test_pre_commit_1(repo: Path):
    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 0

    assert len(get_for_processing_file_paths(file_paths)) == 0


def test_pre_commit_2(repo: Path):
    file_path = repo / "notes.txt"
    file_path.write_text("hello", encoding="utf-8")
    _git(repo, "add", "notes.txt")

    file_paths = sorted(get_indexed_file_paths())
    assert len(file_paths) == 1
    assert file_paths[0] == Path("notes.txt")

    assert len(get_for_processing_file_paths(file_paths)) == 0


def test_pre_commit_3(repo: Path):
    text_path = repo / "notes.txt"
    text_path.write_text("hello", encoding="utf-8")

    ert_path = repo / "test.ert"
    ert_path.write_bytes(b"binary payload")

    _git(repo, "add", "notes.txt", "test.ert")

    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 2

    for_processing_file_paths = get_for_processing_file_paths(file_paths)
    assert len(for_processing_file_paths) == 1
    assert for_processing_file_paths[0] == Path("test.ert")


def test_pre_commit_4(repo: Path):
    text_path = repo / "notes.txt"
    text_path.write_text("hello", encoding="utf-8")

    ert_path = repo / "test.ert"
    ert_path.write_bytes(b"binary payload")

    _git(repo, "add", "notes.txt", "test.ert")

    file_paths = get_indexed_file_paths()
    for_processing_file_paths = get_for_processing_file_paths(file_paths)
    assert for_processing_file_paths == [Path("test.ert")]

    remove_from_index(for_processing_file_paths)

    file_paths = get_indexed_file_paths()
    assert len(file_paths) == 1
    assert file_paths[0] == Path("notes.txt")
