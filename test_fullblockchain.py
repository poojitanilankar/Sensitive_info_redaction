
from integrity import create_integrity_record
from blockchain.blockchain_client import register_integrity_record, verify_document

original = b"My original SENTINEL document"
redacted = b"My redacted SENTINEL document"

record = create_integrity_record(original, redacted)

result = register_integrity_record(
    record,
    "SENTINEL-REAL-001"
)

print("Blockchain registration:", result)

verified = verify_document(
    "SENTINEL-REAL-001",
    record["redacted_hash"]
)

print("SHA-256 blockchain verification:", verified)
