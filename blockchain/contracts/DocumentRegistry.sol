
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract DocumentRegistry {

    struct DocumentRecord {
        string originalHash;
        string redactedHash;
        uint256 timestamp;
        address registeredBy;
    }

    mapping(string => DocumentRecord) private records;

    event DocumentRegistered(
        string indexed documentId,
        string originalHash,
        string redactedHash,
        uint256 timestamp,
        address registeredBy
    );

    function registerDocument(
        string memory documentId,
        string memory originalHash,
        string memory redactedHash
    ) public {
        require(bytes(documentId).length > 0, "Document ID required");
        require(bytes(originalHash).length > 0, "Original hash required");
        require(bytes(redactedHash).length > 0, "Redacted hash required");
        require(
            bytes(records[documentId].originalHash).length == 0,
            "Document already registered"
        );

        records[documentId] = DocumentRecord({
            originalHash: originalHash,
            redactedHash: redactedHash,
            timestamp: block.timestamp,
            registeredBy: msg.sender
        });

        emit DocumentRegistered(
            documentId,
            originalHash,
            redactedHash,
            block.timestamp,
            msg.sender
        );
    }

    function verifyDocument(
        string memory documentId,
        string memory suppliedHash
    ) public view returns (bool) {
        DocumentRecord memory record = records[documentId];

        return
            bytes(record.redactedHash).length > 0 &&
            keccak256(bytes(record.redactedHash)) ==
            keccak256(bytes(suppliedHash));
    }

    function getDocument(
        string memory documentId
    ) public view returns (DocumentRecord memory) {
        require(
            bytes(records[documentId].originalHash).length > 0,
            "Document not found"
        );

        return records[documentId];
    }
}
