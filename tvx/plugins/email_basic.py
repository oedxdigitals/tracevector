COMMAND = "email"

class Plugin:
    name = "Basic Email Metadata"

    def run(self, args):
        target = args[0] if args else None

        print("[PLUGIN] Basic Email Metadata")
        print(f"input: {target}")

        if not target or "@" not in target:
            print("error: invalid email")
            return

        domain = target.split("@")[-1]
        print(f"domain: {domain}")
        print("status: plugin_loaded_successfully")
