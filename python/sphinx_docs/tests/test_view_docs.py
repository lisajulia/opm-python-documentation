import logging
import os
from click.testing import CliRunner
from _pytest.logging import LogCaptureFixture
from pytest_mock.plugin import MockerFixture
from opm_python_docs import view_docs
from .common import CreateGitDirFunc

def test_invoke(
    caplog: LogCaptureFixture,
    create_git_repo: CreateGitDirFunc,
    mocker: MockerFixture,
) -> None:
    caplog.set_level(logging.INFO)
    git_root = create_git_repo()
    os.chdir(git_root)
    mock_click_launch = mocker.patch("opm_python_docs.view_docs.click.launch")
    runner = CliRunner()
    args = ["--branch", "master"]
    result = runner.invoke(view_docs.main, args)
    assert result.exit_code == 0
    mock_click_launch.assert_called_once_with(
        f"file://{git_root}/python/sphinx_docs/docs/_build/master/index.html"
    )
