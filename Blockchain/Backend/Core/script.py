from Blockchain.Backend.util.util import IntToLe, encode_varint
from Blockchain.Backend.Core.EllepticCurve.op import OP_CODE_FUNCTION
class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds
    
    def __add__(self, other):
        return Script(self.cmds + other.cmds)

    def serialize(self):
        result = b""
        for cmd in self.cmds:
            if type(cmd) == int:
                result += IntToLe(cmd, 1)
            else:
                length = len(cmd)
                if length < 75:
                    result += IntToLe(length, 1)
                elif length > 75 and length < 0x100:

                    result += IntToLe(76, 1)
                    result += IntToLe(length, 1)
                elif length >= 0x100 and length <= 520:
                    result += IntToLe(77, 1)
                    result += IntToLe(length, 2)
                else:
                    raise ValueError("too long an cmd")

                result += cmd

        total = len(result)

        return encode_varint(total) + result

    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []
        while len(cmds) > 0:
            cmd = cmds.pop(0)

            if type(cmd) == int:
                operation = OP_CODE_FUNCTION[cmd]

                if cmd == 172:
                    if not operation(stack, z):
                        print(f"Error in Signature Verification")
                        return False 
                
                elif not operation(stack):
                        print(f"Error in Signature Verification")
                        return False 
            else:
                stack.append(cmd)
        return True


    @classmethod 
    def p2pkh_script(cls, h160):
        return Script([0x76, 0xa9, h160, 0x88, 0xac])