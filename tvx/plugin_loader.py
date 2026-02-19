"""
TRACEVECTOR Plugin Loader
Pip-safe, package-based discovery
"""

import importlib
import pkgutil
from typing import List


PLUGIN_PACKAGE = "tvx.plugins"


def load_plugins(command: str) -> List[object]:
    plugins = []

    try:
        package = importlib.import_module(PLUGIN_PACKAGE)
    except ModuleNotFoundError:
        return plugins

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        try:
            module = importlib.import_module(f"{PLUGIN_PACKAGE}.{module_name}")
        except Exception:
            continue

        if hasattr(module, "COMMAND") and module.COMMAND == command:
            if hasattr(module, "Plugin"):
                plugins.append(module.Plugin())

    return plugins


def discover_plugins() -> List[str]:
    names = []

    try:
        package = importlib.import_module(PLUGIN_PACKAGE)
    except ModuleNotFoundError:
        return names

    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        names.append(module_name)

    return names
