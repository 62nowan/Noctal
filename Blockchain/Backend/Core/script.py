from Blockchain.Backend.util.util import IntToLe, encode_varint
from Blockchain.Backend.util.op import OP_CODE_FUNCTION

"""
La classe Script représente un script issue du code Bitcoin utilisé pour verrouiller ou déverrouiller des transactions.
Les scripts sont composés d'une séquence de commandes ou de données qui définissent les conditions nécessaires pour
dépenser une transaction.

    - cmds (list): Une liste de commandes et de données associées au script.
"""
class Script:

    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds


    """
    Combine deux scripts pour en former un seul.
    """
    def __add__(self, other):
        return Script(self.cmds + other.cmds)


    """
    Sérialise le script en une séquence binaire.
    """
    def serialize(self):
        result = b""
        for cmd in self.cmds:
            if type(cmd) == int:
                result += IntToLe(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    result += IntToLe(length, 1)
                elif 75 <= length < 0x100:
                    result += IntToLe(76, 1)
                    result += IntToLe(length, 1)
                elif 0x100 <= length <= 520:
                    result += IntToLe(77, 1)
                    result += IntToLe(length, 2)
                else:
                    raise ValueError("Commande trop longue")

                result += cmd

        total = len(result)
        return encode_varint(total) + result


    """
    Évalue le script en simulant une pile (stack).
    Utilisé pour vérifier la validité des signatures ou autres conditions.
    """
    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            if type(cmd) == int:
                # Si l'instruction est un opcode
                operation = OP_CODE_FUNCTION[cmd]

                if cmd == 172:  # OP_CHECKSIG
                    if not operation(stack, z):
                        print("Erreur dans la vérification de la signature")
                        return False
                elif not operation(stack):
                    print("Erreur dans l'exécution de l'opération")
                    return False
            else:
                # Si l'instruction est une donnée, on l'ajoute à la pile
                stack.append(cmd)
        return True

    
    """
    Génère un script P2PKH (Pay To PubKey Hash).
    """
    @classmethod
    def p2pkh_script(cls, h160):
        return Script([0x76, 0xa9, h160, 0x88, 0xac])
