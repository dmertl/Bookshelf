import os
import zipfile


class Epub:
    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.filename = os.path.basename(path)
        self.zipfile = zipfile.ZipFile(path)

    def readFile(self, file_path):
        return self.zipfile.read(file_path)
