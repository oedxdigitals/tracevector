import re
import dns.resolver
import requests

from tvx.result import ScanResult
from tvx.config import get_key


PLUGIN_INFO = {
    "type": "email",
    "command": "email",
    "name": "Advanced Email Intelligence"
}


# ---------------------------
# Utilities
# ---------------------------

EMAIL_REGEX = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

DISPOSABLE_DOMAINS = {
    "mailinator.com",
    "10minutemail.com",
    "guerrillamail.com",
    "tempmail.com",
    "yopmail.com"
}


def is_valid_format(email: str) -> bool:
    return re.match(EMAIL_REGEX, email) is not None


def get_mx_records(domain: str):
    try:
        answers = dns.resolver.resolve(domain, "MX")
        return sorted([str(r.exchange).rstrip('.') for r in answers])
    except Exception:
        return []


def check_breaches(email: str):
    api_key = get_key("hibp_api_key")
    if not api_key:
        return []

    headers = {
        "hibp-api-key": api_key,
        "user-agent": "tracevector"
    }

    try:
        response = requests.get(
            f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}",
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            return [b["Name"] for b in response.json()]
        elif response.status_code == 404:
            return []
        else:
            return []

    except Exception:
        return []


# ---------------------------
# Main Plugin Logic
# ---------------------------

def run(target: str):
    metadata = {}
    risk_flags = []
    confidence = 0.9

    # Validate format
    if not is_valid_format(target):
        return ScanResult(
            target=target,
            type="email",
            metadata={"error": "Invalid email format"},
            risk_flags=["invalid_format"],
            confidence=0.4
        ).to_dict()

    local_part, domain = target.split("@", 1)

    metadata["local_part"] = local_part
    metadata["domain"] = domain

    # MX Lookup
    mx_records = get_mx_records(domain)
    metadata["mx_records"] = mx_records

    if mx_records:
        risk_flags.append("mx_present")
    else:
        risk_flags.append("no_mx_record")

    # Disposable check
    if domain.lower() in DISPOSABLE_DOMAINS:
        risk_flags.append("disposable_email")

    # Breach check (optional API key)
    breaches = check_breaches(target)
    metadata["breaches"] = breaches
    metadata["breach_count"] = len(breaches)

    if breaches:
        risk_flags.append("breach_found")

    # Clean logic
    if mx_records and not breaches and domain.lower() not in DISPOSABLE_DOMAINS:
        risk_flags.append("clean")

    # Confidence tuning
    if not mx_records:
        confidence -= 0.2
    if breaches:
        confidence += 0.05

    return ScanResult(
        target=target,
        type="email",
        metadata=metadata,
        risk_flags=risk_flags,
        confidence=round(confidence, 2)
    ).to_dict()
