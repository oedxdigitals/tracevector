import importlib
import inspect

PLUGIN_MODULES = [
    "tvx.email",
    "tvx.phone",
    "tvx.ip",
]


def load_plugins():
    plugins = {}

    for module_path in PLUGIN_MODULES:
        try:
            module = importlib.import_module(module_path)

            # Look for a class with a run() method
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and hasattr(obj, "run"):
                    instance = obj()

                    # Use class attribute if available
                    plugin_name = getattr(instance, "name", module_path.split(".")[-1])

                    plugins[plugin_name] = instance

        except Exception:
            continue

    return plugins
