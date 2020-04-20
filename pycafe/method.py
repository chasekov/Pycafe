from pycafe.attribute import AttributeInfo
from pycafe.constantpool import PoolLabel
from pycafe.accessflags import AccessFlags

class Method:

    def __init__(self, pool, access_flags, name_index, descriptor_index, attributes_count, attributes_info):
        self.pool = pool
        self.access_flags = access_flags
        self.name_index = name_index
        self.descriptor_index = descriptor_index
        self.attributes_count = attributes_count    
        self.attributes_info = attributes_info

    def __str__(self):
        methodName = self.pool.get_label(self.name_index).text
        descriptor = self.pool.get_label(self.descriptor_index).text

        header = "  {}\n".format(methodName)
        header += "    descriptor: {}\n".format(descriptor)
        header += "    flags: {}\n".format(AccessFlags.of(self.access_flags))

        for attribute in self.attributes_info:
            header += "    " + str(attribute) + "\n"

        return header

    @classmethod
    def from_bytes(cls, pool, stream):
        access_flags = stream.read_as_int(2)
        name_label = PoolLabel.from_bytes(stream)
        descriptor_label = PoolLabel.from_bytes(stream)
        attributes_count = stream.read_as_int(2)

        attributes = list()
        for _ in range(0, attributes_count):
            attributes.append(AttributeInfo.from_bytes(pool, stream))

        return cls(pool, access_flags, name_label, descriptor_label, attributes_count, attributes)