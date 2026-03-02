const express = require('express');
const Blockchain = require('./utils/blockchain');
const crypto = require('crypto');

const app = express();
const port = 3000;

app.use(express.json());

// Create blockchain instance
const myBlockchain = new Blockchain();

app.get('/', (req, res) => {
    res.send("TimeLess Vault Blockchain is running 🚀");
});

// Upload document endpoint
app.post('/upload', (req, res) => {

    const documentData = req.body.data;

    if (!documentData) {
        return res.status(400).json({
            error: "Please send document data in JSON body"
        });
    }

    // Generate SHA-256 hash
    const documentHash = crypto.createHash('sha256')
        .update(documentData)
        .digest('hex');

    // Add to blockchain
    myBlockchain.addBlock(documentHash);

    res.json({
        message: "Document added to blockchain successfully",
        hash: documentHash,
        totalBlocks: myBlockchain.chain.length
    });
});

// Verify blockchain integrity
app.get('/verify', (req, res) => {

    const isValid = myBlockchain.isChainValid();

    res.json({
        blockchainValid: isValid
    });
});

app.listen(port, () => {
    console.log(`TimeLess Vault running on port ${port}`);
});