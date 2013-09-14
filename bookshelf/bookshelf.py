import os
import magic
import mimetypes
from xml.etree import ElementTree as ET


class Shelf:
    def __init__(self, directory):
        """

        :param directory:
        :type directory: str
        """
        self.directory = directory
        self.xmlPath = os.path.join(directory, 'shelf.xml')
        self.coversDir = os.path.join(directory, 'covers')

        #TODO: may be better to make this an etree instead of an element?
        self.xml = ET.Element('shelf')

    def addBook(self, book):
        """

        :param book:
        :type book: Book
        """
        self.xml.append(book.toXml())
        if book.cover is not None:
            book.writeCoverImage(self.coversDir)

    def write(self):
        tree = ET.ElementTree(self.xml)
        tree.write(self.xmlPath)


class Book:
    def __init__(self, filename):
        self.filename = filename
        self.creator = None
        self.description = None
        self.language = None
        self.publishDate = None
        self.publisher = None
        self.subject = None
        self.title = None
        self.identifiers = {}
        self.cover = None

    def toXml(self):
        """
        Convert book to XML for storage in shelf

        :return:
        :rtype: Book
        """
        book = ET.Element('book')

        #TODO use mapping functions/classes to handle XML conversion
        if self.creator:
            creator = ET.SubElement(book, 'creator')
            creator.text = self.creator

        if self.description:
            description = ET.SubElement(book, 'description')
            description.text = self.description

        if self.language:
            language = ET.SubElement(book, 'language')
            language.text = self.language

        if self.publishDate:
            publishDate = ET.SubElement(book, 'publishDate')
            publishDate.text = self.publishDate.isoformat()

        if self.publisher:
            publisher = ET.SubElement(book, 'publisher')
            publisher.text = self.publisher

        if self.subject:
            subject = ET.SubElement(book, 'subject')
            subject.text = self.subject

        if self.title:
            title = ET.SubElement(book, 'title')
            title.text = self.title

        identifiers = ET.SubElement(book, 'identifiers')
        if self.identifiers:
            for scheme, i in self.identifiers.iteritems():
                identifier = ET.SubElement(identifiers, 'identifier')
                identifier.text = i
                if scheme != '':
                    identifier.set('scheme', scheme)

        if self.cover:
            cover = ET.SubElement(book, 'cover')
            cover_filename = self.getCoverFilename()
            cover.set('href', os.path.join('covers', cover_filename))
            cover.set('media-type', self.cover.mediaType)

        return book

    def writeCoverImage(self, covers_dir):
        """
        Write cover image to folder with filename matching book

        :param covers_dir:
        :type covers_dir: str
        """
        cover_filename = self.getCoverFilename()
        if not os.path.exists(covers_dir):
            os.mkdir(covers_dir)
        cover_path = os.path.join(covers_dir, cover_filename)
        self.cover.write(cover_path)

    def getCoverFilename(self):
        """
        :return:
        :retype: str
        """
        return os.path.splitext(self.filename)[0] + self.cover.extension


class Cover:
    mimeTypeExtensions = {
        'image/jpeg': '.jpg',
        'image/png': '.png'
    }

    def __init__(self, data):
        """

        :param data:
        :type data: str
        """
        self.data = data
        self.mediaType = magic.from_buffer(data, mime=True)
        self.extension = self.guess_extension(self.mediaType)

    def write(self, path):
        """

        :param path:
        :type path: str
        """
        fh = open(path, 'w+')
        fh.write(self.data)
        fh.close()

    def guess_extension(self, mime_type):
        """
        Guess extension from mime type, preferring local dictionary over mimetypes module

        :param mime_type:
        :type mime_type: str
        :return:
        :rtype: str
        """
        if mime_type in Cover.mimeTypeExtensions:
            return Cover.mimeTypeExtensions[mime_type]
        else:
            return mimetypes.guess_extension(mime_type)