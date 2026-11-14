
# security.py
# SENTINEL Privacy Firewall
# New module - does not modify existing files


def check_document_security(risk, is_redacted=False):
    """
    Evaluates whether a document can be downloaded.

    risk: Output dictionary from calculate_risk()
    is_redacted: Whether the document has been redacted.
    """

    score = risk.get("score", 0)
    level = risk.get("level", "Low")

    # A successfully redacted document can be downloaded.
    if is_redacted:
        return {
            "allowed": True,
            "status": "Protected",
            "message": "Redacted document is permitted for download."
        }

    # Block unredacted documents with high or critical risk.
    if level in ["High", "Critical"]:
        return {
            "allowed": False,
            "status": "Blocked",
            "message": "Download blocked! Sensitive information must be redacted first."
        }

    # Medium-risk documents require user review.
    if level == "Medium":
        return {
            "allowed": True,
            "status": "Warning",
            "message": "Warning: Review sensitive information before sharing."
        }

    # Low-risk documents are allowed.
    return {
        "allowed": True,
        "status": "Safe",
        "message": "No significant privacy risk detected."
    }
