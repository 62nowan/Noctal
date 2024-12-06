from Blockchain.Backend.util.util import hash256, LeToInt, IntToLe

"""
Cette classe représente l'entête d'un bloc dans une blockchain. L'entête contient des données essentielles
qui servent à l'identification, à la validation et au minage du bloc.

    - version (int): Version de la blockchain Noctal.
    - prevBlockHash (str): Hash du bloc précédent -> permet de relier les blocs entre eux sous forme de chaine.
    - merkleRoot (str): Hash racine des transactions du bloc, calculé à partir d'un arbre de Merkle.
    - timestamp (int): Horodatage indiquant la date de création du bloc selon le temps universel.
    - bits (bytes): Niveau de difficulté pour le minage du bloc.
    - nonce (int): Valeur modifiée par le mineur pour trouver un hash valide.
    - blockHash (str): Hash final du bloc une fois qu'il a été miné.
"""

class BlockHeader:

    def __init__(self, version, prevBlockHash, merkleRoot, timestamp, bits):

        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = 0  # Initialisé à 0 pour commencer le minage
        self.blockHash = ''  # Hash final du bloc


    """
    Minage du bloc pour trouver un hash valide en fonction du seuil de difficulté spécifié (target).

    Procédure :
        - Calcule le hash en concaténant les attributs de l'entête sous forme binaire.
        - Modifie le nonce jusqu'à ce que le hash respecte la difficulté cible.
        - Une fois le hash trouvé, il est converti en format little-endian (IntToLe) et stocké.
    """
    def mine(self, target):
        self.blockHash = target + 1  # Initialisation pour entrer dans la boucle

        while self.blockHash > target:
            self.blockHash = LeToInt(hash256(
                IntToLe(self.version, 4) +
                bytes.fromhex(self.prevBlockHash)[::-1] +
                bytes.fromhex(self.merkleRoot) +
                IntToLe(self.timestamp, 4) +
                self.bits +
                IntToLe(self.nonce, 4)
            ))
            self.nonce += 1
            print(f" Mining Started {self.nonce}", end='\r')

        # Finalisation du hash et formatage
        self.blockHash = IntToLe(self.blockHash, 32).hex()[::-1]
        self.bits = self.bits.hex()
