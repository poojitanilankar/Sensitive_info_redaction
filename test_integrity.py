
from integrity import (
    calculate_file_hash,
    create_integrity_record,
    verify_document
)

# Dummy document contents for testing
original_document = b"""
SENTINEL TEST DOCUMENT
Name: Test User
PAN: ABCDE1234F
"""

# Simulated redacted document
redacted_document = b"""
SENTINEL TEST DOCUMENT
Name: [REDACTED]
PAN: [REDACTED]
"""

print("\n====================================")
print(" SENTINEL DOCUMENT INTEGRITY REPORT")
print("====================================")

# Step 1: Create integrity record
record = create_integrity_record(
    original_document,
    redacted_document
)

print("\nOriginal SHA-256:")
print(record["original_hash"])

print("\nRedacted SHA-256:")
print(record["redacted_hash"])

print("\nTimestamp:", record["timestamp"])
print("Action:", record["action"])

# Step 2: Verify the unchanged redacted document
print("\n--- TEST 1: Original redacted file ---")

result = verify_document(
    redacted_document,
    record["redacted_hash"]
)

print("Integrity verified:", result["verified"])

# Step 3: Simulate someone modifying the document
tampered_document = b"""
SENTINEL TEST DOCUMENT
Name: Attacker Changed This
PAN: ABCDE1234F
"""

print("\n--- TEST 2: Modified document ---")

tampered_result = verify_document(
    tampered_document,
    record["redacted_hash"]
)

print("Integrity verified:", tampered_result["verified"])

if not tampered_result["verified"]:
    print("WARNING: Document modification detected!")

print("\n====================================")

