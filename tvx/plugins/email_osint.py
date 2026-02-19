import dns.resolver
import re
import hashlib

COMMAND = "email"

class Plugin:
    name = "Email OSINT Analysis"

    def run(self, args):
        email = args[0]
        domain = email.split("@")[-1]

        result = {
            "target": email,
            "metadata": {},
            "risk": {"score": 0, "level": "low"},
            "sources": [],
            "notes": []
        }

        # Basic validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            result["notes"].append("Invalid email format")
            result["risk"]["score"] += 50
            return result

        # MX Records
        try:
            mx = dns.resolver.resolve(domain, "MX")
            result["metadata"]["mx_records"] = [r.exchange.to_text() for r in mx]
        except Exception:
            result["metadata"]["mx_records"] = []
            result["risk"]["score"] += 30
            result["notes"].append("No MX records")

        # Provider detection
        if "google.com" in str(result["metadata"].get("mx_records", "")):
            result["metadata"]["provider"] = "Google"
        else:
            result["metadata"]["provider"] = "Unknown"

        # Disposable check (basic)
        disposable_domains = {"mailinator.com", "tempmail.com"}
        if domain in disposable_domains:
            result["risk"]["score"] += 40
            result["notes"].append("Disposable email domain")

        # Risk level
        result["risk"]["level"] = score_level(result["risk"]["score"])
        result["sources"].append("DNS")

        return result


def score_level(score):
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"
