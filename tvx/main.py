#!/usr/bin/env python3
"""
TRACEVECTOR OSINT CLI – Main Entry Point
"""

import sys
import argparse
from importlib import metadata

from tvx import plugin_loader
from tvx.doctor import run_doctor

APP_NAME = "TRACEVECTOR"
CLI_NAME = "tvx"
STABILITY = "stable"


def get_version() -> str:
    try:
        return metadata.version("tracevector")
    except metadata.PackageNotFoundError:
        return "0.0.0"


def print_banner():
    banner = r"""
████████╗██████╗  █████╗  ██████╗███████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
   ██║   ██████╔╝███████║██║     █████╗
   ██║   ██╔══██╗██╔══██║██║     ██╔══╝
   ██║   ██║  ██║██║  ██║╚██████╗███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝

        TRACEVECTOR OSINT CLI
     Digital Footprint Investigator
"""
    print(banner)


def print_version():
    print(f"{APP_NAME} ({CLI_NAME}) v{get_version()} [{STABILITY}]")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog=CLI_NAME,
        description="TRACEVECTOR OSINT Command Line Interface",
        add_help=True,
    )

    parser.add_argument(
        "--version",
        action="store_true",
        help="Show TRACEVECTOR version and exit",
    )

    subparsers = parser.add_subparsers(dest="command")

    # Doctor
    subparsers.add_parser(
        "doctor",
        help="Run TRACEVECTOR environment diagnostics",
    )

    # Plugin passthrough (dynamic)
    subparsers.add_parser(
        "phone",
        help="Investigate phone numbers (plugin-based)",
    )

    return parser


def main():
    parser = build_parser()
    args, unknown_args = parser.parse_known_args()

    # --version
    if args.version:
        print_version()
        return 0

    # doctor
    if args.command == "doctor":
        run_doctor()
        return 0

    # No command → show help
    if not args.command:
        print_banner()
        parser.print_help()
        return 1

    # Plugin execution
    plugins = plugin_loader.load_plugins(args.command)

    if not plugins:
        print(f"[!] No plugin found for command: {args.command}")
        return 1

    plugin = plugins[0]

    print_banner()
    try:
        plugin.run(unknown_args)
    except Exception as e:
        print(f"[!] Plugin execution failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
