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

def encode_base58(s):
    # determine how many 0 bytes (b'\x00') s starts with
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    # convert to big endian integer
    num = int.from_bytes(s, 'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num, 58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result



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
    

def merkle_parent_level(hashes):
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    
    parent_level = []

    for i in range(0, len(hashes), 2):
        parent = hash256(hashes[i] + hashes[i+1])
        parent_level.append(parent)

    return parent_level


def merkle_root(hashes):
    current_level = hashes

    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)

    return current_level[0]


def target_to_bits(target):
    raw_bytes = target.to_bytes(32, "big")
    raw_bytes = raw_bytes.lstrip(b"\x00")  # <1>
    if raw_bytes[0] > 0x7F:  # <2>
        exponent = len(raw_bytes) + 1
        coefficient = b"\x00" + raw_bytes[:2]
    else:
        exponent = len(raw_bytes)  # <3>
        coefficient = raw_bytes[:3]  # <4>
    new_bits = coefficient[::-1] + bytes([exponent])  # <5>
    return new_bits