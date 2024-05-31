from Blockchain.Backend.util.util import hash256, LeToInt, IntToLe

class BlockHeader:
    def __init__(self, version, prevBlockHash, merkleRoot, timestamp, bits):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0
        self.blockHash = ''

    def mine(self, target):
        self.blockHash = target + 1 

        while self.blockHash > target:
            self.blockHash = LeToInt(hash256(IntToLe(self.version, 4)+ bytes.fromhex(self.prevBlockHash)[::-1]+
                                bytes.fromhex(self.merkleRoot) + IntToLe(self.timestamp, 4) + 
                                self.bits + IntToLe(self.nonce, 4)))
            self.nonce += 1
            print(f" Mining Started {self.nonce}", end = '\r')
        self.blockHash = IntToLe(self.blockHash, 32).hex()[::-1]
        self.bits = self.bits.hex()
            
     