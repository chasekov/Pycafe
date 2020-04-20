import zipfile
import os
import struct

from opcodes import Opcodes
from constant_pool import ConstantPool, PoolLabel
from field import Field
from method import Method
from attribute import AttributeInfo
from access_flags import AccessFlags

CLASS_FILE_EXTENSION = '.class'

def extract_zip(file_name, destination):
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(destination)

def find_class_files(directory):
    results = list()
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(CLASS_FILE_EXTENSION):
                results.append(os.path.join(root, file))
    return results

def read_as_hex_groups(file_path):
    with open(file_path, 'rb') as f:
        hex = f.read().hex()
        return [ ''.join(x) for x in zip(hex[0::2], hex[1::2]) ]

class ClassFile:

    def __init__(self, classFile):
        self.hexgroups = read_as_hex_groups(classFile)
        self.index = 0

    def read(self, byte_count):
        read = self.hexgroups[self.index:self.index+byte_count]
        self.index += byte_count
        return read

    def read_as_int(self, byte_count):
        groups = self.read(byte_count)
        combined = "".join(groups)

        return int(combined, 16)

    def read_as_float(self, byte_count):
        groups = self.read(byte_count)
        combined = "".join(groups)

        return struct.unpack("f", struct.pack("i", int(combined, 16)))[0]

for classFile in find_class_files('targetdir'):
    print("Class file : "  + classFile)

    classObj = ClassFile(classFile)
    print("\tMagic: " + str(classObj.read(4)))
    print("\tMinor Version: " + str(classObj.read_as_int(2)))
    print("\tMajor Version: " + str(classObj.read_as_int(2)))
    print()

    pool = ConstantPool.from_bytes(classObj)
    print()

    accessFlags = AccessFlags.of(classObj.read_as_int(2))
    print("Access Flags: " + str(accessFlags))
    print("Class Label: " + str(PoolLabel.from_bytes(classObj)))
    print("Super Class Label: " + str(PoolLabel.from_bytes(classObj)))

    interfaceTableSize = classObj.read_as_int(2)
    print("Interface Table Size: " + str(interfaceTableSize))
    for i in range(0, interfaceTableSize):
        print(i)

    fieldTableSize = classObj.read_as_int(2)
    print("Field Table Size: " + str(fieldTableSize))
    for _ in range(0, fieldTableSize):
        print(str(Field.from_bytes(pool, classObj)))

    methodTableSize = classObj.read_as_int(2)
    print("Method Table Size: " + str(methodTableSize))
    for _ in range(0, methodTableSize):
        print(str(Method.from_bytes(pool, classObj)))

    attributeTableSize = classObj.read_as_int(2)
    print("Attribute Table Size: " + str(attributeTableSize))
    for _ in range(0, attributeTableSize):
        print("\t" + str(AttributeInfo.from_bytes(pool, classObj)))
