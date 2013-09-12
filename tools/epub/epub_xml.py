from xml.etree import ElementTree as ET
from dateutil import parser


class EpubXml:
    def __init__(self, xml):
        self.element = ET.fromstring(xml)
        self.ns = {
            'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
            'pkg': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }

    def find(self, xpath):
        return self.element.find(xpath, self.ns)

    def findall(self, xpath):
        return self.element.find(xpath, self.ns)

    def findText(self, xpath):
        element = self.find(xpath)
        if element:
            return element.text
        else:
            return None

    def findDateValue(self, xpath):
        element = self.find(xpath)
        if element:
            return parser.parse(element.text)
        else:
            return None

    #TODO: better support for extracting elements that may not always have a key set
    #TODO: or handle with a special case for identifiers and assume uuid/isbn
    def findDictValue(self, xpath, key_name):
        extracted = {}
        elements = self.findall(xpath)
        for e in elements:
            key = e.get(key_name)
            if not key:
                key = ''
            extracted[key] = e.text
        return extracted
