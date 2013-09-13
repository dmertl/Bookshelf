from xml.etree import ElementTree as ET
import os
from . import EpubBookConverter
from . import Epub


class Shelf:
    def __init__(self, directory):
        self.directory = directory
        self.xmlPath = os.path.join(directory, 'shelf.xml')
        self.coversDir = os.path.join(directory, 'covers')

        #TODO: may be better to make this an etree instead of an element?
        self.xml = ET.Element('shelf')

        self.converters = {
            'epub': EpubBookConverter()
        }

        self._processDirectory(directory)

    def _processDirectory(self, directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if filename[-5:] == '.epub':
                book = self.converters['epub'].convert(Epub(file_path))
                self._addBook(book)
        self._write()

    def _addBook(self, book):
        self.xml.append(book.toXml())
        book.writeCoverImage(self.coversDir)

    def _write(self):
        tree = ET.ElementTree(self.xml)
        tree.write(self.xmlPath)
