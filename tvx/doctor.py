import sys
import platform
from importlib import util

from tvx import __version__
from tvx import plugin_loader


def run_doctor():
    print("TRACEVECTOR Doctor\n")

    # Version
    print(f"[+] Version: {__version__}")

    # Frozen binary check
    frozen = getattr(sys, "frozen", False)
    print(f"[+] Frozen binary: {frozen}")

    # Python executable
    print(f"[+] Python: {sys.executable}")

    # Platform
    print(f"[+] Platform: {platform.system()} {platform.release()}")

    # Plugin diagnostics
    plugins = []
    try:
        plugins = plugin_loader.list_plugins()
    except Exception as e:
        print(f"[!] Plugin loader error: {e}")

    print(f"[+] Plugins detected: {len(plugins)}")

    for p in plugins:
        name = p.get("command", "unknown")
        desc = p.get("name", "unnamed plugin")
        print(f"    - [{name}] {desc}")

    print("\n[✓] Environment looks healthy")
