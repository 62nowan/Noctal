import sys
import secrets

sys.path.append('/Users/shash/Noctal')  # -> PATH vers le projet 

from Blockchain.Backend.util.EllepticCurve import Sha256Point
from Blockchain.Backend.util.util import hash160, hash256 
from Blockchain.Backend.Core.database.database import AccountDB
"""
La classe account permet de générer une paire de clés (clé privée et clé publique) 
et une adresse publique associée, en utilisant la cryptographie des modules importés.
"""
class account:
    """
        createKeys() -> Génère une clé privée et publique ainsi qu'une adresse publique

        - privateKey (int): Clé privée générée aléatoirement afin de signer des transactions.
        - PublicAddress (str): Adresse publique générée à partir de la clé publique compressée, encodée en Base58.
        """
    def createKeys(self):
        # Point générateur de la courbe elliptique (SECP256k1)
        Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
        Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        G = Sha256Point(Gx, Gy)

        # Génération de la clé privée (entier aléatoire de 256 bits)
        self.privateKey = secrets.randbits(256)

        # Calcul de la clé publique en multipliant la clé privée par le point G 
        unCompressPublicKey = self.privateKey * G
        xpoint = unCompressPublicKey.x
        ypoint = unCompressPublicKey.y

        # Compression de la clé publique en fonction de la parité de la coordonnée de y
        if ypoint.num % 2 == 0:
            compressKey = b'\x02' + xpoint.num.to_bytes(32, 'big')
        else:
            compressKey = b'\x03' + xpoint.num.to_bytes(32, 'big')

        # Calcul de l'adresse publique
        hsh160 = hash160(compressKey)  # hash160 
        main_prefix = b'\x00'  # Préfixe Mainnet (ici "1")
        newAddr = main_prefix + hsh160

        # Ajout du checksum (4 premiers octets de SHA-256)
        checksum = hash256(newAddr)[:4]
        newAddr = newAddr + checksum

        # Encodage en Base58
        BASE58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
        count = 0
        for c in newAddr:
            if c == 0:
                count += 1
            else:
                break
        num = int.from_bytes(newAddr, 'big')
        prefix = '1' * count
        result = ''
        while num > 0:
            num, mod = divmod(num, 58)
            result = BASE58_ALPHABET[mod] + result
        self.PublicAddress = prefix + result

        # Affichage des résultats
        print(f"Private Key {self.privateKey}")
        print(f"Public Key {self.PublicAddress}")
 
if __name__ == '__main__':
    """
    Exemple d'utilisation de la classe account:
    1. Génère une paire de clés et une adresse publique.
    2. Sauvegarde les informations de l'utilisateur dans le fichier account.txt.
    """
    acct = account()
    acct.createKeys()
    AccountDB().write([acct.__dict__])
