"""
La classe block est un conteneur qui permet de stocker des informations spécifiques dans une chaine.

    - Height (int): La hauteur du bloc dans la chaîne.
    - BlockSize (int): La taille du bloc en octets.
    - BlockHeader (objet cf -> blockheader.py): L'entête du bloc contenant d'autres données essentielles (comme le hash précédent, 
                                                le merkle root, le timestamp, ...)
    - TxCount (int): Le nombre total de transactions dans ce bloc.
    - Txs (list): La liste des transactions contenues dans ce bloc.
"""
class Block:
    def __init__(self, Height, BlockSize, BlockHeader, TxCount, Txs):
        self.Height = Height                                              
        self.BlockSize = BlockSize                                       
        self.BlockHeader = BlockHeader                                  
        self.TxCount = TxCount                                           
        self.Txs = Txs                                             
