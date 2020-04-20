import zipfile
import os

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from pycafe import Class

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
        
def prepare():
    os.system('del /s /q "*.class"')
    os.system("javac targetdir/*.java")

if __name__ == "__main__":
    prepare()
    main()