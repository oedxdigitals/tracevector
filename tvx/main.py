import argparse
import sys
import json

from tvx.plugin_loader import load_plugins
from tvx.scoring import calculate_risk
from tvx.doctor import run_doctor
from tvx.config import set_key
from tvx import __version__


BANNER = r"""
████████╗██████╗  █████╗  ██████╗███████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
   ██║   ██████╔╝███████║██║     █████╗
   ██║   ██╔══██╗██╔══██║██║     ██╔══╝
   ██║   ██║  ██║██║  ██║╚██████╗███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝

        TRACEVECTOR OSINT CLI
     Digital Footprint Investigator
"""


# ---------------------------
# Utility Functions
# ---------------------------

def print_banner():
    print(BANNER)


def print_version():
    print(f"TRACEVECTOR (tvx) v{__version__}")


def print_plugins(plugins):
    print("\nLoaded Plugins:\n")
    for plugin in plugins:
        info = getattr(plugin, "PLUGIN_INFO", {})
        cmd = info.get("command", "unknown")
        name = info.get("name", "Unnamed Plugin")
        print(f"[{cmd}] {name}")
    print()


def print_nested(data, indent=0):
    for key, value in data.items():
        if isinstance(value, dict):
            print(" " * indent + f"{key}:")
            print_nested(value, indent + 4)
        else:
            print(" " * indent + f"{key}: {value}")


def format_pretty(result: dict, risk: dict):
    print("\n=== Scan Result ===")
    print_nested(result)

    print("\n=== Risk Assessment ===")
    print_nested(risk)
    print()


# ---------------------------
# Main Entry
# ---------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="tvx",
        description="TraceVector OSINT CLI"
    )

    parser.add_argument(
        "command",
        nargs="?",
        help="Command (doctor, config, or plugin type)"
    )

    parser.add_argument(
        "target",
        nargs="?",
        help="Target value or config KEY=VALUE"
    )

    parser.add_argument(
        "--list-plugins",
        action="store_true",
        help="List all loaded plugins"
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version information"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output result as JSON"
    )

    args = parser.parse_args()

    plugins = load_plugins()

    # ---------------------------
    # Version
    # ---------------------------
    if args.version:
        print_version()
        return 0

    # ---------------------------
    # Doctor
    # ---------------------------
    if args.command == "doctor":
        run_doctor()
        return 0

    # ---------------------------
    # Config Command
    # ---------------------------
    if args.command == "config":
        if not args.target:
            print("Usage: tvx config KEY=VALUE")
            return 1

        if "=" not in args.target:
            print("Format must be KEY=VALUE")
            return 1

        key, value = args.target.split("=", 1)
        set_key(key.strip(), value.strip())
        print(f"[✓] Config updated: {key}")
        return 0

    # ---------------------------
    # List Plugins
    # ---------------------------
    if args.list_plugins:
        print_version()
        print_plugins(plugins)
        return 0

    # ---------------------------
    # No Command Provided
    # ---------------------------
    if not args.command:
        print_banner()
        parser.print_help()
        return 0

    # ---------------------------
    # Plugin Execution
    # ---------------------------
    selected_plugin = None
    for plugin in plugins:
        info = getattr(plugin, "PLUGIN_INFO", {})
        if info.get("command") == args.command:
            selected_plugin = plugin
            break

    if not selected_plugin:
        print_banner()
        print(f"\n[!] No plugin found for command: {args.command}\n")
        return 1

    if not args.target:
        print(f"[!] Target required for command: {args.command}")
        return 1

    try:
        print_banner()

        result = selected_plugin.run(args.target)
        risk = calculate_risk(result)

        if args.json:
            output = {
                "scan": result,
                "risk": risk
            }
            print(json.dumps(output, indent=4))
        else:
            format_pretty(result, risk)

        return 0

    except Exception as e:
        print(f"\n[!] Error during execution: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
