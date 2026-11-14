
from security import check_document_security

# Test 1: High-risk document
high_risk = {
    "score": 85,
    "level": "Critical"
}

# Test 2: Medium-risk document
medium_risk = {
    "score": 37,
    "level": "Medium"
}

# Test 3: Low-risk document
low_risk = {
    "score": 5,
    "level": "Low"
}

print("\n===== SENTINEL PRIVACY FIREWALL =====")

for name, risk in [
    ("High-risk document", high_risk),
    ("Medium-risk document", medium_risk),
    ("Low-risk document", low_risk)
]:

    result = check_document_security(risk)

    print(f"\n{name}")
    print("Status:", result["status"])
    print("Download allowed:", result["allowed"])
    print("Message:", result["message"])

# Test 4: Redacted document
redacted_result = check_document_security(
    high_risk,
    is_redacted=True
)

print("\nRedacted document")
print("Status:", redacted_result["status"])
print("Download allowed:", redacted_result["allowed"])
print("Message:", redacted_result["message"])
