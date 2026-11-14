
# integrity.py
# SENTINEL Document Integrity Verification

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone


def calculate_file_hash(file_bytes):
    """Generate SHA-256 fingerprint of a document."""

    return hashlib.sha256(file_bytes).hexdigest()


def create_integrity_record(original_bytes, redacted_bytes):
    """Create an integrity record for document redaction."""

    record = {
        "original_hash": calculate_file_hash(original_bytes),
        "redacted_hash": calculate_file_hash(redacted_bytes),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": "DOCUMENT_REDACTED"
    }

    return record


def verify_document(file_bytes, expected_hash):
    """Check whether a document has been modified."""

    actual_hash = calculate_file_hash(file_bytes)

    return {
        "verified": actual_hash == expected_hash,
        "actual_hash": actual_hash,
        "expected_hash": expected_hash
    }
