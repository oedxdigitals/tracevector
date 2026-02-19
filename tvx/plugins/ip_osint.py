import ipaddress
from ipwhois import IPWhois

COMMAND = "ip"

class Plugin:
    name = "IP OSINT Analysis"

    def run(self, args):
        ip = args[0]

        result = {
            "target": ip,
            "metadata": {},
            "risk": {"score": 0, "level": "low"},
            "sources": [],
            "notes": []
        }

        try:
            ip_obj = ipaddress.ip_address(ip)
        except ValueError:
            result["notes"].append("Invalid IP address")
            result["risk"]["score"] = 100
            result["risk"]["level"] = "high"
            return result

        # Private IP check
        if ip_obj.is_private:
            result["notes"].append("Private IP address")
            result["risk"]["score"] += 10

        # WHOIS
        try:
            whois = IPWhois(ip).lookup_rdap()
            result["metadata"]["asn"] = whois.get("asn")
            result["metadata"]["org"] = whois.get("network", {}).get("name")
        except Exception:
            result["notes"].append("WHOIS lookup failed")
            result["risk"]["score"] += 20

        # Datacenter heuristic
        org = str(result["metadata"].get("org", "")).lower()
        if any(k in org for k in ["google", "amazon", "cloud", "hosting"]):
            result["notes"].append("Datacenter / hosting IP")
            result["risk"]["score"] += 20

        result["risk"]["level"] = score_level(result["risk"]["score"])
        result["sources"].append("RDAP")

        return result


def score_level(score):
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
