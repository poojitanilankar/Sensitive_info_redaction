
import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  const contractAddress = "0x1c5Cc24c5949a1650efBFF47a42AE00Da8E39fbD";

  const registry = await ethers.getContractAt(
    "DocumentRegistry",
    contractAddress
  );

  const documentId = "SENTINEL-DOC-001";
  const originalHash = "abc123originalhash";
  const redactedHash = "xyz789redactedhash";

  const tx = await registry.registerDocument(
    documentId,
    originalHash,
    redactedHash
  );

  await tx.wait();

  console.log("Document registered successfully!");

  const verified = await registry.verifyDocument(
    documentId,
    redactedHash
  );

  console.log("Integrity verification:", verified);
}

main().catch(console.error);
