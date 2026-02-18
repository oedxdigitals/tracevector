import sys
import os
import tvx.plugin_loader as loader

def run_doctor():
    print("[*] TRACEVECTOR Doctor\n")

    print("[+] Python executable:", sys.executable)
    print("[+] Frozen binary:", getattr(sys, 'frozen', False))

    plugins = loader.list_all_plugins()
    print(f"[+] Plugins detected: {len(plugins)}")

    for p in plugins:
        print(f"    - [{p['type']}] {p['name']}")

    print("\n[✓] Environment looks healthy")
