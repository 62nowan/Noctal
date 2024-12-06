from Blockchain.Backend.Core.network.connection import Node
from Blockchain.Backend.Core.database.database import BlockchainDB
from Blockchain.Backend.Core.network.network import requestBlock
from threading import Thread

class syncManager:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    
    def SpinUpTheServer(self):
        self.server = Node(self.host, self.port)
        self.server.startServer()
        print("SERVER STARTED")
        print(f"[LISTENING] at {self.host}:{self.port}")

        while True:
            self.conn, self.addr = self.server.acceptConnection()
            handleConn = Thread(target = self.handleConnection)
            handleConn.start()


    def handleConnection(self):
        envelope = self.server.read()
        try:
            if envelope.command == requestBlock.command:
                start_block, end_block = requestBlock.parse(envelope.stream())
                print(f"Start block is {start_block} \n End block is {end_block}")

        except Exception as e:
            print(f"Error while processing the client request \n {e}")


    def startDownload(self, port):
        lastBlock = BlockchainDB().lastBlock()

        if not lastBlock:
            lastBlockHeader = "00003a9559b5a78a9d2ce0f896a8b45bfafec7742c5c72669c8afd0431dc5402"
        else:
            lastBlockHeader = lastBlock['BlockHeader']['blockHash']
        
        startBlock = bytes.fromhex(lastBlockHeader)

        getHeaders = requestBlock(startBlock = startBlock)
        self.connect = Node(self.host, port)
        self.socket = self.connect.connect(port)
        self.connect.send(getHeaders)
