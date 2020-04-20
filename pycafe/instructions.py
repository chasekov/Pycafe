from opcodes import Opcode

class Instruction:

    def __init__(self, opcode):
        self.opcode = opcode

    def __str__(self):
        return "{}".format(self.opcode)

    @staticmethod
    def from_buffer(buffer):
        int_opcode = buffer.read_as_int(1)
        opcode = Opcode.of(int_opcode)

        if opcode == Opcode.INVOKESPECIAL:
            return InvokeSpecial.from_buffer(buffer)
        elif opcode == Opcode.LDC:
            return Ldc.from_buffer(buffer)
        elif opcode == Opcode.LDC2_W:
            return Ldc2_w.from_buffer(buffer)
        elif opcode == Opcode.FSTORE:
            return Fstore.from_buffer(buffer)
        elif opcode == Opcode.ASTORE:
            return Astore.from_buffer(buffer)
        elif opcode == Opcode.DSTORE:
            return Dstore.from_buffer(buffer)
        elif opcode == Opcode.BIPUSH:
            return Bipush.from_buffer(buffer)
        else: 
            return Instruction(opcode)

class InvokeSpecial(Instruction):

    def __init__(self, byte_1, byte_2):
        Instruction.__init__(self, Opcode.INVOKESPECIAL)
        self.byte_1 = byte_1
        self.byte_2 = byte_2

    def __str__(self):
        return "{} {} {}".format(self.opcode, self.byte_1, self.byte_2)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.read_as_int(1), buffer.read_as_int(1))

class Ldc2_w(Instruction):

    def __init__(self, byte_1, byte_2):
        Instruction.__init__(self, Opcode.LDC2_W)
        self.byte_1 = byte_1
        self.byte_2 = byte_2

    def __str__(self):
        return "{} {} {}".format(self.opcode, self.byte_1, self.byte_2)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.read_as_int(1), buffer.read_as_int(1))

class Ldc(Instruction):

    def __init__(self, byte_1):
        Instruction.__init__(self, Opcode.LDC)
        self.byte_1 = byte_1

    def __str__(self):
        return "{} {}".format(self.opcode, self.byte_1)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.read_as_int(1))

class Fstore(Instruction):

    def __init__(self, byte_1):
        Instruction.__init__(self, Opcode.FSTORE)
        self.byte_1 = byte_1

    def __str__(self):
        return "{} {}".format(self.opcode, self.byte_1)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.read_as_int(1))

class Astore(Instruction):

    def __init__(self, byte_1):
        Instruction.__init__(self, Opcode.ASTORE)
        self.byte_1 = byte_1

    def __str__(self):
        return "{} {}".format(self.opcode, self.byte_1)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.read_as_int(1))

class Dstore(Instruction):

    def __init__(self, byte_1):
        Instruction.__init__(self, Opcode.DSTORE)
        self.byte_1 = byte_1

    def __str__(self):
        return "{} {}".format(self.opcode, self.byte_1)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.read_as_int(1))

class Bipush(Instruction):

    def __init__(self, byte_1):
        Instruction.__init__(self, Opcode.BIPUSH)
        self.byte_1 = byte_1

    def __str__(self):
        return "{} {}".format(self.opcode, self.byte_1)

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.read_as_int(1))