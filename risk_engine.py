
# risk_engine.py
# Additional module for SENTINEL
# Does not modify the existing detectors.py

RISK_WEIGHTS = {
    "Aadhaar": 20,
    "PAN": 18,
    "Card": 25,
    "Bank Account": 22,
    "UPI": 15,
    "IFSC": 10,
    "Phone": 8,
    "Email": 8
}


def calculate_risk(detections):
    """
    Calculates document-level privacy exposure risk.

    Input:
        detections: Output from detect_sensitive_data()

    Output:
        Dictionary containing score, level, counts and findings.
    """

    if not detections:
        return {
            "score": 0,
            "level": "Low",
            "total_findings": 0,
            "category_counts": {},
            "message": "No sensitive information detected."
        }

    total_risk = 0
    category_counts = {}

    for item in detections:
        category = item.get("type", "Unknown")
        confidence = item.get("confidence", 0.5)

        weight = RISK_WEIGHTS.get(category, 5)

        category_counts[category] = (
            category_counts.get(category, 0) + 1
        )

        total_risk += weight * confidence

    # Normalize the score so repeated findings
    # increase risk without exceeding 100.
    score = min(round(total_risk / 2), 100)

    if score >= 70:
        level = "Critical"
        message = "High privacy exposure. Immediate redaction recommended."

    elif score >= 40:
        level = "High"
        message = "Significant sensitive information detected."

    elif score >= 15:
        level = "Medium"
        message = "Some sensitive information is exposed."

    else:
        level = "Low"
        message = "Limited sensitive information detected."

    return {
        "score": score,
        "level": level,
        "total_findings": len(detections),
        "category_counts": category_counts,
        "message": message
    }
