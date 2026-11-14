
import json
from pathlib import Path
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

CONTRACT_ADDRESS = Web3.to_checksum_address(
    "0x1c5Cc24c5949a1650efBFF47a42AE00Da8E39fbD"
)

BASE_DIR = Path(__file__).resolve().parent

ABI_PATH = (
    BASE_DIR / "artifacts" / "contracts"
    / "DocumentRegistry.sol" / "DocumentRegistry.json"
)

with open(ABI_PATH, "r", encoding="utf-8") as f:
    abi = json.load(f)["abi"]

contract = w3.eth.contract(
    address=CONTRACT_ADDRESS,
    abi=abi
)

def register_document(document_id, original_hash, redacted_hash):
    account = w3.eth.accounts[0]

    tx = contract.functions.registerDocument(
        document_id, original_hash, redacted_hash
    ).transact({"from": account})

    return w3.eth.wait_for_transaction_receipt(tx)

def verify_document(document_id, supplied_hash):
    return contract.functions.verifyDocument(
        document_id, supplied_hash
    ).call()


def register_integrity_record(record):
    return register_document(
        record["document_id"],
        record["original_hash"],
        record["redacted_hash"]
    )

def register_integrity_record(record, document_id):
    receipt = register_document(
        document_id,
        record["original_hash"],
        record["redacted_hash"]
    )

    return {
        "document_id": document_id,
        "transaction_hash": receipt.transactionHash.hex(),
        "registered": receipt.status == 1
    }

if __name__ == "__main__":
    print("Ganache connected:", w3.is_connected())

    receipt = register_document(
        "SENTINEL-PYTHON-004",
        "sample_original_003",
        "sample_redacted_003"
    )

    print("Transaction successful:", receipt.status == 1)

    print(
        "Integrity verified:",
        verify_document("SENTINEL-PYTHON-004", "sample_redacted_003")    )
