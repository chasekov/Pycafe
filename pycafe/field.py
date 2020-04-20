from pycafe.attribute import AttributeInfo
from pycafe.constantpool import PoolLabel

class Field:

    def __init__(self, access_flags, name_index, descriptor_index, attributes_count, attributes_info):
        self.access_flags = access_flags
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.attributes_count = attributes_count    
        self.attributes_info = attributes_info

    def __str__(self):
        header = "[Field] nameLabel: {} descriptorLabel: {} attributeCount:{}\n".format(self.name_index, self.descriptor_index, self.attributes_count) 

        for attribute in self.attributes_info:
            header += "\t" + str(attribute) + "\n"

        return header

    @classmethod
    def from_bytes(cls, pool, stream):
        access_flags = stream.read(2)
        name_index = PoolLabel.from_bytes(stream)
        descriptor_index = PoolLabel.from_bytes(stream)
        attributes_count = stream.read_as_int(2)

        attributes = list()
        for _ in range(0, attributes_count):
            attributes.append(AttributeInfo.from_bytes(pool, stream))

        return cls(access_flags, name_index, descriptor_index, attributes_count, attributes)