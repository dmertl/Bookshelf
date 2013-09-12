"""
Librarian will create a viewable index of ebooks in any directory

Creates shelf.xml and extracts cover images to covers/
"""
# TODO: unit tests
# TODO: test on more ebooks
# TODO: better coverage on alternate specifications for cover image
# TODO: styling of shelf.xml XSLT is necessary for images
# TODO: some kind of alert or visibility into files with missing data
# TODO: interactive elements with JS?
# TODO: search for cover images that have no matching ebook and remove them
# TODO: save time by not processing ebooks that have not been modified. store modified date or checksum

import zipfile
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element
from pprint import pprint
from dateutil import parser
import sys
import os


class Epub:
    def __init__(self, epub_file):
        self.path = os.path.abspath(epub_file)
        self.filename = os.path.basename(epub_file)

        self.ns = {
            'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
            'pkg': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }

        epub_zip = zipfile.ZipFile(epub_file)

        container = EpubContainerXml(epub_zip.read('META-INF/container.xml'))

        root_file = container.getRootfile()

        root = EpubRootXml(epub_zip.read(root_file))

        self.creator = root.getCreator()
        self.description = root.getDescription()
        self.language = root.getLanguage()
        self.publishDate = root.getPublishDate()
        self.publisher = root.getPublisher()
        self.subject = root.getSubject()
        self.title = root.getTitle()
        self.identifiers = root.getIdentifiers()
        self.cover = root.getCover()
        if self.cover:
            self.cover['data'] = bytes(epub_zip.read(self.cover['href']))

        epub_zip.close()


class EpubXmlParser:
    def __init__(self, element):
        if element is None:
            raise ValueError('Element not provided to EpubXmlParser')
        self.ns = {
            'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
            'pkg': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'opf': 'http://www.idpf.org/2007/opf'
        }
        self.element = element
        self.extractors = {
            'text': self.extractTextValue,
            'date': self.extractDateValue,
            'dict': self.extractDictValue
        }

    def find(self, xpath, extract=None, options=None):
        if extract == 'dict':
            found = self.element.findall(xpath, self.ns)
        else:
            found = self.element.find(xpath, self.ns)
        if found is not None and extract and extract in self.extractors:
            found = self.extractors[extract](found, options)
        return found

    def extractTextValue(self, element, options):
        return element.text

    def extractDateValue(self, element, options):
        return parser.parse(element.text)

    #TODO: better support for extracting elements that may not always have a key set
    #TODO: or handle with a special case for identifiers and assume uuid/isbn
    def extractDictValue(self, element, options):
        extracted = {}
        if 'key' in options:
            for e in element:
                key = e.get(options['key'])
                if not key:
                    key = ''
                extracted[key] = e.text
            return extracted
        else:
            raise ValueError('Must provide "key" option for extracting dict value')


class EpubXmlFile:
    def __init__(self, xml_data):
        self.parser = EpubXmlParser(ET.fromstring(xml_data))

    def find(self, key, extract=None, options=None):
        return self.parser.find(key, extract, options)


class EpubContainerXml(EpubXmlFile):
    def getRootfile(self):
        return self.find('n:rootfiles/n:rootfile').get('full-path')


class EpubRootXml(EpubXmlFile):
    def __init__(self, xml_data):
        EpubXmlFile.__init__(self, xml_data)
        self.metadata = EpubXmlParser(self.find('opf:metadata'))
        self.manifest = EpubXmlParser(self.find('opf:manifest'))

    def getCreator(self):
        return self.metadata.find('dc:creator', 'text')

    def getDescription(self):
        return self.metadata.find('dc:description', 'text')

    def getLanguage(self):
        return self.metadata.find('dc:language', 'text')

    def getPublishDate(self):
        return self.metadata.find('dc:date', 'date')

    def getPublisher(self):
        return self.metadata.find('dc:publisher', 'text')

    def getSubject(self):
        return self.metadata.find('dc:subject', 'text')

    def getTitle(self):
        return self.metadata.find('dc:title', 'text')

    def getIdentifiers(self):
        return self.metadata.find('dc:identifier', 'dict', {'key': '{http://www.idpf.org/2007/opf}scheme'})

    def getCover(self):
        element = self.manifest.find('pkg:item/[@id="cover"]')
        if element is not None:
            return {
                'href': element.get('href'),
                'media-type': element.get('media-type')
            }
        else:
            return None





if len(sys.argv) == 2:
    shelf = Shelf(sys.argv[1])
    shelf.process()
else:
    print 'Invalid syntax. {} directory'.format(sys.argv[0])