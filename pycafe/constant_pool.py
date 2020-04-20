import sys
from enum import Enum

def entry_from_bytes(bytes):
    bit = bytes.read_as_int(1)
    typeFlag = TypeFlag.of(bit)

    if typeFlag == TypeFlag.UTF8:
        return Utf8.from_bytes(bytes)
    elif typeFlag == TypeFlag.FLOAT:
        return Float.from_bytes(bytes)
    elif typeFlag == TypeFlag.LONG:
        return Long.from_bytes(bytes)
    elif typeFlag == TypeFlag.DOUBLE:
        return Double.from_bytes(bytes)    
    elif typeFlag == TypeFlag.CLASS_REFERENCE:
        return ClassReference.from_bytes(bytes)
    elif typeFlag == TypeFlag.STRING_REFERENCE:
        return StringReference.from_bytes(bytes)
    elif typeFlag == TypeFlag.FIELD_REFERENCE:
        return FieldReference.from_bytes(bytes)
    elif typeFlag == TypeFlag.METHOD_REFERENCE:
        return MethodReference.from_bytes(bytes)
    elif typeFlag == TypeFlag.NAMEANDTYPE_REFERENCE:
        return NameAndType.from_bytes(bytes)
    else:
        sys.exit("Failed cause we don't have {} typeFlag defined".format(bit))
        return None

class TypeFlag(Enum):
    UTF8 = 0x0001
    FLOAT = 0x0004
    LONG = 0x0005
    DOUBLE = 0x0006
    CLASS_REFERENCE = 0x0007
    STRING_REFERENCE = 0x0008
    FIELD_REFERENCE = 0x0009
    METHOD_REFERENCE = 0x000A
    NAMEANDTYPE_REFERENCE = 0x000C

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def of(bytes):
        for flag in TypeFlag:
            if flag.value == bytes:
                return flag

        return None

class ConstantPool:

    def __init__(self, pool_size, constants):
        self.pool_size = pool_size
        self.constants = constants

    def get_index(self, index):
        return self.constants[index - 1]

    def get_label(self, label):
        return self.constants[label.index - 1]

    def resolve_as_utf8(self, label):
        return self.constants[label.index - 1].text

    def __str__(self):
        buffer = 'Constant pool:\n'

        for i, entry in enumerate(self.constants, 0):
            if entry == None:
                continue

            buffer += "  #{} = {}\n".format(i+1, entry)
    
        return buffer

    @classmethod
    def from_bytes(cls, stream):
        constants = list()
        pool_size = stream.read_as_int(2)

        i = 1
        while i < pool_size:
            entry = entry_from_bytes(stream)
            constants.append(entry)

            # Phantom entry for Long/Double
            if isinstance(entry, (Long, Double)):
                constants.append(None)
                i = i + 1
            
            i = i + 1

        return cls(pool_size, constants)     

class PoolLabel: 

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "#" + str(self.index)

    @classmethod
    def from_bytes(cls, stream):
        return cls(stream.read_as_int(2))

class Double:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "[Double] value: {}D".format(self.value)

    @classmethod
    def from_bytes(cls, stream):
        return cls(stream.read_as_int(8))

class Long:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "[Long] value: {}L".format(self.value)

    @classmethod
    def from_bytes(cls, stream):
        return cls(stream.read_as_int(8))

class Float:

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "[Float] value: {}f".format(self.value)

    @classmethod
    def from_bytes(cls, stream):
        return cls(stream.read_as_float(4))

class StringReference:

    def __init__(self, utf8Label):
        self.utf8Label = utf8Label

    def __str__(self):
        return "[StringReference] utf8Label: {}".format(self.utf8Label)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream))

class FieldReference:
    def __init__(self, classLabel, nameAndTypeLabel):
        self.classLabel = classLabel
        self.nameAndTypeLabel = nameAndTypeLabel

    def __str__(self):
        return "[FieldReference] classLabel: {} nameAndTypeLabel: {}".format(self.classLabel, self.nameAndTypeLabel)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream), PoolLabel.from_bytes(stream))

class Utf8:
    def __init__(self, text):
        self.text = text

    def __str__(self):
        return "[Utf8] : " + self.text

    @classmethod
    def from_bytes(cls, stream):
        byteSize = stream.read_as_int(2)
        return cls(stream.read_as_utf8(byteSize))

class NameAndType:

    def __init__(self, nameLabel, typeLabel):
        self.nameLabel = nameLabel
        self.typeLabel = typeLabel

    def __str__(self):
        return "[NameAndType] nameLabel: {} typeLabel: {}".format(self.nameLabel, self.typeLabel)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream), PoolLabel.from_bytes(stream))

class MethodReference:

    def __init__(self, classLabel, descriptorLabel):
        self.classLabel = classLabel
        self.descriptorLabel = descriptorLabel

    def __str__(self):
        return "[MethodReference] classLabel: {} descriptorLabel: {}".format(self.classLabel, self.descriptorLabel)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream), PoolLabel.from_bytes(stream))

class ClassReference:

    def __init__(self, nameLabel):
        self.nameLabel = nameLabel

    def __str__(self):
        return "[ClassReference] nameLabel: {}".format(self.nameLabel)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream))