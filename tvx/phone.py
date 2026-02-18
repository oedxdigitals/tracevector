try:
    import phonenumbers
    from phonenumbers import geocoder, carrier
except ImportError:
    print("[!] Missing dependency: phonenumbers")
    print("Run: pip install phonenumbers")
    exit(1)

def investigate_phone(number):
    try:
        parsed = phonenumbers.parse(number)
        print("[+] Valid Number:", phonenumbers.is_valid_number(parsed))
        print("[+] Country:", geocoder.description_for_number(parsed, "en"))
        print("[+] Carrier:", carrier.name_for_number(parsed, "en"))
    except Exception as e:
        print("[!] Error:", e)
