import re

def investigate_email(email):
    print("[+] Email:", email)
    domain = email.split("@")[-1]

    print("[+] Domain:", domain)
    print("[+] Disposable:", "yes" if "mail" in domain else "unknown")
