"""Helper that imports a project file by path, since the project folders contain hyphens."""

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_module(relative_path):
    path = ROOT / relative_path
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
