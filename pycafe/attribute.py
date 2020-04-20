from constant_pool import ConstantPool, Utf8, PoolLabel
from opcodes import Opcode
from hex_buffer import HexBuffer
from instructions import Instruction

class AttributeInfo:

    def __init__(self, attribute_label, attribute_length, info):
        self.attribute_label = attribute_label
        self.attribute_length = attribute_length
        self.info = info

    def __str__(self):
        return str(self.info)

    @classmethod
    def from_bytes(cls, pool, stream):
        attribute_label = PoolLabel.from_bytes(stream)
        attributes_length = stream.read_as_int(4)

        label_text = pool.resolve_as_utf8(attribute_label)

        if label_text == 'Code':
            return cls(attribute_label, attributes_length, CodeAttribute.from_bytes(pool, stream))
        elif label_text == 'SourceFile':
            return cls(attribute_label, attributes_length, SourceFileAttribute.from_bytes(pool, stream))     
        elif label_text == 'LineNumberTable':
            return cls(attribute_label, attributes_length, LineNumberTableAttribute.from_bytes(pool, stream))
        else:
            print('Skipping {}'.format(label_text))
            return cls(attribute_label, attributes_length, stream.read(attributes_length))

class LineNumberTableAttribute:

    def __init__(self, line_number_table_length):
        self.line_number_table_length = line_number_table_length

    def __str__(self):
        return "LineNumberTable length={}".format(self.line_number_table_length)

    @classmethod
    def from_bytes(cls, pool, stream):
        line_number_table_length = stream.read_as_int(2)
        stream.read(line_number_table_length*4)
        return cls(line_number_table_length)

class SourceFileAttribute:

    def __init__(self, sourcefile_index):
        self.sourcefile_index = sourcefile_index

    def __str__(self):
        return "[SourceFile] sourcefileIndex:{}".format(self.sourcefile_index)

    @classmethod
    def from_bytes(cls, pool, stream):
        return cls(stream.read_as_int(2))

class CodeAttribute:
    
    def __init__(self, max_stack, max_locals, instructions, attributes):
        self.max_stack = max_stack
        self.max_locals = max_locals
        self.instructions = instructions
        self.attributes = attributes

    @classmethod
    def from_bytes(cls, pool, stream):
        max_stack = stream.read_as_int(2)
        max_locals = stream.read_as_int(2)
        code_length = stream.read_as_int(4)

        ## Ignored for now
        hex_string = stream.read(code_length)
        code_buffer = HexBuffer.from_string(hex_string)
        instructions = list()

        while code_buffer.has_more():
            instructions.append(Instruction.from_buffer(code_buffer))

        ## Ignored for now
        exception_table_length = stream.read_as_int(2)
        stream.read(exception_table_length * 8)

        attributes_count = stream.read_as_int(2)
        attributes = list()
        for _ in range(0, attributes_count):
            attributes.append(AttributeInfo.from_bytes(pool, stream))

        return cls(max_stack, max_locals, instructions, attributes)

    def __str__(self):
        buffer = "Code:\n"
        buffer += "      stack={}, locals={}\n".format(self.max_stack, self.max_locals)

        for instruction in self.instructions:
            buffer += "        {}\n".format(instruction)

        for attribute in self.attributes:
            buffer += "      {}".format(attribute)

        return buffer
