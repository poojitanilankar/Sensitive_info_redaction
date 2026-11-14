
import re


PATTERNS = {
    "Aadhaar": r"(?<!\d)(?:\d{4}[\s-]?\d{4}[\s-]?\d{4})(?!\d)",

    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

    "Phone": r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{9}(?!\d)",

    "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    "Card": r"(?<!\d)(?:\d[ -]?){13,19}(?!\d)",

    "IFSC": r"\b[A-Z]{4}0[A-Z0-9]{6}\b",

    "UPI": r"\b[A-Za-z0-9._-]{2,}@[A-Za-z]{2,}\b",

    "Bank Account": r"\b\d{9,18}\b"
}


def luhn_check(number):
    digits = [int(c) for c in number if c.isdigit()]

    if not 13 <= len(digits) <= 19:
        return False

    total = 0

    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 1:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit

    return total % 10 == 0


def detect_sensitive_data(text):
    """
    Returns a list of detections.

    Each detection contains:
    type, value, start, end, confidence
    """

    results = []

    for category, pattern in PATTERNS.items():

        for match in re.finditer(pattern, text):

            value = match.group()

            # Avoid classifying the same card as an account number.
            if category == "Bank Account" and (
                " " in value or "-" in value
            ):
                continue

            confidence = 0.95

            if category == "Card":
                if not luhn_check(value):
                    continue

            if category == "Aadhaar":
                digits = re.sub(r"\D", "", value)
                if len(digits) != 12 or digits[0] in "01":
                    continue
                confidence = 0.90

            if category == "Phone":
                confidence = 0.90

            if category == "Bank Account":
                confidence = 0.65

            results.append({
                "type": category,
                "value": value,
                "start": match.start(),
                "end": match.end(),
                "confidence": confidence
            })

    # Remove duplicate or overlapping detections.
    results.sort(key=lambda x: (x["start"], -(x["end"] - x["start"])))

    filtered = []

    for item in results:
        if not any(
            item["start"] < old["end"]
            and item["end"] > old["start"]
            for old in filtered
        ):
            filtered.append(item)

    return filtered
