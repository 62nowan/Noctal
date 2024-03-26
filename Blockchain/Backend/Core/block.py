class Block:
    def __init__(self, Height, BlockSize, BlockHeader, TxCount, Txs):
        self.Height = Height                                             
        self.BlockSize = BlockSize                                        
        self.BlockHeader = BlockHeader                                    
        self.TxCount = TxCount                                            
        self.Txs = Txs                                                   