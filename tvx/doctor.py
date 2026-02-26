import platform
import sys

from tvx.plugin_loader import load_plugins
from tvx import __version__


def run_doctor():
    print("TRACEVECTOR Doctor\n")

    print(f"[+] Version: {__version__}")
    print(f"[+] Frozen binary: {getattr(sys, 'frozen', False)}")
    print(f"[+] Python: {sys.executable}")
    print(f"[+] Platform: {platform.system()} {platform.release()}")

    plugins = load_plugins()

    print(f"[+] Plugins detected: {len(plugins)}")

    for plugin in plugins:
        info = getattr(plugin, "PLUGIN_INFO", {})
        cmd = info.get("command", "unknown")
        name = info.get("name", "Unnamed Plugin")
        print(f"    - [{cmd}] {name}")

    print("\n[✓] Environment looks healthy")
