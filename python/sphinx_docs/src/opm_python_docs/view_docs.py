#! /usr/bin/env python3

import logging
import os

import click

from opm_python_docs import helpers


# CLI command: opmdoc-view-doc
#
# SHELL USAGE:
#
#  opmdoc-view-doc --branch <branch>
#
# DESCRIPTION:
#
#  View the generated sphinx documentation for the given branch in the default browser.
#  If the branch is not provided, the current git branch is used.
#
# EXAMPLES:
#
#  opmdoc-view-doc   # Opens index.html for the current git branch in the default browser
#
#
#
@click.command()
@click.option("--branch", type=str, help="Branch to view documentation for. If not provided, the current git branch is used.")
def main(branch: str|None) -> None:
    logging.basicConfig(level=logging.INFO)
    git_root_dir = helpers.get_git_root()
    branch = branch or helpers.get_current_branch()
    logging.info(f"Opening documentation for branch {branch}")
    url = f"file://{git_root_dir}/python/sphinx_docs/docs/_build/{branch}/index.html"
    click.launch(url)

if __name__ == '__main__':
    main()
