from enum import Enum

class Opcode(Enum):
    NOP = 0x00
    AALOAD = 0x32
    ALOAD_0 = 0x2a
    INVOKESPECIAL = 0xb7
    ICONST_1 = 0x04
    IADD = 0x60
    ISTORE_1 = 0x3c
    LDC2_W = 0x14
    LSTORE_2 = 0x41
    LDC = 0x12
    FSTORE = 0x38
    ASTORE = 0x3a
    DSTORE = 0x39
    RETURN = 0xb1
    BIPUSH = 0x10
    IRETURN = 0xac

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def of(bytes):
        for opcode in Opcode:
            if opcode.value == bytes:
                return opcode

        print('Unimplemented opcode : {}'.format(hex(bytes)))
        return None

class DefaultInstruction:

    def __init__(self):
        self.a = "aaaa"

    @classmethod
    def from_buffer(cls, buffer):
        return cls()