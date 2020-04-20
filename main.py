import zipfile
import os

from class_file import Class

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

def main():
    for class_file_path in find_class_files('targetdir'):
        print(Class.from_file_path(class_file_path))

        # print("Class file : "  + classFile)

        # classObj = HexBuffer.from_file_path(classFile)
        # print("\tMagic: {}".format(classObj.read(4)))
        # print("\tMinor Version: {}".format(classObj.read_as_int(2)))
        # print("\tMajor Version: {}".format(classObj.read_as_int(2)))
        # print()

        # pool = ConstantPool.from_bytes(classObj)
        # print()

        # accessFlags = AccessFlags.of(classObj.read_as_int(2))
        # print("Access Flags: {}".format(accessFlags))
        # print("Class Label: {}".format(PoolLabel.from_bytes(classObj)))
        # print("Super Class Label: {}".format(PoolLabel.from_bytes(classObj)))

        # interfaceTableSize = classObj.read_as_int(2)
        # print("Interface Table Size: {}".format(interfaceTableSize))
        # for i in range(0, interfaceTableSize):
        #     print(i)

        # fieldTableSize = classObj.read_as_int(2)
        # print("Field Table Size: {}".format(fieldTableSize))
        # for _ in range(0, fieldTableSize):
        #     print(Field.from_bytes(pool, classObj))

        # methodTableSize = classObj.read_as_int(2)
        # print("Method Table Size: {}".format(methodTableSize))
        # for _ in range(0, methodTableSize):
        #     print(Method.from_bytes(pool, classObj))

        # attributeTableSize = classObj.read_as_int(2)
        # print("Attribute Table Size: {}".format(attributeTableSize))
        # for _ in range(0, attributeTableSize):
        #     print("\t{}".format(AttributeInfo.from_bytes(pool, classObj)))

def prepare():
    os.system('del /s /q "*.class"')
    os.system("javac targetdir/*.java")

if __name__ == "__main__":
    prepare()
    main()