
from detectors import detect_sensitive_data
from risk_engine import calculate_risk

# Sample document with dummy sensitive information
sample_text = """
SENTINEL TEST DOCUMENT

Aadhaar: 2345 6789 0128
PAN: ABCDE1234F
Phone: 9876543210
Email: test@example.com
IFSC: SBIN0001234
UPI: testuser@okaxis
"""
# Step 1: Detect sensitive information
detections = detect_sensitive_data(sample_text)

# Step 2: Calculate privacy risk
risk = calculate_risk(detections)

# Step 3: Display security report
print("\n================================")
print("       SENTINEL SECURITY REPORT")
print("================================")

print("\nTotal sensitive items:", risk["total_findings"])
print("Risk score:", risk["score"], "/ 100")
print("Risk level:", risk["level"])

print("\nDetected categories:")
for category, count in risk["category_counts"].items():
    print(f"- {category}: {count}")

print("\nSecurity recommendation:")
print(risk["message"])

print("\n================================")
