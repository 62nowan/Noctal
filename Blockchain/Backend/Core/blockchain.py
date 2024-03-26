import sys 
sys.path.append('/Users/______/Documents/Noctal') # Your repository

from Blockchain.Backend.Core.block import Block
from Blockchain.Backend.Core.blockheader import BlockHeader
from Blockchain.Backend.util.util import hash256
from Blockchain.Backend.Core.database.database import BlockchainDB
from Blockchain.Backend.Core.tx import CoinbaseTx
import time



GENESIS_HASH = '0' * 64
VERSION = 1 

class Blockchain:
    def __init__(self):
        pass

    def write_on_disk(self,block):
        blockchainDB = BlockchainDB()
        blockchainDB.write(block)
    
    def fetch_last_block(self):
        blockchainDB = BlockchainDB()
        return blockchainDB.lastBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        prevBlockHash = GENESIS_HASH
        self.addBlock(BlockHeight, prevBlockHash)

    def addBlock(self, BlockHeight, prevBlockHash):
        timestamp = int(time.time()) 
        coinbaseIstance = CoinbaseTx(BlockHeight)
        coinbaseTx = coinbaseIstance.CoinbaseTransaction()
        merkleRoot = coinbaseTx.TxId
        bits = 'ffff001f'
        blockheader = BlockHeader(VERSION, prevBlockHash, merkleRoot, timestamp, bits) 
        blockheader.mine()
        print(f"Block {BlockHeight} mined successfully")
        self.write_on_disk([Block(BlockHeight, 1, blockheader.__dict__, 1, coinbaseTx.to_dict()).__dict__])

    def main(self):
        lastBlock = self.fetch_last_block()
        if lastBlock is None:
            self.GenesisBlock()

        while True:
            lastBlock = self.fetch_last_block()
            BlockHeight = lastBlock["Height"] + 1
            prevBlockHash = lastBlock['BlockHeader']['blockHash']
            self.addBlock(BlockHeight, prevBlockHash)

if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()
