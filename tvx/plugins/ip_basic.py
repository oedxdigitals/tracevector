import ipaddress

COMMAND = "ip"

class Plugin:
    name = "Basic IP Metadata"

    def run(self, args):
        target = args[0] if args else None

        print("[PLUGIN] Basic IP Metadata")
        print(f"input: {target}")

        try:
            ip = ipaddress.ip_address(target)
            print(f"version: IPv{ip.version}")
            print("is_private:", ip.is_private)
            print("status: plugin_loaded_successfully")
        except ValueError:
            print("error: invalid IP address")
