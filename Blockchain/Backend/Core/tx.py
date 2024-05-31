from Blockchain.Backend.Core.script import Script
from Blockchain.Backend.util.util import IntToLe, bytes_needed , decode_base58, LeToInt, encode_varint, hash256

ZERO_HASH = b'\0' * 32
REWARD = 50
PRIVATE_KEY = '84451423271327909225819041603150775307597242086657049636380650670130409950196'
MINER_ADDRESS = '1Lfiwd5xq5oH1n9FsoYv5fz5CmYwNM6RwN'
SIGHASH_ALL = 1

class CoinbaseTx:
    def __init__(self, BlockHeight):
        self.BlockHeightInLittleEndian = IntToLe(BlockHeight, bytes_needed(BlockHeight))
    
    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xFFFFFFFF
        tx_ins = []
        tx_ins.append(TxIn(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)

        tx_outs = []
        target_amount = REWARD * 100000000
        target_h160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(TxOut(amount=target_amount, script_pubkey=target_script))
        coinBaseTx = Tx(1, tx_ins, tx_outs, 0)
        coinBaseTx.TxId = coinBaseTx.id()
        return coinBaseTx

class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
    
    def id(self):
        return self.hash().hex()
    
    
    def hash(self):
        return hash256(self.serialize())[::-1]
    

    def serialize(self):
        result = IntToLe(self.version, 4)
        result += encode_varint(len(self.tx_ins))

        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outs))
        
        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += IntToLe(self.locktime, 4)

        return result


    def sign_hash(self, input_index, script_pubkey):
        s = IntToLe(self.version, 4)
        s += encode_varint(len(self.tx_ins))

        for i, tx_in in enumerate(self.tx_ins):
            if i == input_index:
                s += TxIn(tx_in.prev_tx, tx_in.prev_index, script_pubkey).serialize()
            else:
                s += TxIn(tx_in.prev_tx, tx_in.prev_index).serialize()

        s += encode_varint(len(self.tx_outs))

        for tx_out in self.tx_outs:
            s += tx_out.serialize()

        s += IntToLe(self.locktime, 4)
        s += IntToLe(SIGHASH_ALL, 4)
        h256 = hash256(s)
        return int.from_bytes(h256, 'big')
    


    def sign_input(self, input_index, private_key, script_pubkey):
        z = self.sign_hash(input_index, script_pubkey)
        der = private_key.sign(z).der()
        sig = der + SIGHASH_ALL.to_bytes(1, 'big')
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig, sec])
    
    def verify_input(self, input_index, script_pubkey):
        tx_in = self.tx_ins[input_index]
        z = self.sign_hash(input_index, script_pubkey)
        combined = tx_in.script_sig + script_pubkey
        return combined.evaluate(z)

    def is_coinbase(self):
        if  len(self.tx_ins) != 1:
            return False
        
        first_input = self.tx_ins[0]
        if first_input.prev_tx != b'\x00' * 32:
            return False
        
        if first_input.prev_index != 0xFFFFFFFF:
            return False
        
        return True
    
    
    def to_dict(self):
        
        for tx_index, tx_in in enumerate(self.tx_ins):
            if self.is_coinbase():
                tx_in.script_sig.cmds[0] = LeToInt(tx_in.script_sig.cmds[0])

            tx_in.prev_tx = tx_in.prev_tx.hex()

            for index, cmd in enumerate(tx_in.script_sig.cmds):
                if isinstance(cmd, bytes):
                    tx_in.script_sig.cmds[index] = cmd.hex()

            tx_in.script_sig = tx_in.script_sig.__dict__
            self.tx_ins[tx_index] = tx_in.__dict__


        for index, tx_out in enumerate(self.tx_outs):
            tx_out.script_pubkey.cmds[2] = tx_out.script_pubkey.cmds[2].hex()
            tx_out.script_pubkey = tx_out.script_pubkey.__dict__
            self.tx_outs[index] = tx_out.__dict__
        
        return self.__dict__



class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig=None, sequence=0xFFFFFFFF):
        self.prev_tx = prev_tx
        self.prev_index = prev_index

        if script_sig is None:
            self.script_sig = Script()
        else:
            self.script_sig = script_sig

        self.sequence = sequence

    def serialize(self):
        result = self.prev_tx[::-1]
        result += IntToLe(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += IntToLe(self.sequence, 4)
        return result


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def serialize(self):
        result = IntToLe(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result
