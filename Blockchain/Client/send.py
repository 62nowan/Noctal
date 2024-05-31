from Blockchain.Backend.util.util import decode_base58
from Blockchain.Backend.Core.script import Script
from Blockchain.Backend.Core.tx import TxIn, TxOut, Tx
from Blockchain.Backend.Core.database.database import AccountDB
from Blockchain.Backend.Core.EllepticCurve.EllepticCurve import PrivateKey
import time

class Send:
    def __init__(self, fromAccount, toAccount, Amount, UTXOS):
        self.COIN = 100000000                 #Un BTC
        self.FromPublicAdress = fromAccount
        self.toAccount = toAccount
        self.Amount = Amount * self.COIN
        self.utxos = UTXOS


    def scriptPubKey(self, PublicAdress):
        h160 = decode_base58(PublicAdress)
        script_pubkey = Script().p2pkh_script(h160)
        return script_pubkey
    

    def getPrivateKey(self):
        AllAcounts = AccountDB().read()
        for account in AllAcounts:
            if account['PublicAddress'] == self.FromPublicAdress:
                return account['privateKey']


    def prepareTxIn(self):
        TxIns = []
        self.Total = 0

        self.from_address_script_pubkey = self.scriptPubKey(self.FromPublicAdress)
        self.fromPubKeyHash = self.from_address_script_pubkey.cmds[2]

        newutxos = {}

        try:
            while len(newutxos) < 1:
                newutxos = dict(self.utxos)
                time.sleep(2)
        except Exception as e:
            print(f"Error in converting the Managed dict to Normal dict")

        for Txbyte in newutxos:
            if self.Total < self.Amount:
                TxObj = newutxos[Txbyte]

                for index, txout in enumerate(TxObj.tx_outs):
                    if txout.script_pubkey.cmds[2] == self.fromPubKeyHash:
                        self.Total += txout.amount
                        prev_tx = bytes.fromhex(Txbyte)
                        TxIns.append(TxIn(prev_tx, index))
                else:
                    break
        self.isBalenceEnough = True 
        if self.Total < self.Amount:
            self.isBalenceEnough = False
            
        return TxIns


    def prepareTxOut(self):
        TxOuts = []
        to_scriptPubKey = self.scriptPubKey(self.toAccount)
        TxOuts.append(TxOut(self.Amount, to_scriptPubKey))

        self.fee = self.COIN #frais de transaction
        self.changeAmount = self.Total - self.Amount - self.fee

        TxOuts.append(TxOut(self.changeAmount, self.from_address_script_pubkey))
        return TxOuts


    def signTx(self):
        secret = self.getPrivateKey()
        priv = PrivateKey(secret= secret)
        
        for index, input in enumerate(self.TxIns):
            self.TxObj.sign_input(index, priv, self.from_address_script_pubkey)
        
        return True

    def prepareTransaction(self):
        self.TxIns = self.prepareTxIn()

        if self.isBalenceEnough:
            self.TxOuts = self.prepareTxOut()
            self.TxObj = Tx(1, self.TxIns, self.TxOuts, 0)
            self.TxObj.TxId = self.TxObj.id()
            self.signTx()
            return self.TxObj
        
        return False
        


