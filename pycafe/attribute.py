from constant_pool import ConstantPool, Utf8, PoolLabel

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

        label_text = pool.resolve_as_utf8(attribute_label.index)

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
        return "[LineNumberTable] length={}".format(len(self.line_number_table_length))

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
    
    def __init__(self, max_stack, max_locals, attributes):
        self.max_stack = max_stack
        self.max_locals = max_locals
        self.attributes = attributes

    @classmethod
    def from_bytes(cls, pool, stream):
        max_stack = stream.read_as_int(2)
        max_locals = stream.read_as_int(2)
        code_length = stream.read_as_int(4)

        ## Ignored for now
        stream.read(code_length)

        ## Ignored for now
        exception_table_length = stream.read_as_int(2)
        stream.read(exception_table_length * 8)

        attributes_count = stream.read_as_int(2)
        attributes = list()
        for _ in range(0, attributes_count):
            attributes.append(AttributeInfo.from_bytes(pool, stream))

        return cls(max_stack, max_locals, attributes)

    def __str__(self):
        return "[CodeAttribute] stack:" + str(self.max_stack) + " locals: " + str(self.max_locals)
