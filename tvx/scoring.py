def calculate_risk(result: dict) -> dict:
    """
    Simple fraud risk scoring engine.
    """

    score = 0
    flags = []

    # Example signals
    if result.get("disposable_email"):
        score += 40
        flags.append("Disposable email provider")

    if result.get("tor_exit"):
        score += 50
        flags.append("Tor exit node detected")

    if result.get("vpn"):
        score += 30
        flags.append("VPN usage suspected")

    if result.get("blacklisted"):
        score += 60
        flags.append("Found in blacklist")

    # Risk level
    if score >= 80:
        level = "HIGH"
    elif score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level,
        "flags": flags
    }
