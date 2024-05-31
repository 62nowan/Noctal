from flask import  Flask, render_template, request, redirect, url_for
from Blockchain.Client.send import Send
from Blockchain.Backend.Core.tx import Tx
from Blockchain.Backend.Core.database.database import BlockchainDB
from Blockchain.Backend.util.util import encode_base58
from hashlib import sha256

app = Flask(__name__)
main_prefix = b'\x00'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/transactions')
def transactions():
    return "<h1>Transactions</h1>"

@app.route('/mempool')
def mempool():
    return "<h1>Mempool</h1>"

@app.route('/search')
def search():
    return "<h1>Search</h1>"


def readDatabase():
    ErrorFlag = True
    while ErrorFlag:
        try:
            blockchain = BlockchainDB()
            blocks = blockchain.read()
            ErrorFlag = False 
        except:
            ErrorFlag = True
            print(" Error reading database")
    return blocks

@app.route('/block')
def block():
    if request.args.get('blockHeader'):
        return redirect(url_for('showBlock', blockHeader=request.args.get('blockHeader')) )
    else:
        blocks = readDatabase()
        return render_template('block.html', blocks = blocks)

@app.route('/block/<blockHeader>')
def showBlock(blockHeader):
    blocks = readDatabase()
    for block in blocks:
        if block['BlockHeader']['blockHash'] == blockHeader:
            return render_template('blockDetails.html', block = block, main_prefix = main_prefix, 
            encode_base58 = encode_base58, bytes = bytes, sha256 = sha256)
    
    return "<h1> Invalid Identifier </h1>"

@app.route('/address')
def address():
    return "<h1> Address Page</h1>"


@app.route('/wallet', methods = ["GET", "POST"])  
def wallet():
    message = ''
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        ToAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount", type = int)
        sendCoin = Send(FromAddress, ToAddress, Amount, UTXOS)
        TxObj = sendCoin.prepareTransaction()

        scriptPubKey = sendCoin.scriptPubKey(FromAddress)
        verified = True
            
        if not TxObj:
            message = "Invalid Transaction"

        if isinstance(TxObj, Tx):
            for index, tx in enumerate(TxObj.tx_ins):
                if not TxObj.verify_input(index, scriptPubKey):
                    verified = False
                    
            if verified:
                MEMPOOL[TxObj.TxId] = TxObj
                message = "Transaction added in Memory Pool"


    return render_template('wallet.html', message = message)


def main(utxos, MemPool):
    global UTXOS 
    global MEMPOOL 
    UTXOS = utxos
    MEMPOOL = MemPool
    app.run()
