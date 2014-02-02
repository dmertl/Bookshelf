import os.path
from bookshelf import Book
from bookshelf import Cover
from dateutil import parser


class EpubBookConverter:
    def __init__(self):
        self.map = {
            'creator': {
                'sources': [
                    'opf:metadata/dc:creator'
                ]
            },
            'description': {
                'sources': [
                    'opf:metadata/dc:description'
                ]
            },
            'language': {
                'sources': [
                    'opf:metadata/dc:language'
                ]
            },
            'publishDate': {
                'extractor': RootfileDateExtractor,
                'sources': [
                    'opf:metadata/dc:date'
                ]
            },
            'publisher': {
                'sources': [
                    'opf:metadata/dc:publisher'
                ]
            },
            'subject': {
                'sources': [
                    'opf:metadata/dc:subject'
                ]},
            'title': {
                'sources': [
                    'opf:metadata/dc:title'
                ]},
            'identifiers': {
                'extractor': RootfileDictExtractor,
                'sources': [
                    {
                        'paths': [
                            'opf:metadata/dc:identifier'
                        ],
                        'key': '{http://www.idpf.org/2007/opf}scheme'
                    }
                ]
            },
            'cover': {
                'sources': [
                    {
                        'extractor': FileCoverExtractor,
                        'paths': [
                            'iTunesArtwork'
                        ]
                    },
                    {
                        'extractor': RootfileCoverExtractor,
                        'paths': [
                            'opf:manifest/pkg:item/[@id="cover"]',
                            'opf:manifest/pkg:item/[@id="cover-image"]'
                        ]
                    },
                    {
                        'extractor': RootfileLinkedCoverExtractor,
                        'paths': [
                            'opf:metadata/opf:meta/[@name="cover"]'
                        ]
                    }
                ]
            }
        }

    def convert(self, epub):
        """
        Create new Book from an Epub

        :param epub:
        :type epub: epub.Epub
        :return:
        :rtype: Book
        """
        # Create Book
        book = Book(epub.filename)

        # Map epub data to Book fields
        for field, mapping in self.map.iteritems():
            value = self.getMappedValue(epub, mapping)
            if value is not None:
                setattr(book, field, value)
        return book

    def getMappedValue(self, epub, mapping):
        # Set default extractor
        if 'extractor' in mapping:
            default_extractor = mapping['extractor']
        else:
            default_extractor = RootfileTextExtractor
        # Extract sources until one is successful
        for source in mapping['sources']:
            extracted = self.extractSource(epub, source, default_extractor)
            if extracted is not None:
                return extracted
        return None

    def extractSource(self, epub, source, default_extractor):
        # Use default extractor if no source specific extractor specified
        if type(source) is str:
            source = {
                'paths': [source]
            }
        if 'extractor' not in source:
            source['extractor'] = default_extractor
        # Attempt to extract field value from epub using source
        return source['extractor'].extract(epub, source)

class Extractor(object):
    pass

class RootfileTextExtractor(Extractor):
    @staticmethod
    def extract(epub, settings):
        element = epub.rootfile.findInPaths(settings['paths'])
        if element is not None:
            return element.text
        return None


class RootfileDateExtractor(Extractor):
    @staticmethod
    def extract(epub, settings):
        element = epub.rootfile.findInPaths(settings['paths'])
        if element is not None:
            return parser.parse(element.text)
        return None


class RootfileDictExtractor(Extractor):
    @staticmethod
    def extract(epub, settings):
        extracted = {}
        elements = epub.rootfile.findallInPaths(settings['paths'])
        if elements is not None:
            for element in elements:
                key = element.get(settings['key'])
                if not key:
                    key = ''
                extracted[key] = element.text
        return extracted


class RootfileCoverExtractor(Extractor):
    """
    Extract a cover image from an element in the root file. Retrieves the element by path and uses the href attribute
    as the path to the image.
    """
    @classmethod
    def extract(cls, epub, settings):
        for path in settings['paths']:
            try:
                return cls._extract(epub, path)
            except ExtractError:
                continue
        return None

    @classmethod
    def _extract(cls, epub, path):
        element = epub.rootfile.find(path)
        if element is not None:
            try:
                return Cover(cls._read_file(epub, element.get('href')))
            except KeyError:
                raise ExtractError

    @classmethod
    def _read_file(cls, epub, path):
        """
        Read a file relative to the rootfile
        """
        return epub.read(cls._rootfile_path(epub, path))

    @classmethod
    def _rootfile_path(cls, epub, path):
        """
        Get a rootfile relative path
        :rtype: str
        """
        return os.path.join(os.path.dirname(epub.rootfile_path), path)


class RootfileLinkedCoverExtractor(RootfileCoverExtractor):
    """
    Extracts a cover image from an element in the root file. The identifiable element links to an element with the image
    path. Retrieves the linking element by settings path and grabs that element's content attribute as the id of the
    element holding the image path. Then retrieves that linked element and gets the href which is a path to the file.
    """
    @classmethod
    def _extract(cls, epub, path):
        """
        Extract cover when path is via linking element's content attribute
        """
        linker = epub.rootfile.find(path)
        if linker is not None:
            linked_path = './/*/[@id="{}"]'.format(linker.get('content'))
            return super(RootfileLinkedCoverExtractor, cls)._extract(epub, linked_path)


class FileDataExtractor:
    @staticmethod
    def extract(epub, settings):
        for path in settings['paths']:
            try:
                return epub.read(path)
            except KeyError:
                continue
        return None


class FileCoverExtractor:
    @staticmethod
    def extract(epub, settings):
        try:
            return Cover(epub.readFirstInPaths(settings['paths']))
        except KeyError:
            return None


class ExtractError(Exception):
    pass