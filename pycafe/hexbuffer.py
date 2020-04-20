import struct
import codecs

class HexBuffer:

    def __init__(self, hexgroups):
        self.hexgroups = hexgroups
        self.index = 0

    def has_more(self):
        return self.index != len(self.hexgroups)

    def bytes_read(self):
        return self.index

    def read_as_groups(self, byte_count):
        groups = self.hexgroups[self.index:self.index+byte_count]
        self.index += byte_count
        return groups

    def read_as_int_groups(self, byte_count):
        groups = self.read_as_groups(byte_count)
        int_groups = list()

        for group in groups:
            int_groups.append(int(group, 16))

        return int_groups

    def read(self, byte_count):
        groups = self.read_as_groups(byte_count)
        return "".join(groups)

    def read_as_utf8(self, byte_count):
        return codecs.decode(self.read(byte_count), "hex").decode('utf-8')

    def read_as_int(self, byte_count):
        data = self.read(byte_count)
        return int(data, 16)

    def read_as_float(self, byte_count):
        data = self.read(byte_count)
        return struct.unpack("f", struct.pack("i", int(data, 16)))[0]

    @classmethod
    def from_string(cls, hex_string):
        return cls([ ''.join(x) for x in zip(hex_string[0::2], hex_string[1::2]) ])

    @classmethod
    def from_file(cls, file):
        hex = file.read().hex()
        return cls([ ''.join(x) for x in zip(hex[0::2], hex[1::2]) ])

    @classmethod
    def from_file_path(cls, file_path):
        with open(file_path, 'rb') as f:
            return cls.from_file(f)