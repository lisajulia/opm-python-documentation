#! /usr/bin/env python3

import logging
import requests
import subprocess
from pathlib import Path

import click

URL_SIMULATORS = "https://raw.githubusercontent.com/OPM/opm-simulators/master/python/docstrings_simulators.json"
URL_COMMON = "https://raw.githubusercontent.com/OPM/opm-common/master/python/docstrings_common.json"
URL_DUNE_MODULE = "https://raw.githubusercontent.com/OPM/opm-simulators/master/dune.module"

def get_git_root() -> Path:
    """Return the absolute path of the opm-python-documentation repository's root."""
    try:
        output = subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"],
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError:
        # Handle the error if we're not inside a Git repo, etc.
        raise RuntimeError("Not a valid Git repository or other error occurred.")
    # Check that the parent directory is the opm-python-documentation repository
    root = output.decode("utf-8").strip()
    if not root.endswith("opm-python-documentation"):
        raise RuntimeError("Not in the opm-python-documentation repository.")
    return Path(root)

def convert_pr_to_commit_hash(repo: str, pr_number: int) -> str:
    """Convert a PR number to a commit hash."""
    url = f"https://api.github.com/repos/OPM/{repo}/pulls/{pr_number}"
    response = requests.get(url)
    response.raise_for_status()
    commit_hash = response.json()["head"]["sha"]
    return commit_hash

def download_docstring_file(url: str, pr_number: int|None) -> None:
    """Download a docstrings file from a URL (either opm-simulators or opm-common)."""
    if "opm-simulators" in url:
        repo = "opm-simulators"
        filename = "docstrings_simulators.json"
    else:
        repo = "opm-common"
        filename = "docstrings_common.json"
    if pr_number is not None:
        commit_hash = convert_pr_to_commit_hash(repo, pr_number)
        url = url.replace("/master/", f"/{commit_hash}/")
    logging.info(f"Downloading docstrings file from {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raises 404 if the file is not found
    git_root_dir = get_git_root()
    save_path = git_root_dir / "python" / filename
    with open(str(save_path), "wb") as file:
        file.write(response.content)
    logging.info(f"Saved docstrings file to {save_path}")

def download_dune_module() -> None:
    """Download the dune.module file from the opm-simulators repository."""
    logging.info("Downloading dune.module file")
    response = requests.get(URL_DUNE_MODULE)
    response.raise_for_status()
    git_root_dir = get_git_root()
    save_path = git_root_dir / "dune.module"
    with open(save_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Saved dune.module file to {save_path}")

# CLI command: opmdoc-download-files
#
# SHELL USAGE:
#
#  opmdoc-download-files --opm-simulators <pr-number> --opm-common <pr-number>
#
# DESCRIPTION:
#
#  Downloads the docstring JSON files from opm-simulators and opm-common. Also downloads
#  the dune.module from opm-simulators. By default, the files are downloaded from the
#  master branches. If a PR number is provided, the files are downloaded from the corresponding
#  PR branch.
#
# EXAMPLES:
#
#  opmdoc-download-files   # Downloads the docstrings files and dune.module file from master branches
#
#  opmdoc-download-files \
#     --opm-simulators 1234 \
#     --opm-common 5678 # Downloads the docstrings files from PR 1234 and 5678 and dune.module from master
#
#
@click.command()
@click.option("--opm-simulators", type=int, help="PR number for opm-simulators")
@click.option("--opm-common", type=int, help="PR number for opm-common")
def main(opm_simulators: int|None, opm_common: int|None) -> None:
    logging.basicConfig(level=logging.INFO)
    download_docstring_file(URL_SIMULATORS, pr_number=opm_simulators)
    download_docstring_file(URL_COMMON, pr_number=opm_common)
    download_dune_module()

if __name__ == '__main__':
    main()
