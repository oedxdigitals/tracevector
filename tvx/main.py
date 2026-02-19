#!/usr/bin/env python3

import sys
import argparse
import platform

from tvx import __version__
from tvx.banner import show_banner
from tvx.doctor import run_doctor
from tvx.plugin_loader import (
    list_plugins,
    get_plugins_by_type,
)


def print_version():
    print(f"TRACEVECTOR (tvx) v{__version__}")


def print_plugins():
    plugins = list_plugins()

    if not plugins:
        print("No plugins loaded.")
        return

    print("\nLoaded Plugins:\n")
    for p in plugins:
        info = p.PLUGIN_INFO
        print(
            f"[{info.get('type')}] "
            f"{info.get('name')} "
            f"({p.__name__})"
        )


def build_parser():
    parser = argparse.ArgumentParser(
        prog="tvx",
        description="TRACEVECTOR OSINT CLI Investigator",
        add_help=True,
    )

    parser.add_argument(
        "command",
        nargs="?",
        help="Investigation type (phone, email, ip, etc)",
    )

    parser.add_argument(
        "target",
        nargs="?",
        help="Target to investigate",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    parser.add_argument(
        "--offline",
        action="store_true",
        help="Disable network-based plugins",
    )

    parser.add_argument(
        "--no-banner",
        action="store_true",
        help="Disable ASCII banner",
    )

    parser.add_argument(
        "--list-plugins",
        action="store_true",
        help="List all loaded plugins",
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version info",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Version
    if args.version:
        print_version()
        return 0

    # List plugins
    if args.list_plugins:
        print_version()
        print_plugins()
        return 0

    # Doctor command
    if args.command == "doctor":
        run_doctor()
        return 0

    # No command provided
    if not args.command:
        parser.print_help()
        return 1

    # Banner
    if not args.no_banner:
        show_banner()

    # Load plugins for command
    plugins = get_plugins_by_type(args.command)

    if not plugins:
        print(f"[!] No plugin found for command: {args.command}")
        return 1

    if not args.target:
        print("[!] No target provided")
        return 1

    # Execute plugins
    for plugin in plugins:
        try:
            plugin.run(
                target=args.target,
                options={
                    "json": args.json,
                    "offline": args.offline,
                },
            )
        except Exception as e:
            print(f"[!] Plugin error ({plugin.__name__}): {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
