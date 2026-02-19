# tvx/plugin_loader.py

import pkgutil
import importlib
import tvx.plugins

def load_all_plugins():
    plugins = []

    for _, module_name, _ in pkgutil.iter_modules(tvx.plugins.__path__):
        module = importlib.import_module(f"tvx.plugins.{module_name}")

        if hasattr(module, "PLUGIN_INFO") and hasattr(module, "run"):
            plugins.append(module)

    return plugins


def get_plugins_by_type(target_type):
    return [
        p for p in load_all_plugins()
        if p.PLUGIN_INFO.get("type") == target_type
    ]


def list_plugins():
    return load_all_plugins()
