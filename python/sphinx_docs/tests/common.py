from typing import Protocol
from pathlib import Path

class CreateGitDirFunc(Protocol):  # pragma: no cover
    def __call__(self, add_config_ini: bool) -> Path:
        pass

