from xml.etree import ElementTree as ET
import os


class Book:
    def __init__(self):
        print 'Book init'
        self.creator = None
        self.description = None
        self.filename = None
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
        :rtype:
        """
        book = ET.Element('book')

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
        :type covers_dir:
        :return:
        :rtype:
        """
        cover_filename = self.getCoverFilename()
        if not os.path.exists(covers_dir):
            os.mkdir(covers_dir)
        cover_path = os.path.join(covers_dir, cover_filename)
        self.cover.write(cover_path)

    def getCoverFilename(self):
        return os.path.splitext(self.filename)[0] + os.path.splitext(os.path.basename(self.cover.href))[1]
