from . import EpubXml


class EpubBookConverter:
    def __init__(self):
        self.map = {
            'creator': {
                'converter': 'EpubTextConverter',
                'paths': [
                    'opf:metadata/dc:creator'
                ]
            },
            'description': {
                'converter': 'EpubTextConverter',
                'paths': [
                    'opf:metadata/dc:description'
                ]
            },
            'language': {
                'converter': 'EpubTextConverter',
                'paths': [
                    'opf:metadata/dc:language'
                ]
            },
            'publishDate': {
                'converter': 'EpubDateConverter',
                'paths': [
                    'opf:metadata/dc:date'
                ]
            },
            'publisher': {
                'converter': 'EpubTextConverter',
                'paths': [
                    'opf:metadata/dc:publisher'
                ]
            },
            'subject': {
                'converter': 'EpubTextConverter',
                'paths': [
                    'opf:metadata/dc:subject'
                ]},
            'title': {
                'converter': 'EpubTextConverter',
                'paths': [
                    'opf:metadata/dc:title'
                ]},
            'identifiers': {
                'converter': 'EpubDictConverter',
                'paths': [
                    'opf:metadata/dc:identifier'
                ],
                'key': '{http://www.idpf.org/2007/opf}scheme'
            },
            'cover': {
                'converter': 'EpubCoverConverter',
                'paths': [
                    'opf:manifest/pkg:item/[@id="cover"]'
                ]
            }
        }

    def convert(self, epub):
        """
        Create new Book from an Epub

        :param epub:
        :type epub: Epub
        :return:
        :rtype: Book
        """
        # Get rootfile
        container = EpubXml(epub.read('META-INF/container.xml'))
        rootfile_path = container.find('n:rootfiles/n:rootfile').get('full-path')
        rootfile = EpubXml(epub.read(rootfile_path))

        for field, mapping in self.map.iteritems():
            found = getattr(mapping.converter, 'convert')(rootfile, mapping)


class EpubTextConverter:

    @staticmethod
    def convert(rootfile, mapping):
        for path in mapping.paths:
            found = rootfile.findText(path)
            if found:
                return found
        return None
