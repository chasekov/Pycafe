from pycafe.constantpool import ConstantPool, PoolLabel
from pycafe.field import Field
from pycafe.method import Method
from pycafe.attribute import AttributeInfo
from pycafe.accessflags import AccessFlags
from pycafe.hexbuffer import HexBuffer

class Class:

    def __init__(self, minor_version, major_version, constant_pool, access_flags, class_label, super_label, interface_table, field_table, method_table, attribute_table):
        self.minor_version = minor_version
        self.major_version = major_version
        self.constant_pool = constant_pool
        self.access_flags = access_flags
        self.class_label = class_label
        self.super_label = super_label
        self.interface_table = interface_table
        self.field_table = field_table
        self.method_table = method_table
        self.attribute_table = attribute_table

    def __str__(self):
        classLabel = self.constant_pool.get_label(self.class_label)
        classNameLabel = self.constant_pool.get_label(classLabel.nameLabel)

        buffer = "class {}\n".format(classNameLabel.text)
        buffer += "  minor version: {}\n".format(self.minor_version)
        buffer += "  major version: {}\n".format(self.major_version)
        buffer += "  flags: {}\n".format(self.access_flags)

        buffer += str(self.constant_pool)
        
        # interfaceTableSize = classObj.read_as_int(2)
        # print("Interface Table Size: {}".format(interfaceTableSize))
        # for i in range(0, interfaceTableSize):
        #     print(i)

        buffer += '\n'
        for field in self.field_table:
            buffer += "{}\n".format(field)

        buffer += '{\n'
        for method in self.method_table:
            buffer += "{}\n".format(method)
        buffer += '}\n'

        for attribute in self.attribute_table:
            buffer += "{}\n".format(attribute)

        return buffer

    @classmethod
    def from_file_path(cls, file_path):
        hex_buffer = HexBuffer.from_file_path(file_path)

        # magic : cafebabe
        hex_buffer.read(4)

        minor_version = hex_buffer.read_as_int(2)
        major_version = hex_buffer.read_as_int(2)
        constant_pool = ConstantPool.from_bytes(hex_buffer)
        access_flags = AccessFlags.of(hex_buffer.read_as_int(2))
        classLabel = PoolLabel.from_bytes(hex_buffer)
        superLabel = PoolLabel.from_bytes(hex_buffer)

        interfaceTableSize = hex_buffer.read_as_int(2)
        interfaceTable = list()
        for i in range(0, interfaceTableSize):
            print(i) # to do

        fieldTableSize = hex_buffer.read_as_int(2) 
        fieldTable = list()
        for _ in range(0, fieldTableSize):
            fieldTable.append(Field.from_bytes(constant_pool, hex_buffer))

        methodTableSize = hex_buffer.read_as_int(2)
        methodTable = list()
        for _ in range(0, methodTableSize):
            methodTable.append(Method.from_bytes(constant_pool, hex_buffer))

        attributeTableSize = hex_buffer.read_as_int(2)
        attributeTable = list()
        for _ in range(0, attributeTableSize):
            attributeTable.append(AttributeInfo.from_bytes(constant_pool, hex_buffer))

        return cls(minor_version, major_version, constant_pool, access_flags, classLabel, superLabel, interfaceTable, fieldTable, methodTable, attributeTable)

    