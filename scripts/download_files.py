#! /usr/bin/env python3

import logging
import requests
from pathlib import Path

URL_SIMULATORS = "https://raw.githubusercontent.com/OPM/opm-simulators/master/python/docstrings_simulators.json"
URL_COMMON = "https://raw.githubusercontent.com/OPM/opm-common/master/python/docstrings_common.json"
URL_DUNE_MODULE = "https://raw.githubusercontent.com/OPM/opm-simulators/master/dune.module"

def get_script_dir():
    """Return the directory of the script."""
    script_path = Path(__file__).resolve()
    script_dir = script_path.parent
    return script_dir

def convert_pr_to_commit_hash(repo: str, pr_number: str) -> str:
    """Convert a PR number to a commit hash."""
    url = f"https://api.github.com/repos/OPM/{repo}/pulls/{pr_number}"
    response = requests.get(url)
    response.raise_for_status()
    commit_hash = response.json()["head"]["sha"]
    return commit_hash

def download_docstring_file(url: str) -> None:
    """Download a docstrings file from a URL (either opm-simulators or opm-common)."""
    # Ask command line user question if to use master or PR branch
    if "opm-simulators" in url:
        repo = "opm-simulators"
        filename = "docstrings_simulators.json"
    else:
        repo = "opm-common"
        filename = "docstrings_common.json"
    print(f"Downloading docstrings file from {repo} repository. "
           "Should we use the master branch or a PR branch?")
    branch = input("Enter 'master' or a PR number: ")
    if branch == "master":
        url = url.replace("master", branch)
    else:
        pr_number = branch
        if not pr_number.isdigit():
            print("Invalid PR number.")
            return
        commit_hash = convert_pr_to_commit_hash(repo, pr_number)
        url = url.replace("master", commit_hash)
    logging.info(f"Downloading docstrings file from {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raises 404 if the file is not found
    script_dir = get_script_dir()
    save_path = script_dir.parent / "python" / filename
    with open(save_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Saved docstrings file to {save_path}")

def download_dune_module() -> None:
    """Download the dune.module file from the opm-simulators repository."""
    logging.info("Downloading dune.module file")
    response = requests.get(URL_DUNE_MODULE)
    response.raise_for_status()
    script_dir = get_script_dir()
    save_path = script_dir.parent / "dune.module"
    with open(save_path, "wb") as file:
        file.write(response.content)
    logging.info(f"Saved dune.module file to {save_path}")

def main() -> None:
    download_docstring_file(URL_SIMULATORS)
    download_docstring_file(URL_COMMON)
    download_dune_module()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
