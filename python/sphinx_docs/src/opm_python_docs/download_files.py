#! /usr/bin/env python3

import logging
import requests
import subprocess
from pathlib import Path

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

def convert_pr_to_commit_hash(repo: str, pr_number: str) -> str:
    """Convert a PR number to a commit hash."""
    url = f"https://api.github.com/repos/OPM/{repo}/pulls/{pr_number}"
    response = requests.get(url)
    response.raise_for_status()
    commit_hash = response.json()["head"]["sha"]
    return commit_hash

def download_docstring_file(url: str) -> None:
    """Download a docstrings file from a URL (either opm-simulators or opm-common)."""
    if "opm-simulators" in url:
        repo = "opm-simulators"
        filename = "docstrings_simulators.json"
    else:
        repo = "opm-common"
        filename = "docstrings_common.json"
    print(f"Downloading docstrings file from {repo} repository. "
           "Should we use the master branch or a PR branch?")
    branch = input("Enter 'master' or a PR number: ")
    if branch != "master":
        pr_number = branch
        if not pr_number.isdigit():
            print("Invalid PR number.")
            return
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

def main() -> None:
    logging.basicConfig(level=logging.INFO)
    download_docstring_file(URL_SIMULATORS)
    download_docstring_file(URL_COMMON)
    download_dune_module()

if __name__ == '__main__':
    main()
