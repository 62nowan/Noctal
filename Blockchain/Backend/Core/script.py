from Blockchain.Backend.util.util import IntToLe, encode_varint
class Script:
    def __init__(self, cmds=None):
        if cmds is None:
            self.cmds = []
        else:
            self.cmds = cmds
    
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
                    raise ValueError("Too long an cmd")

                result += cmd

        total = len(result)

        return encode_varint(total) + result


    @classmethod 
    def p2pkh_script(cls, h160):
        return Script([0x76, 0xa9, h160, 0x88, 0xac])