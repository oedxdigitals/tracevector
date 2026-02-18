import os
import sys
import importlib


def get_base_path():
    """
    Returns correct base path for:
    - normal Python execution
    - PyInstaller onefile binary
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def load_plugins(target_type):
    plugins = []

    base_path = get_base_path()
    plugin_path = os.path.join(base_path, "tvx", "plugins")

    if not os.path.isdir(plugin_path):
        print(f"[!] Plugin directory not found: {plugin_path}")
        return plugins

    for file in os.listdir(plugin_path):
        if not file.endswith(".py"):
            continue
        if file.startswith("_"):
            continue

        module_name = f"tvx.plugins.{file[:-3]}"

        try:
            mod = importlib.import_module(module_name)
        except Exception as e:
            print(f"[!] Failed to load plugin {file}: {e}")
            continue

        if getattr(mod, "PLUGIN_TYPE", None) == target_type:
            plugins.append(mod)

    return plugins

def list_all_plugins():
    all_plugins = []
    for t in ("phone", "ip", "email"):
        plugins = load_plugins(t)
        for p in plugins:
            all_plugins.append({
                "type": t,
                "name": getattr(p, "PLUGIN_NAME", "unknown"),
                "module": p.__name__
            })
    return all_plugins
