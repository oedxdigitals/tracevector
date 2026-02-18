#!/usr/bin/env python3

import sys
import json
import traceback

from tvx.banner import show_banner
from tvx.version import VERSION, BUILD
import tvx.plugin_loader as plugin_loader


# -------------------------------------------------
# USAGE
# -------------------------------------------------
def print_usage():
    print(f"""
TRACEVECTOR (tvx) v{VERSION} [{BUILD}]
OSINT CLI Investigator

Usage:
  tvx <type> <target> [options]
  tvx doctor
  tvx --list-plugins
  tvx --version

Types:
  phone     Investigate phone number
  ip        Investigate IP address
  email     Investigate email address

Options:
  --list-plugins          List all loaded plugins
  --json                  Output results as JSON
  --output <file>         Save report (.json or .txt)
  --offline               Disable network-based plugins
  --no-banner             Disable ASCII banner
  --no-plugins <list>     Disable plugins (comma-separated)
  --version               Show version info

Examples:
  tvx phone +14155552671
  tvx ip 8.8.8.8 --offline
  tvx email test@example.com --json
  tvx --list-plugins
  tvx doctor
""")


# -------------------------------------------------
# ARGUMENT PARSER (binary-safe)
# -------------------------------------------------
def parse_args(argv):
    args = {
        "mode": "run",          # run | doctor | list | version
        "type": None,
        "target": None,
        "json": False,
        "offline": False,
        "banner": True,
        "output": None,
        "disabled_plugins": [],
    }

    if "--version" in argv:
        args["mode"] = "version"
        return args

    if "--list-plugins" in argv:
        args["mode"] = "list"
        return args

    if "doctor" in argv:
        args["mode"] = "doctor"
        return args

    if "--json" in argv:
        args["json"] = True
        argv.remove("--json")

    if "--offline" in argv:
        args["offline"] = True
        argv.remove("--offline")

    if "--no-banner" in argv:
        args["banner"] = False
        argv.remove("--no-banner")

    if "--output" in argv:
        idx = argv.index("--output")
        args["output"] = argv[idx + 1]
        del argv[idx:idx + 2]

    if "--no-plugins" in argv:
        idx = argv.index("--no-plugins")
        args["disabled_plugins"] = argv[idx + 1].split(",")
        del argv[idx:idx + 2]

    if len(argv) < 3:
        return None

    args["type"] = argv[1].lower()
    args["target"] = argv[2]

    return args


# -------------------------------------------------
# PLUGIN EXECUTION
# -------------------------------------------------
def run_plugins(target_type, target, offline, disabled):
    results = []
    plugins = plugin_loader.load_plugins(target_type)

    for plugin in plugins:
        name = plugin.__name__.split(".")[-1]

        if name in disabled:
            continue

        if offline and getattr(plugin, "REQUIRES_NETWORK", False):
            continue

        try:
            out = plugin.run(target)
            if out:
                results.append(out)
        except Exception as e:
            results.append({
                "plugin": getattr(plugin, "PLUGIN_NAME", name),
                "error": str(e)
            })

    return results


# -------------------------------------------------
# REPORT EXPORT
# -------------------------------------------------
def export_report(path, report):
    with open(path, "w") as f:
        if path.endswith(".json"):
            json.dump(report, f, indent=2)
        else:
            f.write("TRACEVECTOR REPORT\n")
            f.write(f"Type: {report['type']}\n")
            f.write(f"Target: {report['target']}\n\n")

            for r in report["results"]:
                f.write(f"[{r.get('plugin')}]\n")
                if "error" in r:
                    f.write(f"ERROR: {r['error']}\n\n")
                else:
                    for k, v in r.get("data", {}).items():
                        f.write(f"{k}: {v}\n")
                    f.write("\n")


# -------------------------------------------------
# DOCTOR MODE
# -------------------------------------------------
def run_doctor():
    print("TRACEVECTOR Doctor\n")

    print("[+] Version:", VERSION, BUILD)
    print("[+] Frozen binary:", getattr(sys, "frozen", False))
    print("[+] Python:", sys.executable)

    plugins = plugin_loader.list_all_plugins()
    print(f"[+] Plugins detected: {len(plugins)}")

    for p in plugins:
        print(f"    - [{p['type']}] {p['name']}")

    print("\n[✓] Environment looks healthy")


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    args = parse_args(sys.argv)

    if not args:
        print_usage()
        sys.exit(1)

    # ---- version ----
    if args["mode"] == "version":
        print(f"TRACEVECTOR (tvx) v{VERSION} [{BUILD}]")
        sys.exit(0)

    # ---- list plugins ----
    if args["mode"] == "list":
        plugins = plugin_loader.list_all_plugins()
        print("\nLoaded Plugins:\n")
        for p in plugins:
            print(f"[{p['type']}] {p['name']} ({p['module']})")
        sys.exit(0)

    # ---- doctor ----
    if args["mode"] == "doctor":
        run_doctor()
        sys.exit(0)

    # ---- normal run ----
    if args["banner"]:
        show_banner()

    if args["type"] not in ("phone", "ip", "email"):
        print("[!] Invalid target type\n")
        print_usage()
        sys.exit(1)

    try:
        results = run_plugins(
            args["type"],
            args["target"],
            args["offline"],
            args["disabled_plugins"]
        )

        report = {
            "type": args["type"],
            "target": args["target"],
            "results": results
        }

        if args["output"]:
            export_report(args["output"], report)

        if args["json"]:
            print(json.dumps(report, indent=2))
        else:
            for r in results:
                print("\n" + "=" * 50)
                print(f"[PLUGIN] {r.get('plugin', 'unknown')}")
                print("-" * 50)

                if "error" in r:
                    print("ERROR:", r["error"])
                else:
                    for k, v in r.get("data", {}).items():
                        print(f"{k}: {v}")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
        sys.exit(130)

    except Exception:
        print("[!] Fatal error occurred")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
