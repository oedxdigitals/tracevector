import phonenumbers
from phonenumbers import carrier, geocoder, number_type

from tvx.result import ScanResult


PLUGIN_INFO = {
    "type": "phone",
    "command": "phone",
    "name": "Advanced Phone Metadata"
}


def run(target: str):
    metadata = {}
    risk_flags = []
    confidence = 0.9

    try:
        parsed = phonenumbers.parse(target, None)

        # Basic validation
        metadata["international_format"] = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL
        )
        metadata["country_code"] = parsed.country_code
        metadata["national_number"] = parsed.national_number

        metadata["possible"] = phonenumbers.is_possible_number(parsed)
        metadata["valid"] = phonenumbers.is_valid_number(parsed)

        metadata["region"] = geocoder.description_for_number(parsed, "en")
        metadata["carrier"] = carrier.name_for_number(parsed, "en")

        num_type = number_type(parsed)
        metadata["number_type"] = str(num_type)

        # Risk logic
        if not metadata["possible"]:
            risk_flags.append("impossible_number")
        elif not metadata["valid"]:
            risk_flags.append("invalid_number")
        else:
            risk_flags.append("valid_number")

        if not metadata["carrier"]:
            risk_flags.append("unknown_carrier")

        if num_type == phonenumbers.PhoneNumberType.VOIP:
            risk_flags.append("voip_number")

        if metadata["valid"] and metadata["carrier"]:
            risk_flags.append("clean")

    except Exception:
        metadata["error"] = "Invalid phone number format"
        risk_flags.append("invalid_format")
        confidence = 0.5

    result = ScanResult(
        target=target,
        type="phone",
        metadata=metadata,
        risk_flags=risk_flags,
        confidence=confidence
    )

    return result.to_dict()
