import os
from bookshelf import Shelf
from convert import EpubBookConverter
from epub import Epub


class Librarian:
    def __init__(self):
        self.converters = {
            'epub': EpubBookConverter()
        }

    def process(self, directory):
        """

        :param directory:
        :type directory: str
        """
        shelf = Shelf(directory)
        for filename in os.listdir(directory):
            if filename[-5:] == '.epub':
                file_path = os.path.join(directory, filename)
                book = self.converters['epub'].convert(Epub(file_path))
                shelf.addBook(book)
        shelf.write()
