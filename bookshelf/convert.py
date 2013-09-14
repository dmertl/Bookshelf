from bookshelf import Book
from bookshelf import Cover
from dateutil import parser


class EpubBookConverter:
    def __init__(self):
        self.map = {
            'creator': {
                'converter': EpubTextConverter,
                'paths': [
                    'opf:metadata/dc:creator'
                ]
            },
            'description': {
                'converter': EpubTextConverter,
                'paths': [
                    'opf:metadata/dc:description'
                ]
            },
            'language': {
                'converter': EpubTextConverter,
                'paths': [
                    'opf:metadata/dc:language'
                ]
            },
            'publishDate': {
                'converter': EpubDateConverter,
                'paths': [
                    'opf:metadata/dc:date'
                ]
            },
            'publisher': {
                'converter': EpubTextConverter,
                'paths': [
                    'opf:metadata/dc:publisher'
                ]
            },
            'subject': {
                'converter': EpubTextConverter,
                'paths': [
                    'opf:metadata/dc:subject'
                ]},
            'title': {
                'converter': EpubTextConverter,
                'paths': [
                    'opf:metadata/dc:title'
                ]},
            'identifiers': {
                'converter': EpubDictConverter,
                'paths': [
                    'opf:metadata/dc:identifier'
                ],
                'key': '{http://www.idpf.org/2007/opf}scheme',
                'default_key': 'uuid'
            },
            'cover': {
                'converter': EpubCoverConverter,
                'sources': [
                    {
                        'extractor': ITunesCoverExtractor,
                        'path': 'iTunesArtwork'
                    },
                    {
                        'extractor': RootfileCoverExtractor,
                        'path': 'opf:manifest/pkg:item/[@id="cover"]',
                    },
                    {
                        'extractor': RootfileCoverExtractor,
                        'path': 'opf:manifest/pkg:item/[@id="cover-image"]',
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

        # Map epub data to Book
        for field, mapping in self.map.iteritems():
            value = getattr(mapping['converter'], 'convert')(epub, mapping)
            if value is not None:
                setattr(book, field, value)

        return book


class EpubTextConverter:

    @staticmethod
    def convert(epub, mapping):
        """
        :param epub:
        :type epub: epub.Epub
        :param mapping:
        :type mapping: dict
        :return:
        :rtype: str
        """
        found = epub.rootfile.findInPaths(mapping['paths'])
        if found is not None:
            return found.text
        return None


class EpubDateConverter:

    @staticmethod
    def convert(epub, mapping):
        """

        :param epub:
        :type epub: epub.Epub
        :param mapping:
        :type mapping: dict
        :return:
        :rtype: datetime.datetime
        """
        found = epub.rootfile.findInPaths(mapping['paths'])
        if found is not None:
            return parser.parse(found.text)
        return None


class EpubDictConverter:

    @staticmethod
    def convert(epub, mapping):
        """

        :param epub:
        :type epub: epub.Epub
        :param mapping:
        :type mapping: dict
        :return:
        :rtype: dict
        """
        extracted = {}
        found = epub.rootfile.findallInPaths(mapping['paths'])
        if found is not None:
            for element in found:
                #TODO: if key is not found should create an XML element with no scheme in it, but allow for multiple with no key
                key = element.get(mapping['key'])
                if not key:
                    if 'default_key' in mapping:
                        key = mapping['default_key']
                    else:
                        key = ''
                extracted[key] = element.text
        return extracted

"""
Other cover cases to handle:
<meta content="my-cover-image" name="cover"/> pointing to <item href="images/9780007375509_Cover.png" id="my-cover-image" media-type="image/png"/>
<meta name="cover" content="RW_1597801348_Cover"/> pointing to <item href="1597801348_Cover.jpg" id="RW_1597801348_Cover" media-type="image/jpeg"/>
"""
class EpubCoverConverter:

    @staticmethod
    def convert(epub, mapping):
        """

        :param epub:
        :type epub: epub.Epub
        :param mapping:
        :type mapping: dict
        :return:
        :rtype: Cover
        """
        for source in mapping['sources']:
            found = source['extractor'].extract(epub, source)
            if found is not None:
                return found
        return None


#TODO: separate search vs. extract responsibilities.
# Search classes should detect presence of desired data in epub and return a dict of all necessary info
# Extractor classes should take search dict and convert into bookshelf class / data
class RootfileCoverExtractor:
    @staticmethod
    def extract(epub, settings):
        cover_element = epub.rootfile.find(settings['path'])
        if cover_element is not None:
            return Cover(epub.read(cover_element.get('href')))
        return None


class ITunesCoverExtractor:
    @staticmethod
    def extract(epub, settings):
        try:
            cover_data = epub.read('iTunesArtwork')
            return Cover(cover_data)
        except KeyError:
            # iTunesArtwork file not present
            return None
