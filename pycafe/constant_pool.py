import codecs
import sys

def entry_from_bytes(bytes):
    typeFlag = bytes.read_as_int(1)

    if typeFlag == 1:
        return Utf8.from_bytes(bytes)
    elif typeFlag == 4:
        return Float.from_bytes(bytes)
    elif typeFlag == 5:
        return Long.from_bytes(bytes)    
    elif typeFlag == 7:
        return ClassReference.from_bytes(bytes)
    elif typeFlag == 8:
        return StringReference.from_bytes(bytes)
    elif typeFlag == 9:
        return FieldReference.from_bytes(bytes)
    elif typeFlag == 10:
        return MethodReference.from_bytes(bytes)
    elif typeFlag == 12:
        return NameAndType.from_bytes(bytes)
    else:
        sys.exit("Failed cause we don't have {} typeFlag defined".format(typeFlag))
        return None

class ConstantPool:

    def __init__(self, pool_size, constants):
        self.pool_size = pool_size
        self.constants = constants

    def get_index(self, index):
        return self.constants[index - 1]

    def resolve_as_utf8(self, index):
        return self.constants[index - 1].text

    @classmethod
    def from_bytes(cls, stream):
        constants = list()
        pool_size = stream.read_as_int(2)

        print("Constant Pool:")
        i = 1

        while i < pool_size:
            entry = entry_from_bytes(stream)
            print('\t#' + str(i) + " = " + str(entry))
            constants.append(entry)

            # Phantom entry for Long/Double
            if isinstance(entry, Long):
                constants.append('')
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
        return "[FieldReference] classLabel: " + str(self.classLabel) + " nameAndTypeLabel: " + str(self.nameAndTypeLabel)

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
        hexString = "".join(stream.read(byteSize))
        content = codecs.decode(hexString, "hex").decode('utf-8')

        return cls(content)

class NameAndType:

    def __init__(self, nameLabel, typeLabel):
        self.nameLabel = nameLabel
        self.typeLabel = typeLabel

    def __str__(self):
        return "[NameAndType] nameLabel: " + str(self.nameLabel) + " typeLabel: " + str(self.typeLabel)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream), PoolLabel.from_bytes(stream))

class MethodReference:

    def __init__(self, classLabel, descriptorLabel):
        self.classLabel = classLabel
        self.descriptorLabel = descriptorLabel

    def __str__(self):
        return "[MethodReference] classLabel: " + str(self.classLabel) + " descriptorLabel: " + str(self.descriptorLabel)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream), PoolLabel.from_bytes(stream))

class ClassReference:

    def __init__(self, nameLabel):
        self.nameLabel = nameLabel

    def __str__(self):
        return "[ClassReference] nameLabel: " + str(self.nameLabel)

    @classmethod
    def from_bytes(cls, stream):
        return cls(PoolLabel.from_bytes(stream))