const crypto = require('crypto');

class Block {
    constructor(index, timestamp, documentHash, previousHash = '') {
        this.index = index;
        this.timestamp = timestamp;
        this.documentHash = documentHash;
        this.previousHash = previousHash;
        this.hash = this.calculateHash();
    }

    calculateHash() {
        return crypto.createHash('sha256')
            .update(
                this.index +
                this.timestamp +
                this.documentHash +
                this.previousHash
            )
            .digest('hex');
    }
}

class Blockchain {
    constructor() {
        this.chain = [this.createGenesisBlock()];
    }

    createGenesisBlock() {
        return new Block(0, new Date().toISOString(), "Genesis Block", "0");
    }

    getLatestBlock() {
        return this.chain[this.chain.length - 1];
    }

    addBlock(documentHash) {
        const newBlock = new Block(
            this.chain.length,
            new Date().toISOString(),
            documentHash,
            this.getLatestBlock().hash
        );

        this.chain.push(newBlock);
    }

    isChainValid() {
        for (let i = 1; i < this.chain.length; i++) {

            const currentBlock = this.chain[i];
            const previousBlock = this.chain[i - 1];

            if (currentBlock.hash !== currentBlock.calculateHash()) {
                return false;
            }

            if (currentBlock.previousHash !== previousBlock.hash) {
                return false;
            }
        }

        return true;
    }
}

module.exports = Blockchain;