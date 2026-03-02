// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract VaultRegistry {

    mapping(bytes32 => bool) public documentHashes;

    event HashStored(bytes32 hash);

    function storeHash(bytes32 _hash) public {
        require(!documentHashes[_hash], "Hash already exists");
        documentHashes[_hash] = true;
        emit HashStored(_hash);
    }

    function verifyHash(bytes32 _hash) public view returns (bool) {
        return documentHashes[_hash];
    }
}