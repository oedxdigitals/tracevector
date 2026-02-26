import requests
import ipaddress

from tvx.result import ScanResult
from tvx.config import get_key


PLUGIN_INFO = {
    "type": "ip",
    "command": "ip",
    "name": "Advanced IP Intelligence"
}


# -----------------------------
# TOR Exit Node Check
# -----------------------------
def is_tor_exit(ip: str) -> bool:
    try:
        response = requests.get(
            "https://check.torproject.org/torbulkexitlist",
            timeout=5
        )
        if response.status_code == 200:
            return ip in response.text.splitlines()
    except Exception:
        pass
    return False


# -----------------------------
# AbuseIPDB Check
# -----------------------------
def check_abuse(ip: str):
    api_key = get_key("abuseipdb_api_key")
    if not api_key:
        return None

    headers = {
        "Key": api_key,
        "Accept": "application/json"
    }

    params = {
        "ipAddress": ip,
        "maxAgeInDays": 90
    }

    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/check",
            headers=headers,
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            return response.json().get("data")
    except Exception:
        pass

    return None


# -----------------------------
# Main Logic
# -----------------------------
def run(target: str):
    metadata = {}
    risk_flags = []
    confidence = 0.9

    # -------------------------
    # Validate IP Address
    # -------------------------
    try:
        ip_obj = ipaddress.ip_address(target)
        metadata["version"] = ip_obj.version

        if ip_obj.is_private:
            metadata["classification"] = "private"
            risk_flags.append("private_ip")
            confidence = 0.6

        elif ip_obj.is_loopback:
            metadata["classification"] = "loopback"
            risk_flags.append("loopback_ip")
            confidence = 0.5

        elif ip_obj.is_reserved:
            metadata["classification"] = "reserved"
            risk_flags.append("reserved_ip")
            confidence = 0.6

        else:
            metadata["classification"] = "public"

    except ValueError:
        return ScanResult(
            target=target,
            type="ip",
            metadata={"error": "Invalid IP format"},
            risk_flags=["invalid_format"],
            confidence=0.3
        ).to_dict()

    # -------------------------
    # Stop if not public
    # -------------------------
    if metadata["classification"] != "public":
        return ScanResult(
            target=target,
            type="ip",
            metadata=metadata,
            risk_flags=risk_flags,
            confidence=round(confidence, 2)
        ).to_dict()

    # -------------------------
    # Public IP Intelligence
    # -------------------------
    api_key = get_key("ipinfo_api_key")
    url = f"https://ipinfo.io/{target}/json"

    if api_key:
        url += f"?token={api_key}"

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        metadata["ip"] = data.get("ip")
        metadata["city"] = data.get("city")
        metadata["region"] = data.get("region")
        metadata["country"] = data.get("country")

        # ASN + ISP Parsing
        org = data.get("org")
        metadata["org"] = org

        if org:
            parts = org.split(" ", 1)
            metadata["asn"] = parts[0]
            metadata["isp"] = parts[1] if len(parts) > 1 else None

            # Cloud provider detection
            if metadata["isp"] and any(
                keyword in metadata["isp"].lower()
                for keyword in [
                    "amazon",
                    "google",
                    "microsoft",
                    "digitalocean",
                    "oracle",
                    "hosting"
                ]
            ):
                risk_flags.append("cloud_provider")

        # TOR Detection
        if is_tor_exit(target):
            metadata["tor_exit_node"] = True
            risk_flags.append("tor_exit_node")
        else:
            metadata["tor_exit_node"] = False

        # AbuseIPDB Check
        abuse_data = check_abuse(target)
        metadata["abuseipdb"] = abuse_data

        if abuse_data:
            score = abuse_data.get("abuseConfidenceScore", 0)
            metadata["abuse_score"] = score

            if score > 50:
                risk_flags.append("high_abuse_score")

        # If no risk flags added for public IP
        if not risk_flags:
            risk_flags.append("clean")

    except Exception:
        metadata["error"] = "IP lookup failed"
        risk_flags.append("lookup_failed")
        confidence = 0.6

    return ScanResult(
        target=target,
        type="ip",
        metadata=metadata,
        risk_flags=risk_flags,
        confidence=round(confidence, 2)
    ).to_dict()
