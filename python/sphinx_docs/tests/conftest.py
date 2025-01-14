import shutil
from pathlib import Path

import git
import pytest
from pytest_mock.plugin import MockerFixture
from .common import CreateGitDirFunc

@pytest.fixture(scope="session")
def test_file_path() -> Path:
    return Path(__file__).parent / "files"

@pytest.fixture()
def create_git_repo(
    tmp_path: Path,
    test_file_path: Path,
    mocker: MockerFixture,
) -> CreateGitDirFunc:
    def _create_git_repo() -> Path:
        # Create a temporary directory
        git_root = tmp_path / "opm-python-documentation"
        git_root.mkdir()
        repo = git.Repo.init(str(git_root))
        repo.git.checkout("-b", "master")
        index = repo.index
        # Copy the test files to the temporary directory
        test_files = [
            {"docstrings_common.json": "python"},
            {"docstrings_simulators.json": "python"},
            {"dune.module": ""},
            {"index.html": "python/sphinx_docs/docs/_build/master"},
        ]
        for file_info in test_files:
            # Copy the file to the destination directory, creating any necessary parent directories
            for filename, sub_dir in file_info.items():
                dest_dir = git_root / sub_dir
                dest_dir.mkdir(parents=True, exist_ok=True)
                dest_file = dest_dir / filename
                shutil.copy(test_file_path / filename, dest_file)
                index.add([str(dest_file)])
        author = git.Actor("opmuser", "opm.user@gmail.com")
        committer = author
        index.commit("Initial commit", author=author, committer=committer)
        return git_root
    return _create_git_repo
