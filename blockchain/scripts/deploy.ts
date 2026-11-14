
import { network } from "hardhat";

async function main() {
  const { ethers } = await network.connect();

  console.log("Deploying DocumentRegistry to Ganache...");

  const Registry = await ethers.getContractFactory("DocumentRegistry");
  const registry = await Registry.deploy();

  await registry.waitForDeployment();

  console.log("DocumentRegistry deployed successfully!");
  console.log("Contract address:", await registry.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
