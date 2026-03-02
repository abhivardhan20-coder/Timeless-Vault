async function main() {
  const VaultRegistry = await ethers.getContractFactory("VaultRegistry");
  const vault = await VaultRegistry.deploy();
  await vault.waitForDeployment();
  console.log("Contract deployed to:", await vault.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});