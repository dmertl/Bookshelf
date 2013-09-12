from xml.etree import ElementTree as ET
import os


class Shelf:
    def __init__(self, directory):
        self.directory = directory

    #TODO: move processing to librarian, shelf only deals in books
    def process(self):
        shelf = ET.Element('shelf')
        for epub_file in os.listdir(self.directory):
            if epub_file[-5:] == '.epub':
                print 'Processing: ' + epub_file
                # Load epub
                file_path = os.path.join(self.directory, epub_file)
                epub = Epub(file_path)
                # Generate book XML
                book_xml = self.generateXml(epub)
                # Add book to shelf XML
                shelf.append(book_xml)
                # Save cover image
                if epub.cover:
                    self.saveCover(epub)
        # Write shelf XML file
        tree = ET.ElementTree(shelf)
        tree.write(os.path.join(self.directory, 'shelf.xml'))

    def generateXml(self, epub):
        """
        :type epub: Epub
        :rtype: Element
        """
        book = ET.Element('book')

        if epub.publisher:
            publisher = ET.SubElement(book, 'publisher')
            publisher.text = epub.publisher

        if epub.description:
            description = ET.SubElement(book, 'description')
            description.text = epub.description

        if epub.language:
            language = ET.SubElement(book, 'language')
            language.text = epub.language

        if epub.creator:
            creator = ET.SubElement(book, 'creator')
            creator.text = epub.creator

        if epub.title:
            title = ET.SubElement(book, 'title')
            title.text = epub.title

        if epub.publishDate:
            publishDate = ET.SubElement(book, 'publishDate')
            publishDate.text = epub.publishDate.isoformat()

        if epub.subject:
            subject = ET.SubElement(book, 'subject')
            subject.text = epub.subject

        if epub.identifiers:
            identifiers = ET.SubElement(book, 'identifiers')
            for scheme, i in epub.identifiers.iteritems():
                identifier = ET.SubElement(identifiers, 'identifier')
                identifier.text = i
                if scheme != '':
                    identifier.set('scheme', scheme)

        if epub.cover:
            cover = ET.SubElement(book, 'cover')
            cover_filename = self.getCoverFilename(epub)
            cover.set('href', os.path.join('covers', cover_filename))
            cover.set('media-type', epub.cover['media-type'])

        return book

    def getCoverFilename(self, epub):
        return os.path.splitext(epub.filename)[0] + os.path.splitext(os.path.basename(epub.cover['href']))[1]

    def saveCover(self, epub):
        cover_filename = self.getCoverFilename(epub)
        covers_dir = os.path.join(self.directory, 'covers')
        if not os.path.exists(covers_dir):
            os.mkdir(covers_dir)
        cover_path = os.path.join(covers_dir, cover_filename)
        cover_fh = open(cover_path, 'w+')
        cover_fh.write(epub.cover['data'])
        cover_fh.close()