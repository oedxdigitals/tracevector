COMMAND = "phone"
NAME = "Basic Phone Metadata"

def run(args):
    phone = args[0] if args else "N/A"

    print("=" * 50)
    print("[PLUGIN] Basic Phone Metadata")
    print("-" * 50)
    print(f"input: {phone}")
    print("country: Unknown")
    print("carrier: Unknown")
    print("risk_score: 20/100")
