import hashlib
from hashlib import sha256
from Crypto.Hash import RIPEMD160
from math import log
from Blockchain.Backend.Core.EllepticCurve.EllepticCurve import BASE58_ALPHABET

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()         

def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()

def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1

def IntToLe(n, length):
    return n.to_bytes(length, 'little')

def LeToInt(b):
    return int.from_bytes(b, 'little')


def decode_base58(s):
    num = 0

    for c in s:
        num *= 58
        num += BASE58_ALPHABET.index(c)

    combined = num.to_bytes(25, byteorder= 'big')
    checksum = combined[-4:]

    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f'bad Adress{checksum} {hash256(combined[:-4][:4])}')
        
    return combined[1:-4]

def encode_varint(i):
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + IntToLe(i, 2)
    elif i < 0x100000000:
        return b'\xfe' + IntToLe(i, 4)
    elif i < 0x10000000000000000:
        return b'\xff' + IntToLe(i, 8)
    else:
        raise ValueError('Integer too large: {}'.format(i))
    