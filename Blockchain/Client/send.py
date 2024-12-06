import time
from Blockchain.Backend.util.util import decode_base58
from Blockchain.Backend.Core.script import Script
from Blockchain.Backend.Core.tx import TxIn, TxOut, Tx
from Blockchain.Backend.Core.database.database import AccountDB
from Blockchain.Backend.util.EllepticCurve import PrivateKey
"""
La classe Send est utilisée pour créer, préparer et signer une transaction dans la blockchain.
    
    - COIN (int): Conversion de l'unité principale en la plus petite unité voulue (par exemple 1 bitcoin = 100000000 satoshis).
    - FromPublicAdress (str): Adresse publique de l'expéditeur.
    - toAccount (str): Adresse publique du destinataire.
    - Amount (int): Montant à envoyer, converti en petites unités.
    - utxos (dict): Transactions non dépensées (UTXOs) disponibles pour financer la transaction (c.à.d renvoie une transaction de
                    sortie de la différence entre la valeur du montant à envoyer et le solde total de l'/des utxo(s)).
"""
class Send:
    
    def __init__(self, fromAccount, toAccount, Amount, UTXOS):
        self.COIN = 100000000  # Conversion d'une unité principale en unités plus petites
        self.FromPublicAdress = fromAccount
        self.toAccount = toAccount
        self.Amount = Amount * self.COIN  # Conversion en unités plus petites
        self.utxos = UTXOS


    """
    scriptPubKey() -> Génère un script de verrouillage pour une adresse donnée (PublicAdress).
    """
    def scriptPubKey(self, PublicAdress):
        h160 = decode_base58(PublicAdress)  # Décodage Base58 pour obtenir le hash160
        script_pubkey = Script().p2pkh_script(h160)  # Génère un script P2PKH
        return script_pubkey


    """
    getPrivateKey() -> Récupère la clé privée associée à l'adresse publique de l'expéditeur.
    """
    def getPrivateKey(self):
        AllAccounts = AccountDB().read()
        for account in AllAccounts:
            if account['PublicAddress'] == self.FromPublicAdress:
                return account['privateKey']


    """
    prepareTxIn() -> Prépare les entrées (TxIns) de la transaction en collectant les UTXOs nécessaires.
    """
    def prepareTxIn(self):
        TxIns = []
        self.Total = 0
        self.from_address_script_pubkey = self.scriptPubKey(self.FromPublicAdress)
        self.fromPubKeyHash = self.from_address_script_pubkey.cmds[2]  # Hash public key

        newutxos = {}

        try:
            # Attente des UTXOs si nécessaire
            while len(newutxos) < 1:
                newutxos = dict(self.utxos)
                time.sleep(2)
        except Exception as e:
            print(f"Error in converting the Managed dict to Normal dict")

        # Parcours des UTXOs pour collecter les fonds nécessaires
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


    """
    prepareTxOut() -> Prépare les sorties (TxOuts) de la transaction, y compris la sortie pour le destinataire 
                      et la différence pour l'expéditeur.
    """
    def prepareTxOut(self):
        TxOuts = []
        to_scriptPubKey = self.scriptPubKey(self.toAccount)  # Script pour le destinataire
        TxOuts.append(TxOut(self.Amount, to_scriptPubKey))  # Montant envoyé au destinataire

        self.fee = self.COIN  # Frais de transaction
        self.changeAmount = self.Total - self.Amount - self.fee  # Calcul de la différence

        # Ajout de la différence à l'expéditeur
        TxOuts.append(TxOut(self.changeAmount, self.from_address_script_pubkey))
        return TxOuts


    """
    signTx() -> Signe chaque entrée (TxIn) de la transaction en utilisant la clé privée de l'expéditeur.
    """
    def signTx(self):
        secret = self.getPrivateKey()
        priv = PrivateKey(secret=secret)
        
        for index, input in enumerate(self.TxIns):
            self.TxObj.sign_input(index, priv, self.from_address_script_pubkey)
        
        return True


    """
    prepareTransactions() -> Prépare et signe la transaction.
    """
    def prepareTransaction(self):
        self.TxIns = self.prepareTxIn()

        if self.isBalenceEnough:
            self.TxOuts = self.prepareTxOut()
            self.TxObj = Tx(1, self.TxIns, self.TxOuts, 0)  # Version 1, inputs, outputs, locktime 0
            self.TxObj.TxId = self.TxObj.id()  # Calcul du TxId
            self.signTx()
            return self.TxObj
        
        return False
