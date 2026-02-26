import argparse
import json
import sys
from datetime import datetime

from tvx.plugin_loader import load_plugins
from tvx.scoring import calculate_risk
from tvx.reporting import generate_html
from tvx.config import set_key
from tvx.storage.manager import get_storage


# =====================================
# Banner
# =====================================
def print_banner():
    print(r"""
████████╗██████╗  █████╗  ██████╗███████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██╔════╝
   ██║   ██████╔╝███████║██║     █████╗
   ██║   ██╔══██╗██╔══██║██║     ██╔══╝
   ██║   ██║  ██║██║  ██║╚██████╗███████╗
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚══════╝

        TRACEVECTOR FRAUD INTELLIGENCE
""")


# =====================================
# Main
# =====================================
def main():
    parser = argparse.ArgumentParser(
        prog="tvx",
        description="TraceVector Fraud Intelligence Toolkit"
    )

    parser.add_argument("command", help="Core command or plugin")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--report", help="Generate HTML report")

    parsed = parser.parse_args()

    print_banner()

    command = parsed.command
    arguments = parsed.args

    # =========================
    # CORE: CONFIG
    # =========================
    if command == "config":
        if not arguments or "=" not in arguments[0]:
            print("Usage: tvx config key=value")
            sys.exit(1)

        key, value = arguments[0].split("=", 1)
        set_key(key.strip(), value.strip())
        print(f"[✓] Config saved: {key}")
        sys.exit(0)

    # =========================
    # CORE: CASE
    # =========================
    if command == "case":
        if not arguments:
            print("Usage: tvx case <create|add|show>")
            sys.exit(1)

        action = arguments[0]
        storage = get_storage()

        # CREATE
        if action == "create":
            if len(arguments) < 2:
                print("Usage: tvx case create CASE_ID")
                sys.exit(1)

            case_id = arguments[1]
            storage.create_case(case_id)
            print(f"[✓] Case created: {case_id}")
            sys.exit(0)

        # ADD
        if action == "add":
            if len(arguments) < 4:
                print("Usage: tvx case add CASE_ID plugin target")
                sys.exit(1)

            case_id = arguments[1]
            plugin_name = arguments[2]
            target = arguments[3]

            plugins = load_plugins()

            if plugin_name not in plugins:
                print("[!] Unknown plugin")
                sys.exit(1)

            plugin = plugins[plugin_name]
            result = plugin.run(target)
            risk = calculate_risk(result)

            storage.add_evidence(case_id, plugin_name, target, result, risk)

            print(f"[✓] Evidence added to case {case_id}")
            print(f"Risk Level: {risk['level']} (Score: {risk['score']})")
            sys.exit(0)

        # SHOW
        if action == "show":
            if len(arguments) < 2:
                print("Usage: tvx case show CASE_ID")
                sys.exit(1)

            case_id = arguments[1]
            case_data = storage.get_case(case_id)

            if not case_data["case"]:
                print("[!] Case not found.")
                sys.exit(1)

            print(json.dumps(case_data, indent=2))
            sys.exit(0)

        print("Unknown case action.")
        sys.exit(1)

    # =========================
    # PLUGIN EXECUTION
    # =========================
    plugins = load_plugins()

    if command not in plugins:
        print(f"[!] Unknown command: {command}")
        print("Available plugins:", ", ".join(plugins.keys()))
        sys.exit(1)

    if not arguments:
        print("[!] Target required.")
        sys.exit(1)

    target = arguments[0]
    plugin = plugins[command]

    try:
        result = plugin.run(target)
    except Exception as e:
        print(f"[!] Plugin execution failed: {e}")
        sys.exit(1)

    risk = calculate_risk(result)

    output = {
        "scan": result,
        "risk": risk
    }

    if parsed.json:
        print(json.dumps(output, indent=2))
    else:
        print("\n=== Scan Result ===")
        print(json.dumps(result, indent=2))
        print("\n=== Risk Assessment ===")
        print(json.dumps(risk, indent=2))

    if parsed.report:
        file_path = generate_html(output, risk, parsed.report)
        print(f"\n[✓] HTML report generated: {file_path}")
