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
        self.xmlPath = os.path.join(directory, 'index.html')
        self.coversDir = os.path.join(directory, 'covers')

        # Initialize book shelf element
        self.xml = ET.Element('ul')
        self.xml.set('class', 'shelf')

    def addBook(self, book):
        """

        :param book:
        :type book: Book
        """
        self.xml.append(book.toHtml())
        if book.cover is not None:
            book.writeCoverImage(self.coversDir)

    def write(self):
        html = ET.Element('html')
        head = ET.SubElement(html, 'head')
        link = ET.SubElement(head, 'link')
        link.set('rel', 'stylesheet')
        link.set('type', 'text/css')
        link.set('href', 'shelf.css')
        body = ET.SubElement(html, 'body')
        body.append(self.xml)
        tree = ET.ElementTree(html)
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

    def toHtml(self):
        """
        Convert book to HTML for storage in shelf

        :return:
        :rtype: Book
        """
        book = ET.Element('li')
        book.set('class', 'book')

        link = ET.SubElement(book, 'a')
        link.set('href', self.filename)

        cover = ET.SubElement(link, 'img')
        cover.set('class', 'cover')
        if self.cover:
            cover.set('src', os.path.join('covers', self.getCoverFilename()))

        title = ET.SubElement(book, 'h2')
        title.set('class', 'title')
        if self.title:
            title.text = self.title

        author = ET.SubElement(book, 'h3')
        author.set('class', 'author')
        if self.creator:
            author.text = self.creator

        # if self.description:
        #     description = ET.SubElement(book, 'description')
        #     description.text = self.description
        #
        # if self.language:
        #     language = ET.SubElement(book, 'language')
        #     language.text = self.language
        #
        # if self.publishDate:
        #     publishDate = ET.SubElement(book, 'publishDate')
        #     publishDate.text = self.publishDate.isoformat()
        #
        # if self.publisher:
        #     publisher = ET.SubElement(book, 'publisher')
        #     publisher.text = self.publisher
        #
        # if self.subject:
        #     subject = ET.SubElement(book, 'subject')
        #     subject.text = self.subject
        #
        # identifiers = ET.SubElement(book, 'identifiers')
        # if self.identifiers:
        #     for scheme, i in self.identifiers.iteritems():
        #         identifier = ET.SubElement(identifiers, 'identifier')
        #         identifier.text = i
        #         if scheme != '':
        #             identifier.set('scheme', scheme)

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