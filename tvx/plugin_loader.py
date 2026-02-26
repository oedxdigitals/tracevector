import importlib
import pkgutil

import tvx.plugins


def load_plugins():
    plugins = []

    package = tvx.plugins
    package_path = package.__path__

    for _, module_name, _ in pkgutil.iter_modules(package_path):
        full_module_name = f"tvx.plugins.{module_name}"

        try:
            module = importlib.import_module(full_module_name)

            if hasattr(module, "PLUGIN_INFO") and hasattr(module, "run"):
                plugins.append(module)

        except Exception as e:
            print(f"[!] Failed to load plugin {module_name}: {e}")

    return plugins
