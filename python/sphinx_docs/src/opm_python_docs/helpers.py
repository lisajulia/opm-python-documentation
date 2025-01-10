import subprocess
from pathlib import Path

def get_current_branch() -> str:
    """Return the current Git branch."""
    try:
        output = subprocess.check_output(
            ["git", "branch", "--show-current"],
            stderr=subprocess.STDOUT
        )
    except subprocess.CalledProcessError:
        # Handle the error if we're not inside a Git repo, etc.
        raise RuntimeError("Not a valid Git repository or other error occurred.")
    return output.decode("utf-8").strip()

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
