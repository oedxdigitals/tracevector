WEIGHTS = {
    # Email
    "invalid_format": 50,
    "no_mx_record": 40,
    "disposable_email": 35,
    "breach_found": 30,

    # Phone
    "invalid_number": 40,
    "impossible_number": 45,
    "voip_number": 25,

    # IP
    "private_ip": 10,
    "loopback_ip": 15,
    "reserved_ip": 15,
    "bogon_ip": 40,
    "hosting_provider": 20,
    "cloud_provider": 15,
    "tor_exit_node": 60,
    "high_abuse_score": 70,
    "lookup_failed": 20
}


def calculate_risk(scan_result: dict):
    flags = scan_result.get("risk_flags", [])
    score = 0

    for flag in flags:
        score += WEIGHTS.get(flag, 0)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 50:
        level = "HIGH"
    elif score >= 25:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "risk_score": score,
        "risk_level": level
    }
